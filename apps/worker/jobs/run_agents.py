from apps.worker.queues.celery_app import celery_app
from src.arogya.orchestrator.graph import run_agent_workflow
from src.arogya.orchestrator.state import AgentState

@celery_app.task(name="apps.worker.jobs.run_agents")
def run_agents_task(payload: dict):
    initial_state = AgentState(
        user_query=payload.get("user_query", ""),
        session_id=payload.get("session_id", ""),
        patient_id=payload.get("patient_id", ""),
        image_paths=payload.get("image_paths", []),
        chat_history=payload.get("chat_history", []),
        case_summary=payload.get("case_summary", ""),
        retrieved_docs=payload.get("retrieved_docs", []),
        scratchpad=payload.get("scratchpad", ""),
        verification_score=payload.get("verification_score", 0.0),
        final_report=payload.get("final_report", ""),
        route=payload.get("route", "")
    )
    
    final_state = run_agent_workflow(initial_state)
    
    return {
        "status": "success",
        "final_state": final_state
    }
