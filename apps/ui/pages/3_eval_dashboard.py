import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def generate_mock_data() -> pd.DataFrame:
    np.random.seed(42)
    models = ["Baseline RAG", "Finetuned LoRA", "Tool-Enabled Agents"]
    data = []
    for model in models:
        base_perf = 0.6 if model == "Baseline RAG" else (0.8 if model == "Finetuned LoRA" else 0.9)
        for _ in range(50):
            data.append({
                "model": model,
                "retrieval_precision": np.clip(np.random.normal(base_perf, 0.1), 0, 1),
                "faithfulness": np.clip(np.random.normal(base_perf + 0.05, 0.1), 0, 1),
                "answer_relevancy": np.clip(np.random.normal(base_perf, 0.1), 0, 1),
                "citation_coverage": np.clip(np.random.normal(base_perf - 0.1, 0.1), 0, 1),
                "hallucination_rate": np.clip(np.random.normal(1 - base_perf, 0.05), 0, 1),
                "latency_ms": max(100, np.random.normal(1500 if model == "Tool-Enabled Agents" else 800, 200)),
                "cost_usd": max(0.001, np.random.normal(0.05 if model == "Tool-Enabled Agents" else 0.01, 0.005))
            })
    return pd.DataFrame(data)

def render_dashboard() -> None:
    st.set_page_config(page_title="Evaluation Dashboard", page_icon="📊", layout="wide")
    st.title("Evaluation Metrics Dashboard")
    df = generate_mock_data()
    st.sidebar.header("Filters")
    selected_models = st.sidebar.multiselect(
        "Select Models",
        options=df["model"].unique(),
        default=df["model"].unique()
    )
    if not selected_models:
        st.warning("Please select at least one model to view metrics.")
        return
    filtered_df = df[df["model"].isin(selected_models)]
    summary_df = filtered_df.groupby("model").mean(numeric_only=True).reset_index()
    st.header("Overall Performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Faithfulness", f"{summary_df['faithfulness'].mean():.2f}")
    with col2:
        st.metric("Avg Answer Relevancy", f"{summary_df['answer_relevancy'].mean():.2f}")
    with col3:
        st.metric("Avg Hallucination Rate", f"{summary_df['hallucination_rate'].mean():.2%}")
    with col4:
        st.metric("Avg Latency", f"{summary_df['latency_ms'].mean():.0f} ms")
    st.markdown("---")
    st.subheader("Model Comparison")
    metrics = ["retrieval_precision", "faithfulness", "answer_relevancy", "citation_coverage", "hallucination_rate"]
    melted_df = summary_df.melt(id_vars=["model"], value_vars=metrics, var_name="metric", value_name="score")
    fig = px.bar(
        melted_df,
        x="metric",
        y="score",
        color="model",
        barmode="group",
        title="Quality Metrics by Model",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    col_perf1, col_perf2 = st.columns(2)
    with col_perf1:
        st.subheader("Latency vs Cost")
        fig_scatter = px.scatter(
            summary_df,
            x="latency_ms",
            y="cost_usd",
            color="model",
            size="faithfulness",
            title="Latency vs Cost (Size: Faithfulness)",
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col_perf2:
        st.subheader("Hallucination Distribution")
        fig_box = px.box(
            filtered_df,
            x="model",
            y="hallucination_rate",
            color="model",
            title="Hallucination Rate Spread",
            height=400
        )
        st.plotly_chart(fig_box, use_container_width=True)
    st.markdown("---")
    st.subheader("Detailed Run Logs")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    render_dashboard()
