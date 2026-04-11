"""
Core RAG query logic for the chat endpoint.
Uses shared services for vectorstore and LLM access.
"""

from ..services import get_vectorstore, get_llm


def answer_query(query: str, top_k: int, role: str):
    """
    Core RAG logic (framework independent)
    """

    docs = get_vectorstore().similarity_search(
        query=query,
        k=top_k,
        filter={"role": role}
    )

    if not docs:
        return {
            "answer": "No relevant medical documents found.",
            "sources": []
        }

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are a medical assistant.

Answer strictly using the context below.
If the answer is not present, say:
"I don't have enough medical information to answer this."

Context:
{context}

Question:
{query}
"""

    answer = get_llm().invoke(prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "source": d.metadata.get("source"),
                "page": d.metadata.get("page"),
                "doc_id": d.metadata.get("doc_id")
            }
            for d in docs
        ]
    }
