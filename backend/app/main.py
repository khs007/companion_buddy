import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload, chat, generate, progress
from app.config import settings

app = FastAPI(
    title="AI Study Companion",
    description="RAG-powered study assistant for students",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(generate.router, prefix="/generate", tags=["Generate"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])

@app.on_event("startup")
async def startup():
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.chroma_dir, exist_ok=True)
    print("Study Companion API is running!")

@app.get("/")
def root():
    return {"message": "Study Companion API", "status": "running"}