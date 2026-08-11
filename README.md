# Cost-Efficient RAG Application

## Overview
A lightweight, cost-effective RAG pipeline built with Groq Llama-3.1-8b-instant, HuggingFace embeddings (`all-MiniLM-L6-v2`), and ChromaDB vector store.

## Features
- Ingestion with idempotency and customizable metadata tags.
- Free local vector search + fast LLM inference via Groq.
- FastAPI endpoints for ingestion (`/ingest`) and query retrieval (`/query`).
- Evaluation harness generating hit rate, precision, and latency metrics.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env`: Set `GROQ_API_KEY=your_key`
3. Run API server: `python RAG_app_project1/api.py`
4. Run evaluation: `python RAG_app_project1/eval.py`

## Deliverables
- `api.py` & `query.py` (Runnable RAG Service)
- `eval.py` & `eval_results.json` (Evaluation Harness & Output)
- `COST_ANALYSIS.md` (Cost Breakdown & Database Comparison)