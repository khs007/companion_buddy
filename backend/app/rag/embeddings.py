from langchain_community.embeddings import JinaEmbeddings
from app.config import settings

_embedding_model = None

def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        if not settings.jina_api_key or settings.jina_api_key == "":
            raise ValueError(
                f"JINA_API_KEY is empty. Current value: '{settings.jina_api_key}'. "
                "Check your .env file in backend/"
            )
        
        print("Loading Jina embeddings...")
        _embedding_model = JinaEmbeddings(
            model_name="jina-embeddings-v2-base-en",
            api_key=settings.jina_api_key
        )
        print("✅ Jina embeddings ready")

    return _embedding_model