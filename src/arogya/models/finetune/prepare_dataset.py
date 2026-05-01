"""
Dataset preparation for LoRA fine-tuning.
Converts raw instruction data into the format expected by TRL's SFTTrainer.
"""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from datasets import Dataset, load_dataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_instruction(instruction: str, response: str, context: Optional[str] = None) -> str:
    """
    Format a data sample into a standardized prompt template.
    Using Alpaca-style template for medical QA/summarization.
    """
    if context and str(context).strip():
        return (
            "Below is an instruction that describes a task, paired with an input that provides further context.\n\n"
            f"### Instruction:\n{instruction}\n\n"
            f"### Input:\n{context}\n\n"
            f"### Response:\n{response}"
        )
    else:
        return (
            "Below is an instruction that describes a task.\n\n"
            f"### Instruction:\n{instruction}\n\n"
            f"### Response:\n{response}"
        )

def process_huggingface_dataset(dataset_name: str, split: str = "train") -> Dataset:
    """
    Load a dataset from the HuggingFace hub.
    This is an example for 'pubmed_qa' or similar datasets where we map columns.
    """
    logger.info(f"Loading HuggingFace dataset: {dataset_name} ({split} split)")
    dataset = load_dataset(dataset_name, split=split)
    return dataset

def prepare_dataset(
    input_source: str,
    output_dir: str | Path,
    val_split_size: float = 0.1,
    seed: int = 42,
    is_hub_dataset: bool = False
) -> None:
    """
    Load data, format it, and save it as Hugging Face dataset arrows.
    
    If `is_hub_dataset` is True, `input_source` is a HuggingFace dataset name.
    Otherwise, it's a path to a local JSONL or CSV file.
    """
    output_dir = Path(output_dir)
    
    if is_hub_dataset:
        dataset = process_huggingface_dataset(input_source)
    else:
        input_path = Path(input_source)
        logger.info(f"Loading local data from {input_path}")
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        if input_path.suffix == ".jsonl":
            dataset = load_dataset("json", data_files=str(input_path), split="train")
        elif input_path.suffix == ".csv":
            dataset = load_dataset("csv", data_files=str(input_path), split="train")
        else:
            raise ValueError("Unsupported file format. Please provide a .jsonl or .csv file.")
    
    def format_row(row: Dict[str, Any]) -> Dict[str, str]:
        instruction = row.get("instruction", row.get("question", row.get("prompt", "")))
        response = row.get("response", row.get("answer", row.get("completion", "")))
        context = row.get("context", row.get("input", ""))
        
        if not instruction or not response:
            logger.warning(f"Skipping row missing instruction or response: {row.keys()}")
            return {"text": ""}
            
        text = format_instruction(
            instruction=instruction,
            response=response,
            context=context
        )
        return {"text": text}
    
    logger.info("Formatting dataset into instruction prompts...")
    # Filter out rows that couldn't be formatted
    formatted_dataset = dataset.map(format_row, remove_columns=dataset.column_names)
    formatted_dataset = formatted_dataset.filter(lambda x: len(x["text"]) > 0)
    
    # Split into train and validation
    logger.info(f"Splitting dataset (val size: {val_split_size})")
    split_dataset = formatted_dataset.train_test_split(
        test_size=val_split_size, 
        seed=seed
    )
    
    logger.info(f"Train size: {len(split_dataset['train'])}")
    logger.info(f"Validation size: {len(split_dataset['test'])}")
    
    # Save to disk
    output_dir.mkdir(parents=True, exist_ok=True)
    split_dataset.save_to_disk(str(output_dir))
    logger.info(f"Dataset successfully saved to {output_dir}")

def create_dummy_dataset(output_path: str | Path) -> None:
    """Create a small dummy dataset for testing if none is provided."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    dummy_data = [
        {
            "instruction": "Summarize the following patient notes.",
            "context": "Patient is a 45-year-old male presenting with chronic cough and mild fever. No history of smoking. Chest X-ray clear.",
            "response": "A 45-year-old non-smoking male presented with chronic cough and mild fever, with a clear chest X-ray."
        },
        {
            "instruction": "What are the common side effects of lisinopril?",
            "context": "",
            "response": "Common side effects of lisinopril include dry cough, dizziness, headache, and elevated potassium levels."
        },
        {
            "instruction": "Extract the diagnoses from the clinical text.",
            "context": "Assessment: 1. Type 2 Diabetes Mellitus, well controlled. 2. Essential hypertension. Plan: Continue current medications.",
            "response": "1. Type 2 Diabetes Mellitus\n2. Essential hypertension"
        }
    ]
    
    with open(output_path, "w") as f:
        for item in dummy_data:
            f.write(json.dumps(item) + "\n")
            
    logger.info(f"Created dummy dataset at {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare dataset for medical fine-tuning")
    parser.add_argument("--input", type=str, help="Path to raw JSONL/CSV file or HF dataset name")
    parser.add_argument("--output_dir", type=str, default="data/processed/finetune_dataset", help="Directory to save HF dataset")
    parser.add_argument("--val_split", type=float, default=0.1, help="Validation split fraction")
    parser.add_argument("--hub", action="store_true", help="Set if input is a HuggingFace hub dataset name")
    parser.add_argument("--demo", action="store_true", help="Create and use a dummy dataset for testing")
    
    args = parser.parse_args()
    
    if args.demo:
        dummy_path = Path("data/raw/dummy_medical_qa.jsonl")
        create_dummy_dataset(dummy_path)
        prepare_dataset(str(dummy_path), args.output_dir, args.val_split, is_hub_dataset=False)
    elif args.input:
        prepare_dataset(args.input, args.output_dir, args.val_split, is_hub_dataset=args.hub)
    else:
        logger.error("Must provide either --input or --demo flag")
        parser.print_help()
