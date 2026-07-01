#!/usr/bin/env python3
"""
view_embeddings.py - Standalone Script to View & Inspect Semantic Embeddings
=============================================================================
This script loads the verified mutual fund corpus from `data/corpus.json`,
vectorizes all 22 semantic chunks using our 100% Free Local Embedder (BGE/TF-IDF),
and displays the numerical embedding vectors, dimensions, and L2 norms.
"""

import json
import os
import sys
import numpy as np

# Add project root to path so we can import our backend modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from src.backend.chunker_and_embedder import FreeLocalEmbedder
except ImportError as e:
    print(f"[ERROR] Failed to import FreeLocalEmbedder: {e}")
    sys.exit(1)

def main():
    print("=" * 70)
    print("   FUNDIQ: SEMANTIC EMBEDDINGS INSPECTOR (100% FREE & LOCAL)")
    print("=" * 70)

    corpus_path = os.path.join(project_root, "data", "corpus.json")
    if not os.path.exists(corpus_path):
        print(f"[ERROR] Corpus file not found at: {corpus_path}")
        return

    print(f"\n[1/3] Loading factual corpus from: {corpus_path}...")
    with open(corpus_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data.get("chunks", [])
    print(f"      Loaded {len(chunks)} semantic knowledge chunks across {len(data.get('schemes', []))} schemes.")

    # Prepare document strings (Scheme + Topic + Keywords + Content)
    documents = []
    for c in chunks:
        doc = f"{c.get('scheme', '')} {c.get('topic', '')} {' '.join(c.get('keywords', []))} {c.get('content', '')}".strip()
        documents.append(doc)

    print("\n[2/3] Initializing FreeLocalEmbedder (BAAI/bge-small-en-v1.5 / TF-IDF)...")
    embedder = FreeLocalEmbedder(model_type="bge")

    print("\n[3/3] Generating dense vector embeddings for all chunks...")
    embeddings_matrix = embedder.fit_and_embed(documents)

    # Convert scipy sparse matrix to numpy dense array if TF-IDF fallback was used
    if hasattr(embeddings_matrix, "toarray"):
        embeddings_matrix = embeddings_matrix.toarray()
    elif not isinstance(embeddings_matrix, np.ndarray):
        embeddings_matrix = np.array(embeddings_matrix)

    num_chunks, num_dims = embeddings_matrix.shape
    print(f"\n---> Successfully generated Embeddings Matrix of Shape: ({num_chunks} chunks x {num_dims} dimensions)")
    print("-" * 70)

    # Display detailed embedding preview for each chunk
    print("\n[EMBEDDINGS PREVIEW FOR EACH CHUNK]")
    for idx, chunk in enumerate(chunks):
        vec = embeddings_matrix[idx]
        l2_norm = np.linalg.norm(vec)
        
        # Format the first 6 numerical weights of the embedding vector
        first_6_vals = ", ".join([f"{val:+.4f}" for val in vec[:6]])
        
        print(f"\nID:       {chunk.get('id', f'chunk_{idx+1}')}")
        print(f"Scheme:   {chunk.get('scheme', 'N/A')}")
        print(f"Topic:    {chunk.get('topic', 'N/A')}")
        print(f"Dim/Norm: {num_dims}-dimensional vector | L2 Norm: {l2_norm:.4f}")
        print(f"Vector:   [{first_6_vals}, ... ]")
        print("-" * 50)

    # Optionally save the exported embeddings to an inspection file
    output_path = os.path.join(project_root, "data", "exported_embeddings.json")
    print(f"\n[INFO] Exporting all numerical vectors to: {output_path}...")
    
    export_data = []
    for idx, chunk in enumerate(chunks):
        export_data.append({
            "id": chunk.get("id"),
            "scheme": chunk.get("scheme"),
            "topic": chunk.get("topic"),
            "vector_dimension": num_dims,
            "vector_preview": [round(float(v), 5) for v in embeddings_matrix[idx][:10]],  # first 10 dims
            "full_vector": [round(float(v), 6) for v in embeddings_matrix[idx]]
        })
        
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(export_data, out_f, indent=2)
        
    print(f"[SUCCESS] Exported 22 chunk embeddings to {output_path}.")
    print("=" * 70)

if __name__ == "__main__":
    main()
