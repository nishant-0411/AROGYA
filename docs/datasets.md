# Fine-Tuning Dataset Preparation Guide

As part of the fine-tuning pipeline for the AROGYA assistant, we need to adapt a base model (e.g., Llama-3 8B or Mistral) for specific medical tasks such as summarization, evidence-grounded QA, or medical report formatting. This document explains how we prepare and format datasets to achieve this.

## Overview of Dataset Formatting

We use an Alpaca-style instruction tuning format. All raw data must be converted into standardized prompt templates containing:
- **Instruction**: The task description.
- **Context/Input** (Optional): Additional information, like patient notes or RAG retrieved chunks.
- **Response**: The expected output.

Our script `src/arogya/models/finetune/prepare_dataset.py` handles this mapping automatically.

## Supported Input Sources

You can provide data to the preparation script in two ways:
1. **Local Files (`.jsonl` or `.csv`)**: Ensure your rows contain keys like `instruction` (or `question`), `context` (or `input`), and `response` (or `answer`).
2. **Hugging Face Hub**: Standard public datasets (e.g., `pubmed_qa`).

## Using the Preparation Script

The `prepare_dataset.py` script loads your raw data, applies the Alpaca-style prompt formatting, filters out invalid rows, splits the data into train and validation sets, and saves it in Hugging Face Dataset format for `TRL`'s `SFTTrainer`.

### 1. Generating a Dummy Dataset for Testing
To verify the pipeline without downloading large datasets, you can generate a small dummy dataset:
```bash
python src/arogya/models/finetune/prepare_dataset.py --demo
```
This will create `data/raw/dummy_medical_qa.jsonl` and process it into `data/processed/finetune_dataset`.

### 2. Processing a Local Dataset
If you have a curated local dataset (e.g., `data/raw/my_medical_qa.jsonl`):
```bash
python src/arogya/models/finetune/prepare_dataset.py \
    --input data/raw/my_medical_qa.jsonl \
    --output_dir data/processed/finetune_dataset \
    --val_split 0.1
```

### 3. Processing a Hugging Face Hub Dataset
To prepare a dataset hosted on Hugging Face (e.g., `pubmed_qa`):
```bash
python src/arogya/models/finetune/prepare_dataset.py \
    --input pubmed_qa \
    --hub \
    --output_dir data/processed/finetune_dataset \
    --val_split 0.1
```

## Recommended Open-Source Datasets

If you are looking to build a real fine-tuning set, consider:
- **PubMedQA**: Biomedical question answering with long-form context.
- **MedQA / USMLE**: For tuning medical reasoning and clinical logic.
- **ChatDoctor**: Patient-doctor dialogues for triage and summarization tasks.

*Note: The actual training script (`train_lora.py`) expects the dataset to be in the formatted Hugging Face layout created by this pipeline.*
