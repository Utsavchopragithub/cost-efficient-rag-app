# Cost & Architecture Trade-off Analysis

## Monthly Cost Breakdown (Assuming 1536-dim vectors)

| Scale | Embedded / Self-Hosted (ChromaDB / LanceDB / pgvector) | Fully Managed DB (Pinecone / Weaviate Cloud) | Key Trade-offs |
| :--- | :--- | :--- | :--- |
| **100K Vectors** (~600MB) | **$0 / mo** (Runs locally or on S3 / local SSD) | **~$70 - $100 / mo** (Base Pod cost) | Managed gives easy setup; embedded is virtually free. |
| **1M Vectors** (~6GB) | **~$5 - $15 / mo** (AWS S3 storage + EBS volume) | **~$250 - $400 / mo** (Standard dedicated instance) | Disk-backed search (LanceDB) handles this with zero compute idle costs. |
| **10M Vectors** (~60GB) | **~$50 - $100 / mo** (Shared Postgres / EC2 + S3) | **~$1,200+ / mo** (Multi-node managed cluster) | High query throughput requires RAM index scaling for managed DBs. |

## Switch-to-Managed Decision Criteria
We would switch back to a fully managed vector DB if:
1. **Multi-region horizontal write scale** is required with <50ms query SLA across global users.
2. **Zero ops bandwidth** exists to manage DB backups, re-indexing, and RAM/disk cache tuning.