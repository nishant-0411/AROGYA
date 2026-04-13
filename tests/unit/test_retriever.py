"""
Unit tests for the retriever module in the Arogya application.
Tests vector store creation, document addition, and retriever generation
using mocking to isolate the logic from real Qdrant and LangChain dependencies.
"""

from unittest.mock import MagicMock, patch
from src.arogya.rag.retriever import create_vectorstore, add_documnents, gen_retriever

def test_create_vectorstore():
    client_mock = MagicMock()
    embeddings_mock = MagicMock()
    collection_name = "test_collection"
    
    with patch('src.arogya.rag.retriever.Qdrant') as MockQdrant:
        vectorstore = create_vectorstore(client_mock, collection_name, embeddings_mock)
        MockQdrant.assert_called_once_with(
            client=client_mock,
            collection_name=collection_name,
            embeddings=embeddings_mock
        )
        assert vectorstore == MockQdrant.return_value

def test_add_documnents():
    vectorstore_mock = MagicMock()
    texts = ["Document 1 text", "Document 2 text"]
    metadatas = [{"source": "source 1"}, {"source": "source 2"}]
    
    with patch('src.arogya.rag.retriever.Document') as MockDocument:
        MockDocument.side_effect = lambda page_content, metadata: MagicMock(page_content=page_content, metadata=metadata)
        add_documnents(vectorstore_mock, texts, metadatas)
        assert vectorstore_mock.add_documents.called
        
def test_gen_retriever():
    vectorstore_mock = MagicMock()
    retriever_mock = MagicMock()
    vectorstore_mock.as_retriever.return_value = retriever_mock
    
    retriever = gen_retriever(vectorstore_mock)
    vectorstore_mock.as_retriever.assert_called_once_with(search_kwargs={"k": 3})
    assert retriever == retriever_mock
