# ⚡ Production-Grade RAG Pipeline

A high-performance, containerizable Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **Streamlit**, **ChromaDB**, and **Groq (Llama-3.1)**. 

This repository provides an end-to-end framework for ingesting local documents (Markdown, Plain Text), chunking with deterministic hash IDs to eliminate vector duplicates, storing embeddings in ChromaDB, and serving fast, cited context to LLMs via an interactive Streamlit UI.

---

## 🌟 Key Features

* **Real-time Document Ingestion:** Drag-and-drop `.txt` and `.md` file uploads directly from the Streamlit UI.
* **Deterministic Chunking:** Computes SHA-256 hashes based on document ID, chunk index, and content to guarantee idempotency and prevent vector duplication in ChromaDB.
* **Custom Metadata Filtering:** Tag chunks by custom categories during upload to enable targeted document retrieval during queries.
* **Low-Latency Retrieval:** Built on top of ChromaDB with vector search powered by Sentence Transformers.
* **Granular Metrics & Citations:** Tracks retrieval latency, total end-to-end response time, and exact token usage (prompt vs. completion) with direct chunk citations.
* **Clean Architecture Separation:** FastAPI handles backend orchestration, vector storage, and model calls; Streamlit handles presentation.

---

## 🏗️ Project Architecture

```text
RAG_APP/
├── data/                    # Storage directory for ingested raw documents
├── src/
│   ├── ingestion.py         # Document chunking & deterministic SHA-256 ID generation
│   └── rag_engine.py        # ChromaDB client & LLM pipeline logic
├── main.py                  # FastAPI REST endpoints (/query, /ingest)
├── app.py                   # Streamlit interactive Web Interface
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```
---

## ⚙️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend API:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
* **Vector Store:** [ChromaDB](https://www.trychroma.com/)
* **Embeddings:** HuggingFace / Sentence Transformers (`all-MiniLM-L6-v2`)
* **LLM Provider:** Groq API (`llama-3.1-8b-instant` / `llama-3.3-70b-versatile`)

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.10+** installed on your machine.

### 1. Clone the Repository & Setup Environment

```bash
# Navigate to project directory
cd D:\Projects\RAG_APP

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🏃 Running the Application

You will need **two terminal instances** open (with the virtual environment activated in both).

### Terminal 1: Launch FastAPI Backend

```powershell
uvicorn main:app --reload --reload-dir src
```

* **API Server:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### Terminal 2: Launch Streamlit Frontend

```powershell
streamlit run app.py
```

* **Streamlit Dashboard:** http://localhost:8501

---

## 🛰️ API Endpoint Reference

### 1. Ingest Document
* **Endpoint:** `POST /ingest`
* **Content-Type:** `multipart/form-data`
* **Parameters:**
  * `file`: Upload File (`.txt` or `.md`)
  * `category`: Optional metadata category string (default: `"general"`)
  * `chunk_size`: Words per chunk (default: `500`)
  * `chunk_overlap`: Overlapping words between consecutive chunks (default: `50`)

### 2. Query Pipeline
* **Endpoint:** `POST /query`
* **Content-Type:** `application/json`

* **Payload:**

```json
{
  "question": "What are the core features of the system?",
  "top_k": 5,
  "category_filter": "general"
}
```

---

## 🧪 Testing Ingestion and Queries

1. Open `http://localhost:8501` in your browser.
2. Navigate to the **"📤 Ingest Documents"** tab.
3. Upload any `.txt` or `.md` file, specify a category (e.g., `tech-docs`), and click **Start Ingestion**.
4. Switch to the **"🔍 Query Pipeline"** tab, ask a question related to your uploaded file, and inspect the retrieved chunks and generated response!
---
---

## 👤 Author

* **Developer:** Utsav Chopra
