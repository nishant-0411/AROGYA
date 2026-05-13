"""
Integration Test for Chat Flow

Tests the full multi-agent orchestration end-to-end.
"""

from src.arogya.orchestrator.graph import run_agent_workflow
from src.arogya.orchestrator.state import AgentState

def test_chat_workflow_simple_query():
    print("Testing the chat orchestration (Simple Query)...")
    initial_state: AgentState = {
        "user_query": "What is COVID-19?",
        "session_id": "test_session_1",
        "patient_id": "test_patient_1",
        "image_paths": [],
        "chat_history": [],
        "case_summary": "No case data",
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    result = run_agent_workflow(initial_state)
    assert result["route"] == "report"
    assert "Simple query detected" in result["scratchpad"]
    assert "Medical Report" in result["final_report"]

def test_chat_workflow_complex_query():
    print("Testing the chat orchestration (Complex Query)...")
    initial_state: AgentState = {
        "user_query": "Provide a detailed analysis on the side effects of mRNA vaccinations.",
        "session_id": "test_session_2",
        "patient_id": "test_patient_2",
        "image_paths": [],
        "chat_history": [],
        "case_summary": "No case data",
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    result = run_agent_workflow(initial_state)
    assert result["route"] == "rag"
    assert "Complex query detected" in result["scratchpad"]
    assert len(result["retrieved_docs"]) > 0
    assert result["verification_score"] == 0.9
    assert "Context Used" in result["final_report"]
