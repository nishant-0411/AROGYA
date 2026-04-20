"""
Agent State File

Defines the state structure used by LangGraph.
"""

from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    """
    Represents the state of our agent workflow.
    """
    user_query: str
    session_id: str
    retrieved_docs: Annotated[List[str], operator.add]
    scratchpad: Annotated[str, operator.add]
    verification_score: float
    final_report: str
    route: str
