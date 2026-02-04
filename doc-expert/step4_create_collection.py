#!/usr/bin/env python3
"""
Step 4: Create Collection & Insert Data

This script creates the support_docs_v1 collection with the recommended schema
and demonstrates how to insert data and create indexes.

Schema includes:
- id (VARCHAR) - Primary key
- embedding (FLOAT_VECTOR) - Vector embeddings
- file_path (VARCHAR) - Source file path
- file_name (VARCHAR) - Filename for display/filtering
- chunk_index (INT64) - Position within file
- category (VARCHAR) - Support topic category
- text (VARCHAR) - Chunk text preview
"""

import sys
import os

# Check if running in virtual environment
if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("⚠️  Warning: Virtual environment not detected!")
    print("\n💡 Please activate the virtual environment first:")
    print("   source venv/bin/activate")
    print("   or")
    print("   source start.sh")
    print("\nThen run the script again.")
    sys.exit(1)

import uuid
import numpy as np
from pymilvus import (
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility
)

# Import connection utility
from milvus_connection import connect, verify_connection, list_collections


# Collection configuration
COLLECTION_NAME = "support_docs_v1"
DIMENSION = 768  # Embedding dimension (adjust based on your model: 768, 1024, 1536)
DESCRIPTION = "Customer support documents collection with enhanced metadata"


def create_collection_schema(dimension: int = 768) -> CollectionSchema:
    """
    Create the recommended schema for support_docs_v1 collection.
    
    Args:
        dimension (int): Vector dimension. Default: 768
        
    Returns:
        CollectionSchema: Schema object for the collection
    """
    # Define all fields according to recommended schema
    fields = [
        # Primary key - unique chunk identifier
        FieldSchema(
            name="id",
            dtype=DataType.VARCHAR,
            is_primary=True,
            max_length=100,
            description="Unique chunk ID (UUID recommended)"
        ),
        
        # Vector field - embeddings for similarity search
        FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=dimension,
            description="Dense vector embeddings"
        ),
        
        # File path - original source file location
        FieldSchema(
            name="file_path",
            dtype=DataType.VARCHAR,
            max_length=512,
            description="Original full file path"
        ),
        
        # File name - just the filename for easier display/filtering
        FieldSchema(
            name="file_name",
            dtype=DataType.VARCHAR,
            max_length=255,
            description="Filename (e.g., 'guide.md')"
        ),
        
        # Chunk index - position of chunk within file
        FieldSchema(
            name="chunk_index",
            dtype=DataType.INT64,
            description="Position of chunk within file (0-based)"
        ),
        
        # Category - support topic category for filtering
        FieldSchema(
            name="category",
            dtype=DataType.VARCHAR,
            max_length=100,
            description="Support category (e.g., 'installation', 'troubleshooting')"
        ),
        
        # Text - chunk text preview
        FieldSchema(
            name="text",
            dtype=DataType.VARCHAR,
            max_length=2000,
            description="Chunk text preview"
        ),
    ]
    
    # Create schema
    schema = CollectionSchema(
        fields=fields,
        description=DESCRIPTION
    )
    
    return schema


def create_collection(collection_name: str, dimension: int = 768, drop_existing: bool = False) -> Collection:
    """
    Create a new collection with the recommended schema.
    
    Args:
        collection_name (str): Name of the collection
        dimension (int): Vector dimension. Default: 768
        drop_existing (bool): Whether to drop existing collection if it exists
        
    Returns:
        Collection: Created collection object
    """
    # Check if collection already exists
    if utility.has_collection(collection_name):
        if drop_existing:
            print(f"⚠️  Collection '{collection_name}' already exists. Dropping it...")
            utility.drop_collection(collection_name)
        else:
            print(f"ℹ️  Collection '{collection_name}' already exists. Loading it...")
            return Collection(collection_name)
    
    # Create schema
    print(f"📋 Creating schema for '{collection_name}'...")
    schema = create_collection_schema(dimension)
    
    # Create collection
    print(f"🔨 Creating collection '{collection_name}'...")
    collection = Collection(
        name=collection_name,
        schema=schema
    )
    
    print(f"✅ Collection '{collection_name}' created successfully!")
    return collection


def create_hnsw_index(collection: Collection, metric_type: str = "L2") -> None:
    """
    Create HNSW index on the embedding field.
    Recommended for demo / < 1M vectors.
    
    Args:
        collection (Collection): Collection object
        metric_type (str): Distance metric. "L2" or "IP". Default: "L2"
    """
    print(f"📊 Creating HNSW index on 'embedding' field...")
    
    index_params = {
        "metric_type": metric_type,
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
    
    print("✅ HNSW index created successfully!")


def insert_sample_data(collection: Collection, num_samples: int = 5) -> None:
    """
    Insert sample data into the collection for testing.
    
    Args:
        collection (Collection): Collection object
        num_samples (int): Number of sample records to insert
    """
    print(f"📥 Inserting {num_samples} sample records...")
    
    # Sample categories for support docs
    categories = ["installation", "troubleshooting", "billing", "features", "api"]
    file_names = [
        "getting-started.md",
        "troubleshooting-guide.md",
        "billing-faq.md",
        "feature-overview.md",
        "api-reference.md"
    ]
    
    entities = []
    
    for i in range(num_samples):
        chunk_id = str(uuid.uuid4())
        
        # Generate random embedding (replace with actual embeddings in production)
        embedding = np.random.rand(DIMENSION).tolist()
        
        # Create entity
        entity = {
            "id": chunk_id,
            "embedding": embedding,
            "file_path": f"/docs/support/{file_names[i]}",
            "file_name": file_names[i],
            "chunk_index": i,
            "category": categories[i % len(categories)],
            "text": f"This is sample chunk {i+1} from {file_names[i]}. "
                   f"Category: {categories[i % len(categories)]}. "
                   f"In a real scenario, this would contain actual document content."
        }
        
        entities.append(entity)
    
    # Insert data
    insert_result = collection.insert(entities)
    print(f"✅ Inserted {len(entities)} entities")
    
    # Flush to make data searchable
    print("💾 Flushing data to make it searchable...")
    collection.flush()
    print("✅ Data flushed successfully!")


def verify_collection(collection: Collection) -> None:
    """
    Verify collection setup and display information.
    
    Args:
        collection (Collection): Collection object
    """
    print("\n" + "=" * 60)
    print("Collection Verification")
    print("=" * 60)
    
    # Collection info
    print(f"\n📋 Collection Name: {collection.name}")
    print(f"📊 Number of Entities: {collection.num_entities}")
    
    # Schema info
    print(f"\n📐 Schema Fields:")
    for field in collection.schema.fields:
        field_type = field.dtype.name
        if field.dtype == DataType.FLOAT_VECTOR:
            field_type = f"FLOAT_VECTOR({field.params.get('dim', '?')})"
        print(f"  - {field.name}: {field_type} "
              f"{'(Primary Key)' if field.is_primary else ''}")
    
    # Index info
    print(f"\n🔍 Indexes:")
    indexes = collection.indexes
    if indexes:
        for index in indexes:
            print(f"  - Field: {index.field_name}")
            print(f"    Type: {index.params.get('index_type', 'Unknown')}")
            print(f"    Metric: {index.params.get('metric_type', 'Unknown')}")
    else:
        print("  ⚠️  No indexes found. Create an index for efficient search.")
    
    print("\n" + "=" * 60)


def main():
    """Main function to create collection and insert sample data."""
    print("=" * 60)
    print("Step 4: Create Collection & Insert Data")
    print("=" * 60)
    print()
    
    # Connect to Milvus
    print("🔌 Connecting to Milvus...")
    if not connect():
        print("\n❌ Failed to connect to Milvus.")
        print("💡 Make sure Milvus is running (see Step 1)")
        sys.exit(1)
    
    if not verify_connection():
        print("\n❌ Connection verification failed.")
        sys.exit(1)
    
    print()
    
    # Create collection
    try:
        collection = create_collection(
            collection_name=COLLECTION_NAME,
            dimension=DIMENSION,
            drop_existing=False  # Set to True to recreate existing collection
        )
        print()
        
        # Create index (only if collection is new or has no index)
        indexes = collection.indexes
        if not indexes:
            create_hnsw_index(collection)
            print()
        else:
            print("ℹ️  Index already exists. Skipping index creation.")
            print()
        
        # Insert sample data (only if collection is empty)
        if collection.num_entities == 0:
            insert_sample_data(collection, num_samples=5)
            print()
        else:
            print(f"ℹ️  Collection already contains {collection.num_entities} entities.")
            print("💡 To insert new data, use the insert functions directly.")
            print()
        
        # Verify collection
        verify_collection(collection)
        
        print("\n✅ Step 4 completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Insert your actual document data with real embeddings")
        print("   2. Proceed to Step 5: Similarity Search")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
