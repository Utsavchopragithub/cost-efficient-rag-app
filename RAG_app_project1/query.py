import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from embeddings import get_vectorstore

load_dotenv()

def query_rag(question: str, k: int = 4, category_filter: str = None):
    start_time = time.time()
    db = get_vectorstore()
    
    search_kwargs = {"k": k}
    if category_filter:
        search_kwargs["filter"] = {"category": category_filter}
        
    results = db.similarity_search_with_score(question, **search_kwargs)
    
    if not results:
        return {
            "answer": "No relevant context found in the knowledge base.",
            "sources": [],
            "latency_sec": round(time.time() - start_time, 3)
        }
    
    context_str = "\n\n".join([doc.page_content for doc, _ in results])
    sources = [doc.metadata.get("source", "unknown") for doc, _ in results]
    
    # Updated Prompt for Detailed & Well-Explained Answers
    prompt = f"""You are an expert AI assistant. Answer the user's question clearly and thoroughly using ONLY the provided context.

Context:
{context_str}

Question: {question}

Instructions:
1. Provide a comprehensive, detailed, and clear answer based on the context.
2. Use bullet points or numbered lists where appropriate for readability.
3. If the context does not contain enough information, state: "I do not know based on the provided context."

Answer:"""

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2  # Slightly higher for fluent and natural explanation
    )
    
    response = llm.invoke(prompt)
    
    return {
        "answer": response.content,
        "sources": list(set(sources)),
        "latency_sec": round(time.time() - start_time, 3)
    }