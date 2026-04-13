"""Attach source info"""

def build_citations(docs):
    citations = []

    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        citations.append({
            "text": doc.page_content[:200],
            "source": source
        })

    return citations