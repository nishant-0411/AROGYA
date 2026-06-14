"""
Page 1: Document Upload & Query
User uploads PDF/image, types a query, and the agent workflow runs.
"""
import tempfile
import os
import streamlit as st

st.set_page_config(page_title="Arogya — Query", layout="wide")

st.title("Query the Research Assistant")
st.caption("Upload a document and ask a question. The agent pipeline will retrieve evidence and generate a cited answer.")

st.divider()

# ── Inputs ────────────────────────────────────────────────────────────────────
col_upload, col_query = st.columns([1, 1])

with col_upload:
    st.subheader("1. Upload Documents")
    pdf_file = st.file_uploader("Medical paper / PDF", type=["pdf"])
    image_file = st.file_uploader("X-ray / Image (optional)", type=["png", "jpg", "jpeg", "webp"])

with col_query:
    st.subheader("2. Ask a Question")
    query = st.text_area(
        "Your query",
        placeholder="e.g. What are the key findings about lung nodule detection in this paper?",
        height=150,
    )
    run = st.button("Run Analysis", type="primary", disabled=not (pdf_file and query))

st.divider()

# ── Processing ────────────────────────────────────────────────────────────────
if run and pdf_file and query:
    with st.spinner("Running agent pipeline…"):
        try:
            from src.arogya.multimodal.pdf_pipeline import process_pdf
            from src.arogya.orchestrator.graph import run_agent_workflow

            # Save uploaded PDF to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(pdf_file.read())
                pdf_path = tmp_pdf.name

            pdf_doc = process_pdf(pdf_path)
            os.unlink(pdf_path)

            # Save image to a temp path so vision agent can read it
            image_paths: list[str] = []
            if image_file:
                suffix = os.path.splitext(image_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_img:
                    tmp_img.write(image_file.read())
                    image_paths.append(tmp_img.name)

            initial_state = {
                "user_query": query,
                "session_id": "",
                "patient_id": "",
                "image_paths": image_paths,
                "chat_history": [pdf_doc.get("content", "")],
                "case_summary": "",
                "retrieved_docs": [],
                "scratchpad": "",
                "verification_score": 0.0,
                "final_report": "",
                "route": "",
            }

            result = run_agent_workflow(initial_state)

            st.success("Analysis complete!")
            st.subheader("Report")
            st.markdown(result.get("final_report") or "_No report generated._")

            if result.get("verification_score") is not None:
                st.subheader("Verification Score")
                st.metric("Score", f"{result['verification_score']:.2f}")

            if result.get("retrieved_docs"):
                st.subheader("Retrieved Evidence")
                for i, doc in enumerate(result["retrieved_docs"], 1):
                    with st.expander(f"Chunk {i}"):
                        st.write(doc)

            if result.get("scratchpad"):
                with st.expander("Agent Scratchpad"):
                    st.text(result["scratchpad"])

            # Clean up any leftover temp image files
            for p in image_paths:
                if os.path.exists(p):
                    os.unlink(p)

        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.exception(e)

elif not pdf_file:
    st.info("Upload a PDF to get started.")
