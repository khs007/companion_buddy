import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.services.llm_service import get_llm
from app.rag.vector_store import get_vector_store
from app.prompts.study_prompts import (
    SUMMARY_PROMPT, QUIZ_PROMPT, FLASHCARD_PROMPT
)

def _get_full_text(collection_name: str, max_chunks: int = 20) -> str:
    """Fetch text from ChromaDB for summarization/generation tasks."""
    store = get_vector_store(collection_name)
    results = store.get()
    documents = results.get("documents", [])[:max_chunks]

    return "\n\n".join(documents)

def _parse_json_response(raw: str) -> list:
    """Safely parse JSON from LLM output, handling common formatting issues."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw output: {raw[:300]}")


def generate_summary(collection_name: str) -> str:
    """Generate a structured summary of the uploaded document."""
    text = _get_full_text(collection_name)
    if not text:
        raise ValueError("No content found in this document.")
    llm = get_llm()
    chain = SUMMARY_PROMPT | llm | StrOutputParser()
    return chain.invoke({"text": text[:8000]})  # limit to avoid token overflow

def generate_quiz(collection_name: str, num_questions: int = 5) -> list:
    """Generate multiple-choice quiz questions from the document."""
    text = _get_full_text(collection_name)
    if not text:
        raise ValueError("No content found in this document.")

    llm = get_llm()
    chain = QUIZ_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({"text": text[:6000], "num_questions": num_questions})
    return _parse_json_response(raw)

def generate_flashcards(collection_name: str, num_cards: int = 10) -> list:
    """Generate flashcards (term → definition) from the document."""
    text = _get_full_text(collection_name)
    if not text:
        raise ValueError("No content found in this document.")
    llm = get_llm()
    chain = FLASHCARD_PROMPT | llm | StrOutputParser()
    raw = chain.invoke({"text": text[:6000], "num_cards": num_cards})
    return _parse_json_response(raw)