from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.config import settings


def get_llm():
    """
    Return the configured LLM instance.
    
    Groq  — it's free and very fast.
    Switch to Gemini for production or need longer context.
    """
    if settings.llm_provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # lower = more factual, higher = more creative
            convert_system_message_to_human=True
        )

    elif settings.llm_provider == "groq":
        return ChatGroq(
            model_name=settings.groq_model,
            groq_api_key=settings.groq_api_key,
            temperature=0.3
        )

    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")