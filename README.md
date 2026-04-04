# Arogya

Production-style multimodal medical research assistant built around the `OmniMind` architecture.

`Arogya` is designed as a serious portfolio project that combines:

- multimodal input handling
- multi-agent orchestration
- RAG with citation-backed retrieval
- fine-tuning workflow
- evaluation and hallucination detection
- deployment and monitoring

The long-term goal is a system where a user can upload an X-ray, a research PDF, and a text query, and receive a structured analysis report grounded in retrieved evidence instead of unsupported generation.

## Why This Project Matters

This project is meant to showcase all three layers together:

- `ML engineering`: dataset preparation, fine-tuning, multimodal pipelines
- `MLOps`: evals, monitoring, serving, containerization, deployment
- `system design`: agents, memory, tools, async workflows, retrieval stack

That makes `Arogya` much stronger than a basic chatbot clone and much closer to a production-ready AI system.

## Core Use Case

Example flow:

1. User uploads a medical research paper or case PDF
2. User optionally uploads an image such as an X-ray
3. User asks a question in natural language
4. Multiple agents collaborate to retrieve evidence, verify claims, and draft a report
5. The system returns a structured answer with citations, confidence notes, and limitations

## Architecture Overview

The project follows the `OmniMind` design in four layers:

### 1. Multimodal Input

- `Text / Query`
- `PDF / Docs`
- `Image / Video`
- `Audio` as an optional later extension

### 2. Agent Layer

- `Triage Agent` to understand the task and route it
- `RAG Agent` to fetch grounded evidence
- `Vision Agent` to process image inputs
- `Verifier Agent` to cross-check claims
- `Report Agent` to synthesize the final answer
- `Guardrail Agent` to enforce high-stakes safety rules

### 3. Core Intelligence Layer

- orchestrator graph
- short-term and long-term memory
- vector retrieval
- external tools such as PubMed and web search
- model gateway for base and fine-tuned models

### 4. Output and Serving

- `FastAPI` backend
- `Streamlit` demo UI
- background workers for long-running tasks
- evaluation dashboard
- Docker and cloud deployment

## Planned Tech Stack

### Backend and serving

- Python `3.11`
- `FastAPI`
- `Streamlit`
- `Celery`
- `Redis`
- `PostgreSQL`
- `Qdrant`

### ML and multimodal

- `torch`
- `transformers`
- `sentence-transformers`
- `peft`
- `trl`
- `accelerate`
- `bitsandbytes`
- `pymupdf`
- `unstructured`
- `pytesseract`
- `Pillow`

### Retrieval and evaluation

- `LangGraph`
- `ragas`
- `LangSmith`
- `MLflow`
- `pytest`
- `ruff`
- `mypy`

## Project Status

Current state:

- architecture diagram added
- full phased project plan added
- implementation scaffold not created yet

Roadmap source:

- [PROJECT_PLAN.md](/Users/nishant/Resume Projects/AROGYA/PROJECT_PLAN.md)
- [omnimind_architecture.svg](/Users/nishant/Resume Projects/AROGYA/omnimind_architecture.svg)

## Planned Repository Structure

```text
AROGYA/
├── apps/
│   ├── api/
│   ├── ui/
│   └── worker/
├── src/
│   └── arogya/
│       ├── agents/
│       ├── orchestrator/
│       ├── multimodal/
│       ├── rag/
│       ├── models/
│       ├── memory/
│       ├── tools/
│       └── evals/
├── data/
├── docs/
├── notebooks/
├── scripts/
├── tests/
├── PROJECT_PLAN.md
└── omnimind_architecture.svg
```

## Phase Roadmap

### Phase 0

Repo foundation:

- project skeleton
- env config
- FastAPI health endpoint
- blank Streamlit app
- lint and test setup

### Phase 1

Multimodal ingestion baseline:

- PDF parsing
- OCR support
- image ingestion
- normalized document schema

### Phase 2

RAG MVP:

- chunking
- embeddings
- hybrid retrieval
- citations

### Phase 3

Multi-agent orchestration:

- triage
- retrieval
- verification
- report generation

### Phase 4

Memory and tooling:

- session memory
- persistent case memory
- PubMed integration
- optional external search

### Phase 5

Vision support:

- image-based findings
- multimodal reasoning
- image plus literature report generation

### Phase 6

Fine-tuning pipeline:

- dataset preparation
- LoRA training
- adapter merge
- before and after evaluation

### Phase 7

Reliability and evals:

- RAGAS
- hallucination detection
- regression suite
- evaluation dashboard

### Phase 8

Production serving:

- async job execution
- report generation workers
- Docker stack

### Phase 9

Cloud and portfolio polish:

- deployment manifests
- monitoring
- demo script
- interview-ready documentation

## First Milestone

The best first milestone for this repo is:

- upload one medical paper PDF
- ask one query in chat
- retrieve relevant chunks
- generate a cited answer
- display citations in the UI

That milestone alone already demonstrates practical RAG value.

## Planned Output Format

The final system should generate reports with:

- user query
- input summary
- retrieved evidence
- image findings if present
- verification notes
- final synthesized answer
- confidence level
- limitations
- citations

## Responsible AI Notes

This project should be presented as a `medical research assistant`, not as a diagnostic or clinical decision system.

Rules for the build:

- use only public or de-identified datasets
- show citations for factual claims
- mark uncertainty explicitly
- avoid diagnosis-style language in the UI
- keep verification and guardrails visible in the system design

## Getting Started

Implementation has not been scaffolded yet, but the recommended first files are:

- [pyproject.toml](/Users/nishant/Resume Projects/AROGYA/pyproject.toml)
- [.env.example](/Users/nishant/Resume Projects/AROGYA/.env.example)
- [Makefile](/Users/nishant/Resume Projects/AROGYA/Makefile)
- [apps/api/main.py](/Users/nishant/Resume Projects/AROGYA/apps/api/main.py)
- [apps/ui/app.py](/Users/nishant/Resume Projects/AROGYA/apps/ui/app.py)
- [src/arogya/rag/chunking.py](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/chunking.py)
- [src/arogya/multimodal/pdf_pipeline.py](/Users/nishant/Resume Projects/AROGYA/src/arogya/multimodal/pdf_pipeline.py)

If you want to continue immediately, the next best step is to scaffold Phase 0 and create the initial FastAPI plus Streamlit starter apps.
