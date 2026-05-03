"""
Script to merge a trained LoRA adapter back into the base model.
This is necessary for deploying the fine-tuned model for inference without the PEFT overhead,
or for deploying to local execution engines like Ollama/llama.cpp.
"""

import argparse
import logging
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def merge_adapter(
    base_model_id: str,
    adapter_path: str,
    output_dir: str,
    push_to_hub: bool = False,
    hub_model_id: str = None
) -> None:
    """
    Merges a LoRA adapter with the base model and saves the combined model.
    """
    adapter_path = Path(adapter_path)
    output_dir = Path(output_dir)
    
    if not adapter_path.exists():
        raise FileNotFoundError(f"Adapter path {adapter_path} does not exist. Run train_lora.py first.")
        
    logger.info(f"Loading base model: {base_model_id}")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    logger.info(f"Loading tokenizer: {base_model_id}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
    
    logger.info(f"Loading PEFT adapter from {adapter_path}")
    model = PeftModel.from_pretrained(base_model, str(adapter_path))
    
    logger.info("Merging adapter with base model...")
    model = model.merge_and_unload()
    
    logger.info(f"Saving merged model to {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(output_dir), safe_serialization=True)
    tokenizer.save_pretrained(str(output_dir))
    
    if push_to_hub and hub_model_id:
        logger.info(f"Pushing merged model to Hugging Face Hub: {hub_model_id}")
        model.push_to_hub(hub_model_id, safe_serialization=True)
        tokenizer.push_to_hub(hub_model_id)
        
    logger.info("Merge complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge a LoRA adapter into the base model.")
    parser.add_argument("--base_model_id", type=str, default="mistralai/Mistral-7B-v0.1", help="HuggingFace base model ID")
    parser.add_argument("--adapter_path", type=str, default="data/models/arogya_lora", help="Path to trained LoRA adapter")
    parser.add_argument("--output_dir", type=str, default="data/models/arogya_merged", help="Output directory for merged model")
    parser.add_argument("--push_to_hub", action="store_true", help="Push the merged model to Hugging Face Hub")
    parser.add_argument("--hub_model_id", type=str, help="Hugging Face repo ID to push to (if --push_to_hub is set)")
    
    args = parser.parse_args()
    
    merge_adapter(
        base_model_id=args.base_model_id,
        adapter_path=args.adapter_path,
        output_dir=args.output_dir,
        push_to_hub=args.push_to_hub,
        hub_model_id=args.hub_model_id
    )
