"""
Integration Test for Chat Flow

Tests the full multi-agent orchestration end-to-end.
"""

from src.arogya.orchestrator.graph import run_agent_workflow

def test_chat_workflow_simple_query():
    print("Testing the chat orchestration (Simple Query)...")
    initial_state = {
        "user_query": "What is COVID-19?",
        "session_id": "test_session_1",
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    result = run_agent_workflow(initial_state)
    assert result.get("route") == "report"
    assert "Simple query detected" in result.get("scratchpad")
    assert "Medical Report" in result.get("final_report")

def test_chat_workflow_complex_query():
    print("Testing the chat orchestration (Complex Query)...")
    initial_state = {
        "user_query": "Provide a detailed analysis on the side effects of mRNA vaccinations.",
        "session_id": "test_session_2",
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    result = run_agent_workflow(initial_state)
    assert result.get("route") == "rag"
    assert "Complex query detected" in result.get("scratchpad")
    assert len(result.get("retrieved_docs")) > 0
    assert result.get("verification_score") == 0.9
    assert "Context Used" in result.get("final_report")
