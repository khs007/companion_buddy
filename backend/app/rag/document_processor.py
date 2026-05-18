import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings


def load_and_chunk_pdf(file_path: str) -> list[Document]:
    """
    Load a PDF and split it into overlapping chunks.
    RecursiveCharacterTextSplitter
    It tries to split on paragraphs first, then sentences, then words.
    This keeps semantically related text together.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    # Load  PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(pages)

    filename = os.path.basename(file_path)
    for chunk in chunks:
        chunk.metadata["source_file"] = filename

    print(f"'{filename}' → {len(pages)} pages → {len(chunks)} chunks")
    return chunks


def get_collection_name(filename: str) -> str:
    """
    Create a clean ChromaDB collection name from filename.
    ChromaDB collection names can't have spaces or special chars.
    """
    name = os.path.splitext(filename)[0]  
    name = name.lower().replace(" ", "_")
    name = "".join(c for c in name if c.isalnum() or c == "_")
    name = name[:50]

    # Remove leading/trailing underscores or hyphens
    name = name.strip("_-")

    return name