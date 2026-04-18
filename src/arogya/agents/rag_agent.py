"""
RAG Agent

Retrieves information from our Qdrant vector DB based on user query.
"""

from src.arogya.orchestrator.state import AgentState

def rag_node(state: AgentState):
    query = state.get("user_query", "")

    # Mock retrieval setup (to be hooked up with Qdrant)
    docs = [
        f"Relevant medical info about: {query}",  # Basic
        "Additional clinical guidelines..."
    ]

    return {
        "retrieved_docs": docs,
        "scratchpad": "\n[RAG] Retrieved documents"
    }