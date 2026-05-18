from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        print("Loading Gemini embedding model...")

        _embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"   ,
            google_api_key=settings.google_api_key
        )

        print("Gemini embedding model ready.")

    return _embedding_model