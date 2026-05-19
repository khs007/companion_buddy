from langchain_groq import GroqEmbeddings
from app.config import settings

_embedding_model = None

def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not set in .env")
        
        print("Loading Groq embeddings...")
        _embedding_model = GroqEmbeddings(
            model="mixtral-8x7b-32768",
            groq_api_key=settings.groq_api_key,
            timeout=30
        )
        print("✅ Ready")

    return _embedding_model