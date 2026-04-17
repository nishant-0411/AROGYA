"""
Agent State File

This file defines the memory/state object that gets passed around 
between different agents in the graph. It holds the query, docs, and final answer.
"""

class AgentState:
    def __init__(self):
        # what the user asked
        self.user_query = ""
        # docs we pulled from qdrant
        self.retrieved_docs = []
        # notes from the agents as they think
        self.scratchpad = ""
        # whether the verifier thinks it's good or not
        self.verification_score = 0.0
        # the final answer we send back
        self.final_report = ""

    def load_query(self, query):
        self.user_query = query
        
    def add_docs(self, docs):
        self.retrieved_docs.extend(docs)
        
    def get_summary(self):
        # returns a quick summary of the current state
        return {
            "query": self.user_query,
            "docs_found": len(self.retrieved_docs),
            "report_length": len(self.final_report)
        }
