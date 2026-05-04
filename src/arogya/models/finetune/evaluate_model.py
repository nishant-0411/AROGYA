import argparse
from pathlib import Path
import torch
from datasets import load_from_disk
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

def evaluate_model(model_id: str, dataset_path: str, batch_size: int = 4, max_samples: int = None, is_peft: bool = False, base_model_id: str = None) -> None:
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset path {dataset_path} does not exist.")
    dataset = load_from_disk(str(dataset_path))
    if 'test' not in dataset:
        raise ValueError("Dataset must contain a 'test' split.")
    eval_data = dataset['test']
    if max_samples:
        eval_data = eval_data.select(range(min(max_samples, len(eval_data))))
    if is_peft:
        if not base_model_id:
            raise ValueError("base_model_id must be provided if is_peft is True")
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
        from peft import PeftModel
        model = PeftModel.from_pretrained(base_model, model_id)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    device = model.device
    for i in tqdm(range(0, len(eval_data), batch_size)):
        batch_texts = eval_data[i:i + batch_size]["text"]
        inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=1024).to(device)
        with torch.no_grad():
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
            total_loss += loss.item() * inputs["input_ids"].size(0)
            total_tokens += inputs["input_ids"].size(0)
    avg_loss = total_loss / total_tokens
    perplexity = torch.exp(torch.tensor(avg_loss)).item()
    print(f"Evaluation Results for {model_id}:")
    print(f"Average Loss: {avg_loss:.4f}")
    print(f"Perplexity: {perplexity:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, required=True)
    parser.add_argument("--dataset", type=str, default="data/processed/finetune_dataset")
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--max_samples", type=int, default=None)
    parser.add_argument("--is_peft", action="store_true")
    parser.add_argument("--base_model_id", type=str, default=None)
    args = parser.parse_args()
    evaluate_model(
        model_id=args.model_id,
        dataset_path=args.dataset,
        batch_size=args.batch_size,
        max_samples=args.max_samples,
        is_peft=args.is_peft,
        base_model_id=args.base_model_id
    )
