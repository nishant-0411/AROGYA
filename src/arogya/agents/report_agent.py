"""
Report Agent

Generates final response.
"""

from src.arogya.orchestrator.state import AgentState

def report_node(state: AgentState):
    query = state.get("user_query", "")
    retrieved_docs = state.get("retrieved_docs", [])

    if retrieved_docs:
        context = "\n".join(retrieved_docs)
        final_report = f"""Medical Report:

Query: {query}

Context Used:
{context}

Answer:
Based on retrieved medical knowledge, this is a structured response.
"""
    else:
        final_report = f"""Medical Report:

Query: {query}

Answer:
This is a general response without retrieval.
"""

    return {
        "final_report": final_report,
        "scratchpad": "\n[Report] Final answer generated"
    }