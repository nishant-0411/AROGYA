"""
Orchestrator Graph File

This file connects all our LangGraph agents together (Triage, RAG, Verifier, Report).
It controls the flow of execution from start to finish.
"""

from langgraph.graph import StateGraph, END
from src.arogya.orchestrator.state import AgentState
from src.arogya.agents.triage_agent import triage_node
from src.arogya.agents.rag_agent import rag_node
from src.arogya.agents.verifier_agent import verifier_node
from src.arogya.agents.report_agent import report_node

def route_after_triage(state: AgentState):
    return state.get("route", "report")

def create_workflow():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("triage", triage_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("verifier", verifier_node)
    workflow.add_node("report", report_node)
    
    workflow.set_entry_point("triage")
    
    workflow.add_conditional_edges(
        "triage",
        route_after_triage,
        {
            "rag": "rag",
            "report": "report"
        }
    )
    
    workflow.add_edge("rag", "verifier")
    workflow.add_edge("verifier", "report")
    workflow.add_edge("report", END)
    
    # Compile the graph
    return workflow.compile()

# Global compiled graph
app = create_workflow()

def run_agent_workflow(initial_state: AgentState):
    print(f"Starting LangGraph workflow for query: {initial_state.get('user_query')}")
    final_state = app.invoke(initial_state)
    print("Workflow complete!")
    return final_state
