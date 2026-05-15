from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.rag.embeddings import get_embedding_model
from app.config import settings


def get_vector_store(collection_name: str) -> Chroma:
    """Load or create a ChromaDB collection for a specific document."""
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedding_model(),
        persist_directory=settings.chroma_dir
    )


def add_documents_to_store(docs: list[Document], collection_name: str):
    """Add chunked documents into the vector store."""
    store = get_vector_store(collection_name)
    store.add_documents(docs)
    print(f"Added {len(docs)} chunks to collection '{collection_name}'")


def get_retriever(collection_name: str):
    """Return a retriever that fetches top-k relevant chunks."""
    store = get_vector_store(collection_name)
    return store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retrieval_k}
    )