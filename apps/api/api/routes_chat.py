"""
Chat Routes

FastAPI endpoints for the chat interface.
Triggers the agent orchestrator via LangGraph.
"""

from fastapi import APIRouter
from apps.api.schemas.chat import ChatRequest, ChatResponse
from arogya.orchestrator.graph import run_agent_workflow
from arogya.memory.session_memory import get_session_history
from arogya.memory.patient_case_memory import PatientCaseMemory

router = APIRouter()
case_memory = PatientCaseMemory()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    print(f"Received chat request: {req.message}")
    
    session_id = req.session_id or "default"
    patient_id = req.patient_id or "default_patient"
    
    # Load memories
    history = get_session_history(session_id)
    chat_history_str = [f"{msg.type}: {msg.content}" for msg in history.messages]
    
    case_summary = case_memory.get_case_summary(patient_id)
    
    # Initialize the workflow state for LangGraph
    initial_state = {
        "user_query": req.message,
        "session_id": session_id,
        "patient_id": patient_id,
        "chat_history": chat_history_str,
        "case_summary": case_summary,
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    # Run Orchestrator
    result_state = run_agent_workflow(initial_state)
    
    # Save the interaction to session memory
    history.add_user_message(req.message)
    final_answer = result_state.get("final_report", "No report generated.")
    history.add_ai_message(final_answer)
    
    return ChatResponse(
        answer=final_answer,
        sources=result_state.get("retrieved_docs", [])
    )
