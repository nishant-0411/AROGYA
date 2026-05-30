# Arogya Project Plan

## Suggested File Structure

```text
AROGYA/
├── omnimind_architecture.svg
├── PROJECT_PLAN.md
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── Makefile
├── docker-compose.yml
├── infra/
│   ├── docker/
│   │   ├── api.Dockerfile
│   │   ├── worker.Dockerfile
│   │   └── ui.Dockerfile
│   ├── k8s/
│   │   ├── api-deployment.yaml
│   │   ├── worker-deployment.yaml
│   │   ├── ui-deployment.yaml
│   │   ├── redis.yaml
│   │   └── qdrant.yaml
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── apps/
│   ├── api/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── routes_health.py
│   │   │   ├── routes_chat.py
│   │   │   ├── routes_upload.py
│   │   │   └── routes_reports.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   └── schemas/
│   │       ├── chat.py
│   │       ├── upload.py
│   │       └── report.py
│   ├── ui/
│   │   ├── app.py
│   │   ├── pages/
│   │   │   ├── 1_chat.py
│   │   │   ├── 2_reports.py
│   │   │   └── 3_eval_dashboard.py
│   │   └── components/
│   │       ├── upload_box.py
│   │       ├── citation_card.py
│   │       └── report_viewer.py
│   └── worker/
│       ├── main.py
│       ├── jobs/
│       │   ├── ingest_documents.py
│       │   ├── ingest_images.py
│       │   ├── run_agents.py
│       │   └── generate_report.py
│       └── queues/
│           └── celery_app.py
├── src/
│   └── arogya/
│       ├── orchestrator/
│       │   ├── graph.py
│       │   ├── state.py
│       │   ├── planner.py
│       │   └── policies.py
│       ├── agents/
│       │   ├── triage_agent.py
│       │   ├── rag_agent.py
│       │   ├── vision_agent.py
│       │   ├── verifier_agent.py
│       │   ├── report_agent.py
│       │   └── guardrail_agent.py
│       ├── multimodal/
│       │   ├── image_pipeline.py
│       │   ├── pdf_pipeline.py
│       │   ├── text_pipeline.py
│       │   └── audio_pipeline.py
│       ├── rag/
│       │   ├── chunking.py
│       │   ├── embeddings.py
│       │   ├── retriever.py
│       │   ├── reranker.py
│       │   └── citation_builder.py
│       ├── models/
│       │   ├── llm_gateway.py
│       │   ├── vision_gateway.py
│       │   ├── finetune/
│       │   │   ├── prepare_dataset.py
│       │   │   ├── train_lora.py
│       │   │   ├── merge_adapter.py
│       │   │   └── evaluate_model.py
│       │   └── prompts/
│       │       ├── triage.txt
│       │       ├── verifier.txt
│       │       └── report_writer.txt
│       ├── memory/
│       │   ├── session_memory.py
│       │   ├── patient_case_memory.py
│       │   └── long_term_memory.py
│       ├── tools/
│       │   ├── pubmed_tool.py
│       │   ├── web_search.py
│       │   ├── calculator.py
│       │   └── code_executor.py
│       ├── evals/
│       │   ├── ragas_eval.py
│       │   ├── hallucination_eval.py
│       │   ├── multimodal_eval.py
│       │   └── regression_suite.py
│       └── utils/
│           ├── ids.py
│           ├── io.py
│           └── telemetry.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── curated/
│   ├── embeddings/
│   └── eval/
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_rag_baseline.ipynb
│   ├── 03_vision_baseline.ipynb
│   └── 04_finetune_experiments.ipynb
├── scripts/
│   ├── bootstrap.sh
│   ├── seed_demo_data.py
│   ├── run_local_stack.sh
│   ├── create_qdrant_collections.py
│   └── export_eval_report.py
├── tests/
│   ├── unit/
│   │   ├── test_chunking.py
│   │   ├── test_retriever.py
│   │   ├── test_pdf_pipeline.py
│   │   └── test_agents.py
│   ├── integration/
│   │   ├── test_chat_flow.py
│   │   ├── test_rag_pipeline.py
│   │   └── test_report_generation.py
│   └── evals/
│       ├── test_hallucination_guard.py
│       └── test_medical_case_bench.py
└── docs/
    ├── architecture.md
    ├── adr/
    │   ├── 001-model-choice.md
    │   ├── 002-vector-db-choice.md
    │   └── 003-agent-orchestration.md
    ├── datasets.md
    ├── deployment.md
    └── demo-script.md
```

## Vision

`Arogya` is a production-style multimodal medical research assistant inspired by your `OmniMind` architecture, built heavily on **LangChain** and exclusively utilizing **free, open-source resources**.
It should accept image, PDF, text, and optional audio input; run multiple specialized LangChain agents powered by local models (e.g., via Ollama); use RAG for grounded answers; optionally use a fine-tuned local model for domain adaptation; and return a citation-backed analysis report.

This project is strongest as a portfolio piece when it visibly demonstrates:

- Multimodal ML engineering
- Agent orchestration and memory
- RAG with verification and citations
- Fine-tuning workflow
- Evaluation and hallucination detection
- MLOps deployment and monitoring

## Recommended Tech Stack

### Core platform

- Python `3.11`
- `FastAPI` for backend
- `Streamlit` for demo UI
- `Celery` + `Redis` for background jobs
- `PostgreSQL` for metadata and audit logs
- `Qdrant` for vector search

### LLM and multimodal stack

- `LangChain` for agent orchestration and pipelines
- `transformers`
- `sentence-transformers`
- `peft`
- `trl`
- `bitsandbytes`
- `accelerate`
- `torch`
- `pymupdf`
- `unstructured`
- `pytesseract`
- `Pillow`
- `open_clip_torch` or a free vision-capable local model (e.g. LLaVA via Ollama)
- `openai-whisper` for optional audio transcription

### Retrieval, eval, observability

- `ragas`
- `mlflow`
- `deepeval` or custom eval harness
- `prometheus-client`
- `structlog`

### Testing and quality

- `pytest`
- `pytest-asyncio`
- `httpx`
- `ruff`
- `black`
- `mypy`
- `pre-commit`

## Dependency Plan

Create one main dependency file: [`pyproject.toml`](/Users/nishant/Resume Projects/AROGYA/pyproject.toml)

Use dependency groups instead of many separate requirement files:

- `dev`: linting, tests, notebooks, pre-commit
- `api`: FastAPI, pydantic, uvicorn
- `ui`: Streamlit, plotting, frontend helpers
- `ml`: torch, transformers, peft, trl, sentence-transformers
- `rag`: qdrant-client, rank-bm25, pymupdf, unstructured, pypdf
- `worker`: celery, redis
- `eval`: ragas, deepeval, mlflow

Example package list to install over time:

```text
fastapi
uvicorn[standard]
streamlit
pydantic
pydantic-settings
sqlalchemy
psycopg[binary]
alembic
redis
celery
qdrant-client
langchain
langchain-community
transformers
torch
accelerate
peft
trl
bitsandbytes
sentence-transformers
rank-bm25
pymupdf
unstructured
pypdf
pytesseract
pillow
open_clip_torch
openai-whisper
ragas
mlflow
prometheus-client
structlog
python-multipart
httpx
tenacity
orjson
pytest
pytest-asyncio
ruff
black
mypy
pre-commit
jupyter
```

Do not install everything on day 1. Build in layers.

## Phase-by-Phase Roadmap

## Phase 0 - Repo Foundation

Goal: create a clean project skeleton so every later phase has a place to land.

Create these files first:

- [`README.md`](/Users/nishant/Resume Projects/AROGYA/README.md)
- [`pyproject.toml`](/Users/nishant/Resume Projects/AROGYA/pyproject.toml)
- [`Makefile`](/Users/nishant/Resume Projects/AROGYA/Makefile)
- [`.env.example`](/Users/nishant/Resume Projects/AROGYA/.env.example)
- [`docs/architecture.md`](/Users/nishant/Resume Projects/AROGYA/docs/architecture.md)
- [`apps/api/main.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/main.py)
- [`apps/ui/app.py`](/Users/nishant/Resume Projects/AROGYA/apps/ui/app.py)
- [`tests/unit/test_agents.py`](/Users/nishant/Resume Projects/AROGYA/tests/unit/test_agents.py)

Install now:

- `fastapi`
- `uvicorn[standard]`
- `streamlit`
- `pydantic`
- `pydantic-settings`
- `pytest`
- `ruff`
- `black`
- `mypy`
- `pre-commit`

Deliverables:

- Health endpoint
- Blank Streamlit app
- Basic lint/test pipeline
- Environment config pattern

Exit criteria:

- `make lint` passes
- `make test` passes
- API starts locally
- UI starts locally

## Phase 1 - Multimodal Ingestion Baseline - Done
Goal: accept image, PDF, and text inputs and convert them into normalized internal documents.

Create next:

- [`src/arogya/multimodal/pdf_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/multimodal/pdf_pipeline.py)
- [`src/arogya/multimodal/image_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/multimodal/image_pipeline.py)
- [`src/arogya/multimodal/text_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/multimodal/text_pipeline.py)
- [`apps/api/api/routes_upload.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/api/routes_upload.py)
- [`apps/api/schemas/upload.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/schemas/upload.py)
- [`scripts/seed_demo_data.py`](/Users/nishant/Resume Projects/AROGYA/scripts/seed_demo_data.py)
- [`tests/unit/test_pdf_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/tests/unit/test_pdf_pipeline.py)

Install in this phase:

- `pymupdf`
- `pypdf`
- `unstructured`
- `pytesseract`
- `pillow`
- `python-multipart`

Work items:

- Parse research-paper PDFs
- OCR image-based pages when needed
- Normalize extracted text into a shared `DocumentChunk` schema
- Store raw and processed artifacts under `data/`

Exit criteria:

- Upload endpoint accepts PDF and image files
- Parsed content is saved in a normalized form
- At least 3 sample medical papers can be ingested end to end

## Phase 2 - RAG MVP

Goal: build grounded retrieval before adding agent complexity.

Create next:

- [`src/arogya/rag/chunking.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/chunking.py)
- [`src/arogya/rag/embeddings.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/embeddings.py)
- [`src/arogya/rag/retriever.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/retriever.py)
- [`src/arogya/rag/citation_builder.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/citation_builder.py)
- [`scripts/create_qdrant_collections.py`](/Users/nishant/Resume Projects/AROGYA/scripts/create_qdrant_collections.py)
- [`tests/unit/test_chunking.py`](/Users/nishant/Resume Projects/AROGYA/tests/unit/test_chunking.py)
- [`tests/unit/test_retriever.py`](/Users/nishant/Resume Projects/AROGYA/tests/unit/test_retriever.py)

Install in this phase:

- `qdrant-client`
- `sentence-transformers`
- `rank-bm25`
- `numpy`

Work items:

- Implement chunking for papers, reports, and notes
- Build hybrid retrieval: dense + keyword
- Add citation metadata with source page numbers
- Keep retrieval deterministic enough for testing

Exit criteria:

- Query returns top relevant chunks with citations
- At least one benchmark notebook shows useful retrieval quality
- Citation traces appear in the response JSON

## Phase 3 - Agent Orchestration MVP

Goal: turn the RAG system into a multi-agent workflow.

Create next:

- [`src/arogya/orchestrator/graph.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/orchestrator/graph.py)
- [`src/arogya/orchestrator/state.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/orchestrator/state.py)
- [`src/arogya/agents/triage_agent.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/agents/triage_agent.py)
- [`src/arogya/agents/rag_agent.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/agents/rag_agent.py)
- [`src/arogya/agents/verifier_agent.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/agents/verifier_agent.py)
- [`src/arogya/agents/report_agent.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/agents/report_agent.py)
- [`apps/api/api/routes_chat.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/api/routes_chat.py)
- [`apps/api/schemas/chat.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/schemas/chat.py)
- [`tests/integration/test_chat_flow.py`](/Users/nishant/Resume Projects/AROGYA/tests/integration/test_chat_flow.py)

Install in this phase:

- `langchain`
- `langchain-community`
- `httpx`
- `tenacity`

Agent layout:

- `Triage Agent`: understands query type and routes the workflow
- `RAG Agent`: retrieves evidence from indexed knowledge
- `Vision Agent`: interprets X-ray or medical image inputs later
- `Verifier Agent`: checks claims against evidence
- `Report Agent`: writes the final structured answer

Exit criteria:

- One request can trigger multiple agents
- Final answer contains evidence and confidence notes
- Agent state is logged for debugging

## Phase 4 - Memory and Tooling

Goal: make the system more realistic and less stateless.

Create next:

- [`src/arogya/memory/session_memory.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/memory/session_memory.py)
- [`src/arogya/memory/patient_case_memory.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/memory/patient_case_memory.py)
- [`src/arogya/tools/pubmed_tool.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/tools/pubmed_tool.py)
- [`src/arogya/tools/web_search.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/tools/web_search.py)
- [`src/arogya/tools/calculator.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/tools/calculator.py)
- [`docs/adr/003-agent-orchestration.md`](/Users/nishant/Resume Projects/AROGYA/docs/adr/003-agent-orchestration.md)

Install in this phase:

- `redis`
- `sqlalchemy`
- `psycopg[binary]`
- `alembic`

Work items:

- Add session-level chat memory (LangChain native)
- Add persistent case memory
- Add PubMed or curated-research free tool
- Keep external web search optional and clearly labeled (DuckDuckGo)

Exit criteria:

- Sessions can continue across turns
- Evidence source type is visible: internal RAG vs external tool
- Memory can be cleared for privacy-sensitive demos

## Phase 5 - Vision and Multimodal Expansion

Goal: support image-based medical reasoning such as X-ray review assistance.

Create next:

- [`src/arogya/agents/vision_agent.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/agents/vision_agent.py)
- [`src/arogya/models/vision_gateway.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/models/vision_gateway.py)
- [`src/arogya/evals/multimodal_eval.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/evals/multimodal_eval.py)
- [`tests/integration/test_rag_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/tests/integration/test_rag_pipeline.py)

Install in this phase:

- `torch`
- `transformers`
- `open_clip_torch`
- `opencv-python` if needed

Work items:

- Accept image uploads alongside text query
- Extract visual features or call a vision-capable model
- Feed vision findings into report generation, never as a hidden opaque answer

Important note:

- Keep medical-image outputs framed as research support, not diagnosis

Exit criteria:

- Demo accepts X-ray plus text query
- Report clearly separates image findings from retrieved literature evidence

## Phase 6 - Fine-Tuning Pipeline

Goal: demonstrate ML engineering depth with domain adaptation.

Create next:

- [`src/arogya/models/finetune/prepare_dataset.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/models/finetune/prepare_dataset.py)
- [`src/arogya/models/finetune/train_lora.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/models/finetune/train_lora.py)
- [`src/arogya/models/finetune/merge_adapter.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/models/finetune/merge_adapter.py)
- [`src/arogya/models/finetune/evaluate_model.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/models/finetune/evaluate_model.py)
- [`docs/datasets.md`](/Users/nishant/Resume Projects/AROGYA/docs/datasets.md)
- [`notebooks/04_finetune_experiments.ipynb`](/Users/nishant/Resume Projects/AROGYA/notebooks/04_finetune_experiments.ipynb)

Install in this phase:

- `transformers`
- `datasets`
- `peft`
- `trl`
- `accelerate`
- `bitsandbytes`
- `mlflow`

Suggested fine-tune target:

- Start with a small instruction-tuned open-source model (e.g. Llama-3 8B, Mistral) locally and train LoRA adapters on medical summarization, evidence-grounded QA, or report formatting tasks

Do not fine-tune first.
First prove that the RAG baseline works.

Exit criteria:

- Reproducible training script exists
- Dataset preparation is documented
- Before/after eval shows what improved and what did not

## Phase 7 - Hallucination Detection and Evaluation

Goal: prove reliability, not just demo quality.

Create next:

- [`src/arogya/evals/ragas_eval.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/evals/ragas_eval.py)
- [`src/arogya/evals/hallucination_eval.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/evals/hallucination_eval.py)
- [`src/arogya/evals/regression_suite.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/evals/regression_suite.py)
- [`tests/evals/test_hallucination_guard.py`](/Users/nishant/Resume Projects/AROGYA/tests/evals/test_hallucination_guard.py)
- [`tests/evals/test_medical_case_bench.py`](/Users/nishant/Resume Projects/AROGYA/tests/evals/test_medical_case_bench.py)
- [`apps/ui/pages/3_eval_dashboard.py`](/Users/nishant/Resume Projects/AROGYA/apps/ui/pages/3_eval_dashboard.py)

Install in this phase:

- `ragas`
- `deepeval`
- `pandas`
- `plotly`

Metrics to track:

- Retrieval precision
- Faithfulness
- Answer relevancy
- Citation coverage
- Hallucination rate
- Latency per agent
- Cost per request

Exit criteria:

- Repeatable evaluation suite exists
- You can compare baseline vs finetuned vs tool-enabled versions
- One dashboard summarizes quality and latency

## Phase 8 - Production Serving and Async Jobs

Goal: move from notebook/demo project to system design project.

Create next:

- [`apps/worker/main.py`](/Users/nishant/Resume Projects/AROGYA/apps/worker/main.py)
- [`apps/worker/queues/celery_app.py`](/Users/nishant/Resume Projects/AROGYA/apps/worker/queues/celery_app.py)
- [`apps/worker/jobs/ingest_documents.py`](/Users/nishant/Resume Projects/AROGYA/apps/worker/jobs/ingest_documents.py)
- [`apps/worker/jobs/run_agents.py`](/Users/nishant/Resume Projects/AROGYA/apps/worker/jobs/run_agents.py)
- [`apps/worker/jobs/generate_report.py`](/Users/nishant/Resume Projects/AROGYA/apps/worker/jobs/generate_report.py)
- [`docker-compose.yml`](/Users/nishant/Resume Projects/AROGYA/docker-compose.yml)
- [`infra/docker/api.Dockerfile`](/Users/nishant/Resume Projects/AROGYA/infra/docker/api.Dockerfile)
- [`infra/docker/worker.Dockerfile`](/Users/nishant/Resume Projects/AROGYA/infra/docker/worker.Dockerfile)
- [`infra/docker/ui.Dockerfile`](/Users/nishant/Resume Projects/AROGYA/infra/docker/ui.Dockerfile)

Install in this phase:

- `celery`
- `redis`
- `orjson`

Work items:

- Run heavy jobs asynchronously
- Support report polling or WebSocket updates
- Containerize API, worker, UI, vector DB, and Redis

Exit criteria:

- Large PDF/image processing does not block the API
- Local docker stack starts successfully
- End-to-end demo is reproducible

## Phase 9 - Cloud, Monitoring, and Portfolio Polish

Goal: package the project like a serious production system.

Create next:

- [`infra/k8s/api-deployment.yaml`](/Users/nishant/Resume Projects/AROGYA/infra/k8s/api-deployment.yaml)
- [`infra/k8s/worker-deployment.yaml`](/Users/nishant/Resume Projects/AROGYA/infra/k8s/worker-deployment.yaml)
- [`infra/k8s/ui-deployment.yaml`](/Users/nishant/Resume Projects/AROGYA/infra/k8s/ui-deployment.yaml)
- [`infra/terraform/main.tf`](/Users/nishant/Resume Projects/AROGYA/infra/terraform/main.tf)
- [`docs/deployment.md`](/Users/nishant/Resume Projects/AROGYA/docs/deployment.md)
- [`docs/demo-script.md`](/Users/nishant/Resume Projects/AROGYA/docs/demo-script.md)

Install in this phase:

- `prometheus-client`
- cloud SDKs only if actually needed

Work items:

- Add tracing and metrics
- Add deployment docs for AWS, GCP, or Hugging Face
- Record one polished walkthrough demo
- Prepare interview-ready architecture explanation

Exit criteria:

- Live or semi-live hosted demo exists
- Monitoring and logs are visible
- README has screenshots, architecture, setup, and demo flow

## Build Order Summary

Follow this order:

1. Repo skeleton
2. PDF and image ingestion
3. RAG baseline
4. Agent orchestration
5. Memory and tools
6. Vision support
7. Fine-tuning
8. Evaluation
9. Async serving and Docker
10. Cloud deployment and portfolio polish

This order matters because:

- RAG before fine-tuning gives you a real baseline
- Agents before memory keeps debugging simpler
- Evaluation before hosting prevents a fake-looking demo

## Minimal First Milestone

If you want the smartest first milestone, build only this:

- Upload one medical research PDF
- Ask a question in chat
- Retrieve relevant chunks with citations
- Generate a structured answer
- Show sources in the UI

That alone is already a very strong portfolio checkpoint.

## Suggested Report Format

Your final generated report should eventually have these sections:

- User query
- Input summary
- Retrieved evidence
- Image findings if present
- Cross-check and verification notes
- Final synthesized answer
- Confidence level
- Limitations and disclaimer
- Citations

## Risks to Handle Early

- Medical hallucinations or overconfident phrasing
- Poor OCR quality in scanned PDFs
- Weak citation formatting
- Fine-tuning on low-quality datasets
- Slow multimodal pipelines
- Privacy issues if real patient data is ever used

## Recommended Rules for This Project

- Use only de-identified public datasets
- Always show citations for factual claims
- Mark unsupported claims explicitly
- Keep diagnosis-style wording out of the UI
- Treat this as a research assistant, not a clinical system

## What To Create Right After This File


Start with these 8 files immediately:

1. [`README.md`](/Users/nishant/Resume Projects/AROGYA/README.md)
2. [`pyproject.toml`](/Users/nishant/Resume Projects/AROGYA/pyproject.toml)
3. [`.env.example`](/Users/nishant/Resume Projects/AROGYA/.env.example)
4. [`Makefile`](/Users/nishant/Resume Projects/AROGYA/Makefile)
5. [`apps/api/main.py`](/Users/nishant/Resume Projects/AROGYA/apps/api/main.py)
6. [`apps/ui/app.py`](/Users/nishant/Resume Projects/AROGYA/apps/ui/app.py)
7. [`src/arogya/rag/chunking.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/rag/chunking.py)
8. [`src/arogya/multimodal/pdf_pipeline.py`](/Users/nishant/Resume Projects/AROGYA/src/arogya/multimodal/pdf_pipeline.py)

## Interview Value

This project can honestly showcase:

- System design for multi-agent AI
- Practical RAG architecture
- Fine-tuning workflow design
- Evaluation discipline
- Production deployment thinking
- Responsible AI guardrails in a high-stakes domain

If built phase by phase, this becomes much more impressive than a single-shot chatbot clone.