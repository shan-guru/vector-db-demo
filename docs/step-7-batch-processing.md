# Step 7: Batch Job for Large Documents

For large documents (5–10 MB or more):

## Batch Processing Workflow

1. Load document
2. Split into chunks (paragraphs / tokens)
3. Convert each chunk into embeddings
4. Insert chunks in **batches** into Milvus

## Benefits

* Efficient indexing
* Scalable ingestion
* Better search granularity
* Supports large files without memory issues

This batch job can later be:

* A standalone Python script
* A scheduled task
* A background worker
