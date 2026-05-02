"""
Script to train a LoRA adapter for a base language model using TRL and PEFT.
This is used in Phase 6 for domain adaptation to medical research/report generation.
"""

import argparse
import logging
from pathlib import Path

import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_lora(
    model_id: str,
    dataset_path: str,
    output_dir: str,
    epochs: int = 3,
    batch_size: int = 4,
    learning_rate: float = 2e-4,
    lora_r: int = 16,
    lora_alpha: int = 32,
    lora_dropout: float = 0.05,
    max_seq_length: int = 1024,
    use_4bit: bool = True
) -> None:
    """
    Fine-tunes a model using LoRA and saves the adapter.
    """
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset path {dataset_path} does not exist. Run prepare_dataset.py first.")

    logger.info(f"Loading dataset from {dataset_path}")
    dataset = load_from_disk(str(dataset_path))
    
    if 'train' not in dataset:
        raise ValueError("Dataset must contain a 'train' split.")
        
    train_data = dataset['train']
    eval_data = dataset['test'] if 'test' in dataset else None

    logger.info(f"Loading tokenizer for {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    logger.info(f"Loading model {model_id}")
    
    # Configure quantization if requested (useful for local training on consumer GPUs)
    if use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
    else:
        bnb_config = None

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    if use_4bit:
        model = prepare_model_for_kbit_training(model)

    logger.info("Configuring LoRA")
    peft_config = LoraConfig(
        lora_alpha=lora_alpha,
        lora_dropout=lora_dropout,
        r=lora_r,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    logger.info("Setting up SFTTrainer")
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        save_steps=50,
        logging_steps=10,
        learning_rate=learning_rate,
        weight_decay=0.001,
        fp16=True,
        bf16=False,
        max_grad_norm=0.3,
        max_steps=-1,
        warmup_ratio=0.03,
        group_by_length=True,
        lr_scheduler_type="cosine",
        report_to="none", 
        dataset_text_field="text",
        max_seq_length=max_seq_length
    )
    
    if eval_data:
        training_args.eval_strategy = "steps"
        training_args.eval_steps = 50

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        eval_dataset=eval_data,
        peft_config=peft_config,
        tokenizer=tokenizer,
        args=training_args,
    )

    logger.info("Starting training...")
    trainer.train()

    logger.info(f"Saving final adapter to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    logger.info("Training complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a LoRA adapter for a medical assistant model.")
    parser.add_argument("--model_id", type=str, default="mistralai/Mistral-7B-v0.1", help="HuggingFace model ID")
    parser.add_argument("--dataset", type=str, default="data/processed/finetune_dataset", help="Path to prepared dataset")
    parser.add_argument("--output_dir", type=str, default="data/models/arogya_lora", help="Output directory for adapter")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size per device")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--no_4bit", action="store_true", help="Disable 4-bit quantization")
    
    args = parser.parse_args()
    
    train_lora(
        model_id=args.model_id,
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        use_4bit=not args.no_4bit
    )
