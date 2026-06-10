import streamlit as st

st.set_page_config(
    page_title="Arogya — Medical Research Assistant",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Arogya")
st.caption("Production-style multimodal medical research assistant · OmniMind Architecture")

st.markdown(
    """
    Upload a medical research paper or X-ray, ask a question in natural language,
    and receive a structured answer grounded in retrieved evidence — with citations,
    confidence levels, and verifiable reasoning.
    """
)

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Phases Complete", "8 / 10")
col2.metric("Core Agents", "6")
col3.metric("Source Modules", "8")
col4.metric("Eval Suite", "RAGAS + DeepEval")

st.divider()

st.subheader("Pages")
st.page_link("pages/1_query.py",          label="🔍 Query Assistant",       help="Upload a PDF/image and ask a question")
st.page_link("pages/3_eval_dashboard.py", label="📊 Evaluation Dashboard",  help="Model comparison, hallucination rates, latency/cost charts")

st.divider()

st.subheader("Architecture — 4 Layers")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("**Input**")
    st.markdown("Text · PDF · Image · Audio")
with c2:
    st.markdown("**Agents**")
    st.markdown("Triage · RAG · Vision · Verifier · Report · Guardrail")
with c3:
    st.markdown("**Intelligence**")
    st.markdown("LangGraph · Memory · Qdrant · PubMed · Ollama")
with c4:
    st.markdown("**Serving**")
    st.markdown("FastAPI · Streamlit · Celery · Docker")

st.divider()

st.subheader("Roadmap")

phases = [
    ("✅", "Phase 0", "Repo foundation"),
    ("✅", "Phase 1", "Multimodal ingestion"),
    ("✅", "Phase 2", "RAG MVP"),
    ("✅", "Phase 3", "Multi-agent orchestration"),
    ("✅", "Phase 4", "Memory & tooling"),
    ("✅", "Phase 5", "Vision support"),
    ("✅", "Phase 6", "Fine-tuning pipeline"),
    ("✅", "Phase 7", "Reliability & evals"),
    ("⚡", "Phase 8", "Production serving — in progress"),
    ("🔲", "Phase 9", "Cloud & portfolio polish"),
]

for icon, phase, label in phases:
    st.markdown(f"{icon} **{phase}** — {label}")

st.divider()
st.caption("⚕️ Arogya is a medical research assistant, not a diagnostic or clinical decision tool.")
