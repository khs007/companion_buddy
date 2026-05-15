from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings

_embedding_model = None

def get_embedding_model() -> HuggingFaceEmbeddings:
    global _embedding_model

    if _embedding_model is None:
        print(f"Loading embedding model: {settings.embedding_model}")
        _embedding_model = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},  
            encode_kwargs={"normalize_embeddings": True}
        )
        print("Embedding model loaded.")

    return _embedding_model