"""
Chat Routes

FastAPI endpoints for the chat interface.
Triggers the agent orchestrator via LangGraph.
"""

from fastapi import APIRouter
from ...schemas.chat import ChatRequest, ChatResponse
from arogya.orchestrator.graph import run_agent_workflow

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    print(f"Received chat request: {req.message}")
    
    # Initialize the workflow state for LangGraph
    initial_state = {
        "user_query": req.message,
        "session_id": req.session_id or "default",
        "retrieved_docs": [],
        "scratchpad": "",
        "verification_score": 0.0,
        "final_report": "",
        "route": ""
    }
    
    # Run Orchestrator
    result_state = run_agent_workflow(initial_state)
    
    return ChatResponse(
        answer=result_state.get("final_report", "No report generated."),
        sources=result_state.get("retrieved_docs", [])
    )
