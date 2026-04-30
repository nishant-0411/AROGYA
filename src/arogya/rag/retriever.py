"""Connect to Qdrant and retrieve relevant chunks"""

from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document

def create_vectorstore(client, collection_name, embeddings):
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings
    )
    return vectorstore

def add_documnents(vectorstore, texts, metadata_list=None):
    docs = []

    for i , text in enumerate(texts):
        metadata = metadata_list[i] if metadata_list else {}
        docs.append(Document(page_content=text, metadata = metadata))

    vectorstore.add_documents(docs)

def gen_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})