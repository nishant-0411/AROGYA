"""
Triage Agent

First agent in the chain. Decides what kind of query the user is asking.
"""

from src.arogya.orchestrator.state import AgentState

def triage_node(state: AgentState):
    query = state.get("user_query", "").lower()

    if any(word in query for word in ["what", "define", "explain"]): #Basic
        return {
            "scratchpad": "\n[Triage] Simple query detected",
            "route": "report"
        }
    else:
        return {
            "scratchpad": "\n[Triage] Complex query detected",
            "route": "rag"
        }