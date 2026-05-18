from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.generate_service import generate_summary, generate_quiz, generate_flashcards
from app.rag.document_processor import get_collection_name

router = APIRouter()


class GenerateRequest(BaseModel):
    filename: str
    num_questions: int = 5
    num_cards: int = 10


@router.post("/summary")
def get_summary(request: GenerateRequest):
    collection = get_collection_name(request.filename)
    try:
        summary = generate_summary(collection)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quiz")
def get_quiz(request: GenerateRequest):
    collection = get_collection_name(request.filename)
    try:
        questions = generate_quiz(collection, request.num_questions)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flashcards")
def get_flashcards(request: GenerateRequest):
    collection = get_collection_name(request.filename)
    try:
        cards = generate_flashcards(collection, request.num_cards)
        return {"flashcards": cards}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))