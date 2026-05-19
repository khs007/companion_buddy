import time
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.rag.embeddings import get_embedding_model
from app.config import settings


def get_vector_store(collection_name: str) -> Chroma:
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedding_model(),
        persist_directory=settings.chroma_dir
    )


def add_documents_to_store(docs: list[Document], collection_name: str):
    store = get_vector_store(collection_name)
    batch_size = 2
    max_retries = 3

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        batch_num = i // batch_size + 1

        for attempt in range(1, max_retries + 1):
            try:
                print(f"Batch {batch_num} attempt {attempt}")
                store.add_documents(batch)
                print(f"✅ Batch {batch_num} done")
                break
            except Exception as e:
                if attempt == max_retries:
                    raise RuntimeError(f"Failed after {max_retries} attempts: {str(e)}")
                print(f"⏳ Retry in 3s...")
                time.sleep(3)

    print(f"✅ Added {len(docs)} chunks to '{collection_name}'")


def get_retriever(collection_name: str):
    store = get_vector_store(collection_name)
    return store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retrieval_k}
    )