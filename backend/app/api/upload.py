import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config import settings
from app.rag.document_processor import load_and_chunk_pdf, get_collection_name
from app.rag.vector_store import add_documents_to_store

router = APIRouter()


@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Handle PDF upload:
    1. Save file to disk
    2. Extract and chunk text
    3. Store embeddings in ChromaDB
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    save_path = os.path.join(settings.upload_dir, file.filename)

    # Save uploaded file
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process and index the PDF
    try:
        chunks = load_and_chunk_pdf(save_path)
        collection = get_collection_name(file.filename)
        add_documents_to_store(chunks, collection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {
        "message": "PDF uploaded and indexed successfully",
        "filename": file.filename,
        "chunks_indexed": len(chunks),
        "collection": collection
    }


@router.get("/list")
def list_uploaded_files():
    """Return list of all uploaded PDFs."""
    files = [f for f in os.listdir(settings.upload_dir) if f.endswith(".pdf")]
    return {"files": files}