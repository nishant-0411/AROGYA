# Arogya

> Production-grade multimodal medical research assistant built on the **OmniMind** architecture.

Arogya demonstrates the full depth of an AI engineering portfolio — not just a chatbot, but a system that combines multimodal input handling, LangGraph multi-agent orchestration, citation-backed RAG, a LoRA fine-tuning pipeline, evaluation suites, async task workers, containerised deployment, and cloud infrastructure-as-code.

---

## Why This Project Matters

Arogya is designed to show all three engineering layers together:

| Layer | What's demonstrated |
|---|---|
| **ML Engineering** | Multimodal pipelines, LoRA fine-tuning with PEFT/TRL, adapter merging, model evaluation |
| **MLOps** | RAGAS + DeepEval evaluation suites, hallucination detection, regression suite, Docker + K8s + Terraform |
| **System Design** | LangGraph agent orchestration, short/long-term memory, hybrid RAG, async Celery workers |

Built entirely on **open-source tools and free resources**.

---

## Core Use Case

A user can upload a medical research paper (PDF) and optionally a patient image (e.g. an X-ray), ask a natural-language question, and receive a structured, citation-backed report:

1. **Upload** a clinical research PDF (e.g. a paper on Pulmonary Embolism)
2. **Upload** an image (e.g. a chest X-ray) — optional
3. **Ask** a question in natural language
4. **Multi-agent workflow** routes the query through Triage → Vision → RAG → Verifier → Report agents
5. **Receive** a structured report with visual findings, retrieved evidence, verification scores, confidence levels, limitations, and inline citations

---

## Architecture

The system is built in four layers following the OmniMind design:

```
┌─────────────────────────────────────────────────┐
│  Multimodal Input Layer                         │
│  Text · PDF/Docs · Images (X-rays, scans)       │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  LangGraph Agent Orchestration                  │
│                                                 │
│  Triage ──► Vision ──► RAG ──► Verifier ──► Report │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  Core Intelligence Layer                        │
│  Qdrant Vector DB · LangChain · Session &       │
│  Case Memory · PubMed · DuckDuckGo · Ollama     │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│  Serving & Infra Layer                          │
│  FastAPI · Streamlit · Celery · Redis ·         │
│  PostgreSQL · Docker · Kubernetes · Terraform   │
└─────────────────────────────────────────────────┘
```

### Agents (`src/arogya/agents/`)

| Agent | Responsibility |
|---|---|
| `triage_agent.py` | Parses the incoming state, detects image presence, and routes to Vision or RAG |
| `vision_agent.py` | Analyses uploaded images via the vision model gateway; extracts radiological findings |
| `rag_agent.py` | Queries Qdrant with hybrid retrieval and attaches cited passages to the state |
| `verifier_agent.py` | Cross-checks claims for potential hallucinations and assigns a verification score |
| `report_agent.py` | Synthesises the final structured report from all agent outputs |

The agents are wired together as a **LangGraph `StateGraph`** in `src/arogya/orchestrator/graph.py`.

---

## Repository Structure

```text
AROGYA/
├── apps/
│   ├── api/                        # FastAPI backend (main.py + route handlers)
│   ├── ui/                         # Streamlit frontend (app.py + pages/)
│   └── worker/                     # Celery async task worker
├── src/arogya/
│   ├── agents/                     # Triage, RAG, Vision, Verifier, Report agents
│   ├── orchestrator/               # LangGraph StateGraph (graph.py, state.py)
│   ├── multimodal/                 # PDF, image, and text ingestion pipelines
│   ├── rag/                        # Chunking, embeddings, retriever, citation builder
│   ├── models/
│   │   ├── vision_gateway.py       # Ollama-backed vision model router
│   │   └── finetune/               # LoRA dataset prep, training, merge, evaluation
│   ├── memory/                     # Session memory + persistent patient case memory
│   ├── tools/                      # PubMed, DuckDuckGo, calculator tools
│   └── evals/                      # RAGAS, hallucination, multimodal, regression evals
├── infra/
│   ├── docker/                     # Dockerfiles for api / ui / worker
│   ├── k8s/                        # Kubernetes manifests (api, ui, worker, qdrant)
│   └── terraform/                  # AWS VPC, EKS, RDS (Postgres), ElastiCache (Redis), ECR
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evals/
├── data/
├── docs/
│   └── demo-script.md              # Step-by-step demo walkthrough
├── notebooks/
├── scripts/
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── PROJECT_PLAN.md
└── omnimind_architecture.svg
```

---

## Tech Stack

### Backend & Serving
- **Python 3.11** · **FastAPI** · **Uvicorn** · **Pydantic v2**
- **Streamlit** + Plotly (frontend UI)
- **Celery** + **Redis** (async task queue)
- **PostgreSQL** + SQLAlchemy (relational store)
- **Qdrant** (vector database)

### ML & Multimodal
- `torch` · `transformers` · `sentence-transformers`
- `peft` · `trl` · `accelerate` (LoRA fine-tuning)
- `PyMuPDF` · `unstructured` · `pytesseract` · `Pillow` (document & OCR parsing)
- **Ollama** (local open-source LLM & vision model gateway)

### Agentic Framework
- **LangChain** · **LangGraph** · `langchain-qdrant` · `langchain-huggingface`

### Retrieval & Evaluation
- **RAGAS** · **DeepEval** (RAG evaluation metrics)
- `duckduckgo-search` · PubMed API (external knowledge tools)

### Infrastructure
- **Docker** + **Docker Compose**
- **Kubernetes** (K8s manifests for all services)
- **Terraform** (AWS EKS, RDS, ElastiCache, ECR, VPC)

### Developer Tooling
- `pytest` · `pytest-asyncio` · `ruff` · `black` · `mypy` · `pre-commit`

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally (`ollama serve`)
- Docker (for the full stack)

### Local Development

```bash
# 1. Clone and create a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Edit .env and fill in any required keys

# 3. Start infrastructure (Qdrant, Redis, Postgres)
docker-compose up -d redis qdrant postgres

# 4. Run the FastAPI backend
make run-api          # → http://localhost:8000
                      #   Docs at http://localhost:8000/docs

# 5. Run the Streamlit UI (separate terminal)
make run-ui           # → http://localhost:8501
```

### Full Stack with Docker Compose

```bash
docker-compose up --build
```

This starts all six services: `api`, `worker`, `ui`, `redis`, `qdrant`, `postgres`.

### Running Tests

```bash
pytest tests/
```

---

## Evaluation Suite

The `src/arogya/evals/` module provides four evaluation scripts:

| Script | What it measures |
|---|---|
| `ragas_eval.py` | Retrieval faithfulness, answer relevancy, context precision via RAGAS |
| `hallucination_eval.py` | Hallucination detection using DeepEval |
| `multimodal_eval.py` | Vision pipeline accuracy and multimodal report quality |
| `regression_suite.py` | End-to-end regression tests across known queries |

---

## Fine-Tuning Pipeline

The `src/arogya/models/finetune/` directory contains the full LoRA pipeline:

```bash
# 1. Prepare a medical instruction dataset
python src/arogya/models/finetune/prepare_dataset.py --demo

# 2. Train a LoRA adapter (uses PEFT + TRL)
python src/arogya/models/finetune/train_lora.py

# 3. Merge the adapter into the base model
python src/arogya/models/finetune/merge_adapter.py

# 4. Evaluate base vs. fine-tuned performance
python src/arogya/models/finetune/evaluate_model.py
```

---

## Cloud Deployment

### Kubernetes

Manifests for all services are in `infra/k8s/`:

```bash
kubectl apply -f infra/k8s/
```

Services: `api-deployment.yaml`, `ui-deployment.yaml`, `worker-deployment.yaml`, `qdrant.yaml`.

### AWS (Terraform)

Infrastructure in `infra/terraform/` provisions:

- **VPC** with public/private subnets across availability zones
- **EKS** cluster + managed node group
- **RDS** PostgreSQL 15 (private subnet)
- **ElastiCache** Redis 7 replication group
- **ECR** repositories for `arogya-api`, `arogya-worker`, `arogya-ui`

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

---

## Demo

See [docs/demo-script.md](docs/demo-script.md) for a full step-by-step walkthrough covering:
- Ingesting a clinical research paper
- Uploading a chest X-ray
- Running the LangGraph multi-agent workflow
- Reviewing the generated report
- Testing via REST API endpoints

---

## Responsible AI

Arogya is a **medical research assistant**, not a diagnostic or clinical decision system.

- Uses only public or de-identified datasets
- All factual claims are citation-backed
- Uncertainty is marked explicitly in every report
- Diagnosis-style language is avoided in the UI
- Verification and guardrail agents are visible by design

---

## References

- [PROJECT_PLAN.md](PROJECT_PLAN.md) — phased roadmap and implementation details
- [omnimind_architecture.svg](omnimind_architecture.svg) — architecture diagram
- [docs/demo-script.md](docs/demo-script.md) — demo walkthrough
