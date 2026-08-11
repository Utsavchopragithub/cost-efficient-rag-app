# 🤖 Cost-Efficient RAG System with Streamlit UI

A lightweight, production-ready Retrieval-Augmented Generation (RAG) system built with **LangChain**, **ChromaDB**, **Groq API** (`llama-3.1-8b-instant`), and **Streamlit**.

---

## 📐 System Architecture & Data Flow

Below is the architectural workflow of how documents are ingested and queried in this RAG system:

```mermaid
flowchart TD
    subgraph Ingestion_Pipeline ["1. Ingestion Pipeline"]
        A[User Uploads PDF/TXT Document] --> B[Text Splitter: RecursiveCharacterTextSplitter]
        B --> C[Generate Embeddings: HuggingFace all-MiniLM-L6-v2]
        C --> D[(Vector Database: ChromaDB Local Persistent)]
    end

    subgraph Retrieval_&_Generation ["2. Query & Generation Pipeline"]
        E[User Enters Query in Streamlit UI] --> F[Embed Query & Vector Search]
        D -->|Top-K Similar Chunks| F
        F --> G[Construct Grounded Prompt]
        G --> H[Groq Llama 3.1 8B Instant LLM]
        H --> I[Display Answer in Streamlit UI]
    end