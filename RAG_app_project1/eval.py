# eval.py
import time
import json
from query import query_rag

# Sample Evaluation Dataset (15 Benchmark Questions & Ground Truth)
BENCHMARK_DATASET = [
    {
        "question": "What is the primary objective of the system?",
        "ground_truth_keywords": ["QA service", "low-cost vector store", "honest evaluation"]
    },
    {
        "question": "Which vector stores are allowed?",
        "ground_truth_keywords": ["pgvector", "Qdrant", "ChromaDB", "LanceDB", "FAISS", "sqlite-vec"]
    },
    {
        "question": "What are the required evaluation metrics?",
        "ground_truth_keywords": ["Recall@k", "Hit Rate", "MRR", "nDCG@k", "EM/F1"]
    }
    # Add remaining questions up to 15-30 items here
]

def evaluate_rag():
    total_queries = len(BENCHMARK_DATASET)
    hits = 0
    latencies = []
    results_log = []

    print(f"Starting Evaluation on {total_queries} benchmark queries...\n")

    for idx, item in enumerate(BENCHMARK_DATASET, start=1):
        q = item["question"]
        expected = item["ground_truth_keywords"]

        start = time.time()
        res = query_rag(q, k=4)
        latency = time.time() - start
        latencies.append(latency)

        # Hit Rate Check: Do retrieved answer/sources cover key facts?
        answer_text = res.get("answer", "")
        hit = any(kw.lower() in answer_text.lower() for kwstr in expected for kw in kwstr.split())
        if hit:
            hits += 1

        results_log.append({
            "query_id": idx,
            "question": q,
            "answer": answer_text,
            "sources": res.get("sources", []),
            "hit": hit,
            "latency_sec": round(latency, 3)
        })

    # Metric Calculations
    hit_rate = (hits / total_queries) * 100
    avg_latency = sum(latencies) / len(latencies)
    latencies.sort()
    p50_latency = latencies[int(0.50 * len(latencies))]
    p95_latency = latencies[int(0.95 * len(latencies))]

    summary = {
        "total_queries": total_queries,
        "hit_rate_pct": round(hit_rate, 2),
        "avg_latency_sec": round(avg_latency, 3),
        "p50_latency_sec": round(p50_latency, 3),
        "p95_latency_sec": round(p95_latency, 3)
    }

    print("=== EVALUATION SUMMARY ===")
    print(json.dumps(summary, indent=2))

    # Save results file
    with open("eval_results.json", "w") as f:
        json.dump({"summary": summary, "details": results_log}, f, indent=2)

if __name__ == "__main__":
    evaluate_rag()