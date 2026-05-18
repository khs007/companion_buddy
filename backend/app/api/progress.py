import json
import os
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
PROGRESS_FILE = "progress.json"
def _load_progress() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def _save_progress(data: dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

class QuizResult(BaseModel):
    filename: str
    score: int      
    total: int       
    weak_areas: list[str] = []

@router.post("/quiz-result")
def save_quiz_result(result: QuizResult):
    data = _load_progress()
    entry = {
        "score": result.score,
        "total": result.total,
        "percentage": round((result.score / result.total) * 100, 1),
        "weak_areas": result.weak_areas,
        "timestamp": datetime.now().isoformat()
    }

    if result.filename not in data:
        data[result.filename] = []
    data[result.filename].append(entry)

    _save_progress(data)
    return {"message": "Result saved", "entry": entry}

@router.get("/history/{filename}")
def get_history(filename: str):
    data = _load_progress()
    history = data.get(filename, [])
    return {"filename": filename, "history": history}

@router.get("/summary")
def get_all_progress():
    data = _load_progress()
    summary = {}
    for filename, sessions in data.items():
        if sessions:
            scores = [s["percentage"] for s in sessions]
            summary[filename] = {
                "sessions": len(sessions),
                "avg_score": round(sum(scores) / len(scores), 1),
                "best_score": max(scores),
                "last_studied": sessions[-1]["timestamp"]
            }
    return summary