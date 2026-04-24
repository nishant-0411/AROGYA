"""
Web Search Tool

A LangChain tool for performing general web searches using DuckDuckGo.
This tool is used as an optional external fallback when internal medical knowledge
or PubMed do not provide sufficient information.
"""

from langchain.tools import tool
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

ddg_search = DuckDuckGoSearchAPIWrapper(max_results=3)

@tool
def search_web(query: str) -> str:
    """
    Search the web for general information using DuckDuckGo.
    Use this tool ONLY when you need information that is not available in the internal 
    medical knowledge base (RAG) or PubMed.
    Always clearly label information retrieved from this tool as coming from an 'External Web Search'.
    """
    try:
        results = ddg_search.run(query)
        if not results:
            return "No relevant results found on the web for the given query."
        return results
    except Exception as e:
        return f"Error searching the web: {str(e)}"
