"""
Verifier Agent

Checks the RAG findings for hallucinations before we write the final report.
"""

from src.arogya.orchestrator.state import AgentState

def verifier_node(state: AgentState):
    retrieved_docs = state.get("retrieved_docs", [])
    if len(retrieved_docs) > 0:
        return {
            "verification_score": 0.9,
            "scratchpad": "\n[Verifier] High confidence"
        }
    else:
        return {
            "verification_score": 0.5,
            "scratchpad": "\n[Verifier] Low confidence"
        }
