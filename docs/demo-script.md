# Arogya Demo Script

This script guide walks through presenting and demonstrating the Arogya medical research assistant. It showcases the integration of multimodal inputs, multi-agent orchestration, citation-backed RAG, session memory, fine-tuning validation, and system evaluation.

---

## 1. Demo Scenario Overview

We demonstrate the system using a clinical research scenario:
* **Upload:** A clinical research paper on Pulmonary Embolism (PDF format).
* **Upload:** A patient chest X-ray image (PNG format).
* **User Query:** "Analyze this X-ray and report if there are findings consistent with the uploaded literature."
* **Result:** A structured, verified report containing visual findings, retrieved literature evidence, claim verification, confidence scores, and limitations.

---

## 2. Infrastructure and Setup

Ensure local environment and Ollama services are running.

```bash
ollama serve
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
make run-api
```

```bash
make run-ui
```

---

## 3. Step-by-Step Walkthrough

### Part 1: Ingestion of Medical Literature
1. Navigate to the Streamlit UI dashboard.
2. Go to the Document Upload section.
3. Upload the research paper PDF.
4. The system parses the document, chunks the text, computes embeddings, and stores them in the Qdrant database.

### Part 2: Uploading Patient Image
1. Upload the patient chest X-ray image in the Multimodal input widget.
2. The UI prepares the image paths array for the request payload.

### Part 3: Executing the LangGraph Multi-Agent Workflow
1. Input the query in the chat input.
2. Submit the query to start the orchestration flow.
3. The UI displays the execution trace of the specialized agents:
   * **Triage Agent:** Detects the chest X-ray image and routes the state to the Vision Agent.
   * **Vision Agent:** Analyzes the X-ray using the Vision model gateway and extracts findings.
   * **RAG Agent:** Queries Qdrant to retrieve relevant passages about pulmonary embolism and radiological findings.
   * **Verifier Agent:** Evaluates the retrieved documents and images, validating claims to check for potential hallucinations.
   * **Report Agent:** Synthesizes the final report using the structured format.

### Part 4: Reviewing the Generated Report
1. Verify the layout of the final report containing:
   * Summarized input.
   * Visual findings.
   * Retrieved literature evidence.
   * Verification score and guardrail notes.
   * Confidence level and medical disclaimers.
   * Inline source citations.

---

## 4. REST API Verification

The backend workflows can also be demonstrated using API endpoints.

### File Upload Endpoint

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/paper.pdf"
```

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/xray.png"
```

### Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare the chest X-ray findings with the uploaded pulmonary embolism paper", "session_id": "demo-session", "patient_id": "patient-101"}'
```

---

## 5. Fine-Tuning and Model Evals

Demonstrate the model customisation and validation pipeline:

1. Prepare the medical instruction dataset:
```bash
python src/arogya/models/finetune/prepare_dataset.py --demo
```

2. Execute the evaluation suite to compare base model vs fine-tuned adapter performance:
```bash
python src/arogya/models/finetune/evaluate_model.py
```

3. Open the evaluation dashboard page in Streamlit to view retrieval precision, faithfulness, and answer relevancy metrics.
