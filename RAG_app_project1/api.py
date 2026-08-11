import time
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from ingest import ingest_document
from query import query_rag

app = FastAPI(title="Cost-Efficient RAG API")

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 4
    category_filter: Optional[str] = None

class IngestRequest(BaseModel):
    file_path: str
    category: Optional[str] = "default"

@app.post("/ingest")
def handle_ingest(req: IngestRequest):
    try:
        db = ingest_document(req.file_path, category=req.category)
        return {"status": "success", "file_path": req.file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def handle_query(req: QueryRequest):
    start_time = time.time()
    try:
        response = query_rag(
            question=req.question, 
            k=req.top_k, 
            category_filter=req.category_filter
        )
        latency = round(time.time() - start_time, 3)
        response["total_latency_sec"] = latency
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)