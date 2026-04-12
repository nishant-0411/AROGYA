"""Creating Local Embedding Models using Huggingface """

from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return model