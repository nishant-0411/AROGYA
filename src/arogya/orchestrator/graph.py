"""
Orchestrator Graph File

This file connects all our agents together (Triage, RAG, Verifier, Report).
It controls the flow of execution from start to finish.
"""

def create_workflow_graph():
    print("Building the multi-agent graph map...")
    
    workflow_map = {
        "start": "triage",
        "triage_logic": "if simple -> report, if complex -> rag",
        "rag": "verifier",
        "verifier": "report",
        "report": "end"
    }
    
    return workflow_map

def run_agent_workflow(user_query, state_obj):
    print(f"Starting workflow for query: {user_query}")
    graph = create_workflow_graph()
    
    # pretend we run through the nodes
    print("Running Triage Agent...")
    print("Running RAG Agent...")
    print("Running Verifier Agent...")
    print("Running Report Agent...")
    
    state_obj.final_report = "This is a fake medical report from our prototype."
    print("Workflow complete!")
    
    return state_obj
