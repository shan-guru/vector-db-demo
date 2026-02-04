# Step 4: Create Collection & Insert Data

This step demonstrates how to create a Milvus collection with a proper schema and insert document data as vectors. The design follows the architecture outlined in [Document Semantic Search System Design](doc-search-analysis.md) and [Performance & Metadata Handling Guide](doc-system-perf-data.md).

## Prerequisites

* Milvus running and connected (see [Step 1](step-1-run-milvus-docker.md) and [Step 3](step-3-connect-milvus.md))
* Python environment set up (see [Step 2](step-2-python-environment-setup.md))
* Understanding of embedding models and vector dimensions

## Collection Strategy

### Collection per Use-Case

Following the design recommendations, we use **one collection per use-case** to maintain isolation between different document sets:

| Collection Name     | Purpose                          | Vector Dim | Example Index          |
|---------------------|----------------------------------|------------|------------------------|
| `support_docs_v1`   | Customer support articles        | 768 / 1536 | HNSW or IVF_FLAT       |
| `internal_wiki_v1`  | Company internal knowledge base  | 768 / 1536 | IVF_SQ8_PQ (compressed)|
| `product_manuals_v1`| Technical PDFs/manuals           | 768 / 1536 | HNSW                   |

**Benefits:**
- No cross-mixing of results between use cases
- Independent scaling and indexing per collection
- Easy to manage and query specific document sets

## Schema Definition

### ⚠️ Schema Recommendation for support_docs_v1

**The minimal 3-field schema (id, embedding, file_path) is NOT sufficient** for a production support documents collection. 

**Recommended fields for `support_docs_v1`:**

| Field | Required? | Why? |
|-------|-----------|------|
| `id` | ✅ Yes | Primary key, unique identifier |
| `embedding` | ✅ Yes | Vector search capability |
| `file_path` | ✅ Yes | Traceability to source file |
| `file_name` | ✅ **Recommended** | Easier filtering and display |
| `chunk_index` | ✅ **Recommended** | Maintain document order |
| `category` | ✅ **Recommended** | Filter by support topic (critical for support docs) |
| `text` | ⚠️ Optional | Quick preview (can be in metadata store) |

**Why these additional fields matter:**
- **`category`**: Essential for support docs - allows filtering by topic (installation, troubleshooting, billing, etc.)
- **`file_name`**: Easier to display and filter than full `file_path`
- **`chunk_index`**: Maintains document structure and order
- **`text`**: Optional but useful for quick previews without metadata lookup

### Minimal Schema (Basic - Not Recommended for Production)

This is the absolute minimum schema. **Not recommended** for `support_docs_v1` as it lacks fields needed for filtering and organization:

| Field       | Type      | Description                          | Indexed? | Primary Key? |
|-------------|-----------|--------------------------------------|----------|--------------|
| `id`        | VARCHAR / INT64 | Unique chunk ID (UUID or auto-increment) | Yes      | Yes          |
| `embedding` | FLOAT_VECTOR | Dense vector (768, 1024, 1536, …)   | Yes      | No           |
| `file_path` | VARCHAR   | Original full path (optional inline) | No       | No           |

**Limitations:**
- No way to filter by file or category
- No chunk ordering information
- Difficult to organize and query support documents
- Cannot track document metadata

**Note:** If keeping paths in Milvus → limit length (e.g. < 512 chars). For longer paths or rich metadata, use a separate metadata store (see [Metadata Handling](#metadata-handling-approaches)).

### Recommended Schema for support_docs_v1

For a support documents collection, we recommend this enhanced schema that enables filtering, organization, and better querying:

| Field       | Type      | Description                          | Indexed? | Primary Key? | Use Case |
|-------------|-----------|--------------------------------------|----------|--------------|----------|
| `id`        | VARCHAR   | Unique chunk ID (UUID recommended)   | Yes      | Yes          | Primary identifier |
| `embedding` | FLOAT_VECTOR | Dense vector (768, 1024, 1536, …)   | Yes      | No           | Vector search |
| `file_path` | VARCHAR   | Original full path (max 512 chars)   | No       | No           | File traceability |
| `file_name` | VARCHAR   | Just the filename (e.g., "guide.md") | No       | No           | Display & filtering |
| `chunk_index`| INT64   | Position of chunk within file (0-based) | No | No | Ordering chunks |
| `category`  | VARCHAR   | Support category (e.g., "installation", "troubleshooting") | No | No | Filtering by topic |
| `text`      | VARCHAR   | Chunk text preview (max 2000 chars) | No       | No           | Quick preview |

**Benefits of this schema:**
- ✅ **Filtering**: Can filter by `category`, `file_name`, or `file_path`
- ✅ **Organization**: Group and organize support docs by category
- ✅ **Ordering**: `chunk_index` helps maintain document order
- ✅ **Display**: `file_name` and `text` for better UI presentation
- ✅ **Performance**: Scalar filters reduce search space (see [Performance Guide](doc-system-perf-data.md))

**Example queries enabled:**
- Filter by category: `category == "installation"`
- Filter by file: `file_name == "getting-started.md"`
- Filter by path pattern: `file_path like "/docs/troubleshooting/%"`

### Schema with Optional Metadata Fields

For simpler setups, you can include additional scalar fields:

| Field       | Type      | Description                          |
|-------------|-----------|--------------------------------------|
| `id`        | VARCHAR   | Unique chunk ID                      |
| `embedding` | FLOAT_VECTOR | Vector embeddings                 |
| `file_path` | VARCHAR   | Original file path (max 512 chars)   |
| `chunk_index`| INT64    | Index of chunk within file          |
| `text`      | VARCHAR   | Chunk text preview (optional)        |

## Create Collection - Code Example

### Basic Collection Creation

```python
from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility
)

# Connect to Milvus (assuming connection from Step 3)
from milvus_connection import connect
connect()

# Collection parameters
COLLECTION_NAME = "support_docs_v1"
DIMENSION = 768  # or 1536 depending on embedding model

# Define fields - RECOMMENDED schema for support_docs_v1
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
    FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=255),
    FieldSchema(name="chunk_index", dtype=DataType.INT64),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
]

# Create schema
schema = CollectionSchema(
    fields=fields,
    description="Customer support documents collection with enhanced metadata"
)

# Create collection
collection = Collection(
    name=COLLECTION_NAME,
    schema=schema
)

print(f"✅ Collection '{COLLECTION_NAME}' created successfully!")
```

### Alternative: Minimal Schema (If Using Separate Metadata Store)

If you're using Approach B (separate metadata store), you can use a minimal schema in Milvus:

```python
from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType
)

# Minimal schema when using external metadata store
fields = [
    FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    # Optional: Add only essential filter fields
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),  # For filtering
]

schema = CollectionSchema(
    fields=fields,
    description="Minimal schema with external metadata store"
)

collection = Collection(
    name="internal_wiki_v1",
    schema=schema
)
```

**When to use minimal schema:**
- Using separate metadata store (SQLite/Redis/PostgreSQL)
- File paths are very long (> 512 chars)
- Need rich metadata that doesn't fit in Milvus
- Want to keep Milvus lean for performance

## Metadata Handling Approaches

As outlined in [Performance & Metadata Handling Guide](doc-system-perf-data.md), there are three approaches:

### Approach A: Inline in Milvus (Simplest)

Store metadata directly in Milvus collection as scalar fields.

**Pros:**
- Simplest setup, single source of truth
- No additional database needed

**Cons:**
- String length limit (~65k chars)
- Slower filtering on large datasets

**Best for:** < 1M vectors, short file paths

### Approach B: Separate Lightweight DB (Recommended)

Store vectors in Milvus, metadata in SQLite/Redis/PostgreSQL.

**Pros:**
- Very fast lookup (< 5 ms for batch of 50 ids)
- Unlimited metadata fields
- No string length restrictions

**Cons:**
- Two systems to maintain

**Best for:** Most production cases (recommended)

**Implementation:**
```python
# Insert into Milvus
milvus_data = [
    {"id": "chunk_001", "embedding": [0.1, 0.2, ...], "file_path": "/docs/guide.md"}
]

# Insert into SQLite metadata store
metadata_data = {
    "chunk_id": "chunk_001",
    "file_path": "/docs/guide.md",
    "file_name": "guide.md",
    "file_size_mb": 2.5,
    "chunk_index": 0,
    "chunk_start": 0,
    "chunk_end": 1000,
    "last_modified": "2025-01-15"
}
```

### Approach C: Hybrid

Store file_path in Milvus (for filtering) + rich metadata in separate DB.

**Best for:** Large scale + rich metadata needed

## Insert Data

### Basic Insert Example

```python
import numpy as np
from pymilvus import Collection

# Assume collection is already created
collection = Collection("support_docs_v1")

# Prepare data
# In real scenario, you would:
# 1. Read documents
# 2. Chunk text
# 3. Generate embeddings using your embedding model
# 4. Prepare entities

# Example data (replace with actual embeddings)
# Using the recommended schema for support_docs_v1
entities = [
    {
        "id": "chunk_001",
        "embedding": np.random.rand(768).tolist(),  # Replace with actual embedding
        "file_path": "/docs/getting-started.md",
        "file_name": "getting-started.md",
        "chunk_index": 0,
        "category": "installation",
        "text": "This guide will help you get started with our product..."
    },
    {
        "id": "chunk_002",
        "embedding": np.random.rand(768).tolist(),
        "file_path": "/docs/installation.md",
        "file_name": "installation.md",
        "chunk_index": 0,
        "category": "installation",
        "text": "To install the software, follow these steps..."
    }
]

# Insert data
insert_result = collection.insert(entities)
print(f"✅ Inserted {len(entities)} entities")

# Flush to make data searchable
collection.flush()
print("✅ Data flushed and ready for search")
```

### Batch Insert (Recommended for Large Datasets)

```python
def batch_insert(collection, data_batch, batch_size=1000):
    """
    Insert data in batches for better performance.
    
    Args:
        collection: Milvus collection object
        data_batch: List of entities to insert
        batch_size: Number of entities per batch
    """
    total_inserted = 0
    
    for i in range(0, len(data_batch), batch_size):
        batch = data_batch[i:i + batch_size]
        insert_result = collection.insert(batch)
        total_inserted += len(batch)
        print(f"Inserted batch {i//batch_size + 1}: {len(batch)} entities")
    
    # Flush after all inserts
    collection.flush()
    print(f"✅ Total inserted: {total_inserted} entities")
    return total_inserted

# Usage
# batch_insert(collection, large_data_list, batch_size=1000)
```

## Create Index

After inserting data, create an index for efficient similarity search. Index choice depends on your scale (see [Performance Guide](doc-system-perf-data.md)).

### HNSW Index (Recommended for Demo / < 1M vectors)

```python
from pymilvus import Collection

collection = Collection("support_docs_v1")

# Create HNSW index
index_params = {
    "metric_type": "L2",  # or "IP" for inner product
    "index_type": "HNSW",
    "params": {
        "M": 16,              # Number of connections
        "efConstruction": 200 # Build-time parameter
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)

print("✅ HNSW index created")
```

### IVF_FLAT Index (For Production / 1-10M vectors)

```python
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {
        "nlist": 1024  # Number of clusters
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)
```

### IVF_SQ8_PQ Index (For Large Scale / 10M+ vectors)

```python
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_SQ8",
    "params": {
        "nlist": 1024
    }
}

collection.create_index(
    field_name="embedding",
    index_params=index_params
)
```

## Index Type Selection Guide

| Scenario                          | Recommended Index     | Recall/Accuracy | Query Speed | Memory Usage |
|-----------------------------------|-----------------------|------------------|-------------|--------------|
| Demo / < 1 million vectors        | HNSW                  | Very high        | Very fast   | Moderate–High|
| 1–10 million vectors, good recall | IVF_FLAT              | High             | Fast        | Moderate     |
| 10M+ vectors, memory constrained  | IVF_SQ8 / IVF_PQ      | Good–Medium      | Very fast   | Low          |
| Highest recall needed             | HNSW + high efSearch  | Excellent        | Moderate    | High         |

## Verify Collection and Data

```python
from pymilvus import utility

# Check if collection exists
if utility.has_collection("support_docs_v1"):
    print("✅ Collection exists")

# Get collection info
collection = Collection("support_docs_v1")
print(f"Collection name: {collection.name}")
print(f"Number of entities: {collection.num_entities}")

# Check index status
indexes = collection.indexes
for index in indexes:
    print(f"Index: {index.field_name}, Type: {index.params}")
```

## Complete Example Script

See `doc-expert/step4_create_collection.py` for a complete working example that:
- Creates a collection with proper schema
- Inserts sample data
- Creates an index
- Verifies the setup

## Next Steps

Once your collection is created and indexed:
- Proceed to [Step 5: Similarity Search](step-5-similarity-search.md) to query your data
- For batch processing of large documents, see [Step 7: Batch Processing](step-7-batch-processing.md)

## References

- [Document Semantic Search System Design](doc-search-analysis.md) - Full architecture and design
- [Performance & Metadata Handling Guide](doc-system-perf-data.md) - Performance optimization and metadata strategies
