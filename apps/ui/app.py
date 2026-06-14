import streamlit as st

st.set_page_config(
    page_title="Arogya — Medical Research Assistant",
    page_icon="assets/favicon.png" if False else None,
    layout="wide",
)

# ── Global style ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Warm white background */
    .stApp {
        background-color: #FDFAF7;
        color: #3D2B1F;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F5EDE3;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
        color: #C47E45;
    }

    /* Buttons */
    .stButton > button {
        background-color: #C47E45;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.4rem 1.2rem;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #A8652F;
    }

    /* Primary button override */
    .stButton > button[kind="primary"] {
        background-color: #C47E45;
    }

    /* Divider */
    hr {
        border-color: #E8D5C4;
    }

    /* Page link */
    a {
        color: #C47E45;
    }

    /* Headings */
    h1 { font-weight: 600; color: #3D2B1F; }
    h2 { font-weight: 500; color: #3D2B1F; }
    h3 { font-weight: 500; color: #5A3E2B; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Arogya")
st.caption("Multimodal medical research assistant · OmniMind Architecture")

st.markdown(
    """
    Upload a medical research paper or X-ray, ask a question in natural language,
    and receive a structured answer grounded in retrieved evidence — with citations,
    confidence levels, and verifiable reasoning.
    """
)

st.divider()

# ── Stats ─────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Phases Complete", "8 / 10")
col2.metric("Core Agents", "6")
col3.metric("Source Modules", "8")
col4.metric("Eval Suite", "RAGAS + DeepEval")

st.divider()

# ── Navigation ────────────────────────────────────────────────────────────────
st.subheader("Pages")

nav_col1, nav_col2, _ = st.columns([1, 1, 2])
with nav_col1:
    st.markdown(
        """<a href="/1_query" target="_self"
            style="display:block;padding:0.6rem 1rem;background:#F5EDE3;border:1px solid #E8D5C4;
                   border-radius:6px;color:#3D2B1F;text-decoration:none;font-weight:500;">
            Query Assistant
            <br><small style="font-weight:400;color:#7A6050;">Upload a PDF/image and ask a question</small>
        </a>""",
        unsafe_allow_html=True,
    )
with nav_col2:
    st.markdown(
        """<a href="/3_eval_dashboard" target="_self"
            style="display:block;padding:0.6rem 1rem;background:#F5EDE3;border:1px solid #E8D5C4;
                   border-radius:6px;color:#3D2B1F;text-decoration:none;font-weight:500;">
            Evaluation Dashboard
            <br><small style="font-weight:400;color:#7A6050;">Model comparison, hallucination rates, latency/cost</small>
        </a>""",
        unsafe_allow_html=True,
    )

st.divider()

# ── Architecture ──────────────────────────────────────────────────────────────
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

# ── Roadmap ───────────────────────────────────────────────────────────────────
st.subheader("Roadmap")

phases = [
    ("Done",        "Phase 0", "Repo foundation"),
    ("Done",        "Phase 1", "Multimodal ingestion"),
    ("Done",        "Phase 2", "RAG MVP"),
    ("Done",        "Phase 3", "Multi-agent orchestration"),
    ("Done",        "Phase 4", "Memory & tooling"),
    ("Done",        "Phase 5", "Vision support"),
    ("Done",        "Phase 6", "Fine-tuning pipeline"),
    ("Done",        "Phase 7", "Reliability & evals"),
    ("In progress", "Phase 8", "Production serving"),
    ("Upcoming",    "Phase 9", "Cloud & portfolio polish"),
]

for status, phase, label in phases:
    color = "#C47E45" if status == "In progress" else ("#AAAAAA" if status == "Upcoming" else "#5A8A5A")
    st.markdown(
        f"<span style='color:{color};font-weight:500'>[{status}]</span> "
        f"<strong>{phase}</strong> — {label}",
        unsafe_allow_html=True,
    )

st.divider()
st.caption("Arogya is a medical research assistant, not a diagnostic or clinical decision tool.")
