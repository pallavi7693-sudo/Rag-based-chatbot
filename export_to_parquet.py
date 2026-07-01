#!/usr/bin/env python3
"""
export_to_parquet.py - Generate Apache Parquet Knowledge & Embeddings Dataset
=============================================================================
This utility converts our verified mutual fund JSON corpus (`data/corpus.json`)
and its generated statistical/dense embedding vectors into an Apache Parquet
dataset (`data/corpus_embeddings.parquet`).

Why Parquet?
- Highly compressed, columnar binary format standard in AI & Data Science.
- Directly ingestible into Pandas, Polars, LanceDB, Milvus, and HuggingFace Hub.
- Preserves full schema types and high-dimensional floating-point vectors cleanly.
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from src.backend.chunker_and_embedder import FreeLocalEmbedder
except ImportError as e:
    print(f"[ERROR] Failed to import FreeLocalEmbedder: {e}")
    sys.exit(1)

def main():
    print("=" * 70)
    print("   FUNDIQ: APACHE PARQUET DATASET & EMBEDDINGS EXPORTER")
    print("=" * 70)

    corpus_path = os.path.join(project_root, "data", "corpus.json")
    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus file not found at: {corpus_path}")
        return

    print(f"\n[1/4] Loading verified JSON corpus from: {corpus_path}...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data.get("chunks", [])
    print(f"      Found {len(chunks)} factual knowledge chunks across {len(data.get('schemes', []))} schemes.")

    # Prepare document text for embedding
    documents = []
    for c in chunks:
        doc = f"{c.get('scheme', '')} {c.get('topic', '')} {' '.join(c.get('keywords', []))} {c.get('content', '')}".strip()
        documents.append(doc)

    print("\n[2/4] Generating dense embedding vectors using FreeLocalEmbedder...")
    embedder = FreeLocalEmbedder(model_type="bge")
    embeddings_matrix = embedder.fit_and_embed(documents)

    if hasattr(embeddings_matrix, "toarray"):
        embeddings_matrix = embeddings_matrix.toarray()
    elif not isinstance(embeddings_matrix, np.ndarray):
        embeddings_matrix = np.array(embeddings_matrix)

    num_chunks, num_dims = embeddings_matrix.shape
    print(f"      Generated ({num_chunks} x {num_dims}) normalized embeddings matrix.")

    print("\n[3/4] Constructing structured Pandas DataFrame...")
    rows = []
    for idx, c in enumerate(chunks):
        rows.append({
            "chunk_id": c.get("id", f"chunk_{idx+1}"),
            "scheme": c.get("scheme", ""),
            "topic": c.get("topic", ""),
            "keywords": c.get("keywords", []),
            "content": c.get("content", ""),
            "source_url": c.get("source_url", ""),
            "last_updated": c.get("last_updated", "July 2026"),
            "vector_dimension": num_dims,
            "embedding_vector": [float(val) for val in embeddings_matrix[idx]]
        })

    df = pd.DataFrame(rows)
    print(f"      DataFrame successfully constructed with shape: {df.shape}")
    print(df[["chunk_id", "scheme", "topic", "vector_dimension"]].head())

    print("\n[4/4] Exporting DataFrame to Apache Parquet format...")
    output_parquet = os.path.join(project_root, "data", "corpus_embeddings.parquet")
    
    # Export to Parquet using PyArrow engine
    df.to_parquet(output_parquet, engine="pyarrow", index=False)
    
    file_size_kb = os.path.getsize(output_parquet) / 1024
    print("-" * 70)
    print(f"[SUCCESS] Parquet dataset generated at: {output_parquet}")
    print(f"          File Size: {file_size_kb:.2f} KB | Total Rows: {len(df)} | Columns: {list(df.columns)}")
    print("=" * 70)
    print("\n[TIP] You can now load this dataset anytime in Python:")
    print("   import pandas as pd")
    print("   df = pd.read_parquet('data/corpus_embeddings.parquet')")
    print("=" * 70)

if __name__ == "__main__":
    main()
