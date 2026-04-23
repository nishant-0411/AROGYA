"""
PubMed Tool

A LangChain tool for searching the PubMed database for medical research articles.
"""

from langchain.tools import tool
from langchain_community.utilities.pubmed import PubMedAPIWrapper

pubmed = PubMedAPIWrapper(top_k_results=3, max_annotations=5)

@tool
def search_pubmed(query: str) -> str:
    try:
        results = pubmed.run(query)
        if not results:
            return "No relevant articles found on PubMed for the given query."
        return results
    except Exception as e:
        return f"Error searching PubMed: {str(e)}"
