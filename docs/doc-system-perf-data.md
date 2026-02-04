Here is a focused Markdown document covering the **two key aspects** you asked for:

1. **Performance aspects** — how vector search (Milvus) behaves in complex / large-scale scenarios  
2. **Metadata handling** — how to reliably store, retrieve and present **file references** (original document paths / locations / box locations) during query results

```markdown
# Milvus-based Document Search System  
## Critical Design Aspects: Performance & File Reference Metadata

### 1. Performance in Complex & Large-Scale Scenarios

**Core Principle**  
Milvus does **not** perform full-text or keyword scans over documents during queries.  
It performs **approximate nearest neighbor (ANN)** search in vector space using pre-built indexes → this is the source of its speed even when datasets grow large.

#### Key Performance Characteristics

- **Query latency does not grow linearly with number of documents**  
  Once an index is built, most queries return in 20–300 ms (local machine) even with millions of vectors.

- **Index types & trade-offs** (recommended choices)

  | Scenario                          | Recommended Index     | Recall/Accuracy | Query Speed | Memory Usage | Build Time | Best For                          |
  |-----------------------------------|-----------------------|------------------|-------------|--------------|------------|-----------------------------------|
  | Demo / < 1 million vectors        | HNSW                  | Very high        | Very fast   | Moderate–High| Moderate   | High-quality local testing        |
  | 1–10 million vectors, good recall | IVF_FLAT              | High             | Fast        | Moderate     | Fast       | Balanced prod use                 |
  | 10M+ vectors, memory constrained  | IVF_SQ8 / IVF_PQ      | Good–Medium      | Very fast   | Low          | Fast       | Large-scale, cost-sensitive       |
  | Highest recall needed             | HNSW + high efSearch  | Excellent        | Moderate    | High         | Moderate   | Precision-critical applications   |

- **Important tuning parameters**

  - `top_k`: usually 10–50 → higher = slower but more complete
  - `nprobe` (IVF): 8–128 → higher = better recall, slower
  - `ef` (HNSW): 64–512 during search → higher = better recall
  - Use **partition key** or **scalar filter** (`customer_id = 'ABC123'`) → reduces searched space dramatically

- **Scaling behavior (real numbers – typical laptop/server)**

  | # Vectors     | Index Type   | Query Latency (ms) | Memory (GB) approx. |
  |---------------|--------------|--------------------|---------------------|
  | 100,000       | HNSW         | 30–80              | ~1–2                |
  | 1,000,000     | HNSW         | 50–150             | ~8–12               |
  | 5,000,000     | IVF_PQ       | 80–250             | ~6–10               |
  | 20,000,000    | IVF_SQ8_PQ   | 100–400            | ~10–18              |

- **What keeps performance under control**

  1. Vector index (not brute-force)
  2. Partitioning / scalar filtering (skip irrelevant data)
  3. Consistent embedding model (same dimension across all data)
  4. Batch inserts + periodic index rebuild (instead of frequent small updates)
  5. Limit `top_k` and re-rank only the top 20–50 candidates if needed

→ **Bottom line**: Even with 50–100 large files today → and thousands tomorrow → query performance stays predictable and fast as long as you index properly and filter smartly.

### 2. Metadata Handling – Preserving & Presenting File References

**Goal**  
Every retrieved chunk must be traceable back to:
- Original file path (e.g. `/projects/2025/Q3/ABC_Corp_Onboarding_Guide_v2.md`)
- Optionally: file name, size, last modified, chunk offset/range

**Recommended Approaches** (ranked from simplest to most scalable)

| Approach                          | Metadata Location          | Pros                                      | Cons                                      | Best For                              |
|-----------------------------------|----------------------------|-------------------------------------------|-------------------------------------------|---------------------------------------|
| A. Inline in Milvus (scalar field)| Milvus collection          | Simplest, single source of truth          | String length limit (~65k), slower filter | < 1M vectors, short paths             |
| B. Separate lightweight DB        | SQLite / Redis / DynamoDB  | Very fast lookup, unlimited metadata      | Two systems to maintain                   | Most production cases                 |
| C. Hybrid (path in Milvus + extra in DB) | Milvus + Redis/PostgreSQL | Best of both: fast filter + rich metadata | Slightly more complex                     | Large scale + rich metadata needed    |

**Recommended strategy for your use case (B – Separate lightweight DB)**

**Why?**
- File paths can be long
- You may want extra fields later (author, version, approval date, stakeholder list…)
- Redis / SQLite lookup is extremely fast (< 5 ms for batch of 50 ids)

**Implementation flow**

1. **During ingestion (per chunk)**

   ```text
   chunk_id = uuid() or hash(file_path + chunk_index)
   vector  = embed(chunk_text)

   insert into Milvus:
     id          = chunk_id
     embedding   = vector
     # optional: customer_id (for filtering)

   insert into metadata store (SQLite example):
     chunk_id       TEXT PRIMARY KEY
     file_path      TEXT
     file_name      TEXT
     file_size_mb   REAL
     chunk_index    INTEGER
     chunk_start    INTEGER
     chunk_end      INTEGER
     last_modified  TEXT
     customer_id    TEXT   (optional)
   ```

2. **During query**

   ```text
   query_vector = embed(user_question)

   result = milvus.search(
       collection_name = "project_documents",
       data = [query_vector],
       filter = "customer_id == 'ABC123'",
       limit = 20,
       output_fields = ["id"]
   )

   chunk_ids = [hit["id"] for hit in result]

   metadata_rows = metadata_db.query(
       "SELECT file_path, file_name, chunk_start, chunk_end FROM chunks WHERE chunk_id IN (?)",
       chunk_ids
   )

   # Build final response
   context = "\n\n".join(relevant_chunk_texts)
   sources = set(row["file_path"] for row in metadata_rows)

   Response:
   """
   [Natural language answer / summary using retrieved chunks]

   **Referenced Documents:**
   • /projects/2025/Q3/ABC_Corp_Onboarding_Guide_v2.md
   • /projects/2025/Q2/Change-Request-XYZ-Approved.md
   • ...
   """
   ```

**Advantages of this pattern**
- Zero duplication risk (path lives in one place)
- Very fast batch lookup (Redis hash or SQLite IN clause)
- Easy to add more fields later (approval date, stakeholders, document version…)
- Paths become clickable links in UI
- Works perfectly with large files (10–100 MB) → chunks still point to exact source file

**Next refinement options (if needed later)**
- Add full-text keyword filter on file_name / path
- Store small preview snippet in metadata
- Versioning: add `document_version` field
- Soft delete / archival flag

Let me know if you want code snippets for any part (ingestion, query handler, SQLite schema, Redis usage…).
```

This Markdown keeps both topics concise yet detailed enough for planning / handover.  
Ready for your feedback or next focus area.