from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import answer_question
from app.rag.document_processor import get_collection_name

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    filename: str  # which document to query against


@router.post("/ask")
def ask_question(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    collection = get_collection_name(request.filename)

    try:
        result = answer_question(request.question, collection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return result