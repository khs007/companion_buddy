from langchain.chains import RetrievalQA
from app.services.llm_service import get_llm
from app.rag.vector_store import get_retriever
from app.prompts.study_prompts import RAG_CHAT_PROMPT


def answer_question(question: str, collection_name: str) -> dict:
    """
    Core RAG function:
    1. Retrieve relevant chunks from ChromaDB
    2. Feed chunks + question to LLM
    3. Return answer with source info
    """
    llm = get_llm()
    retriever = get_retriever(collection_name)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" = put all chunks into one prompt
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": RAG_CHAT_PROMPT}
    )

    result = qa_chain.invoke({"query": question})

    sources = []
    for doc in result.get("source_documents", []):
        page = doc.metadata.get("page", "?")
        source_file = doc.metadata.get("source_file", "unknown")
        sources.append(f"{source_file} (page {page + 1})")

    return {
        "answer": result["result"],
        "sources": list(set(sources))  # deduplicate
    }