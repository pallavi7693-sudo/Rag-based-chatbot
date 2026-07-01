import os
import re
import json
from typing import List, Dict, Any, Union

# ==========================================
# 1. 100% FREE TEXT CHUNKING ENGINE
# ==========================================
class FreeRecursiveTextChunker:
    """
    A 100% free, open-source text chunking tool that recursively splits raw documents
    into semantic chunks without needing paid APIs or proprietary libraries.
    """
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        final_chunks = []
        if not text:
            return final_chunks
            
        return self._split_recursive(text, self.separators)

    def _split_recursive(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        separator = separators[-1]
        for s in separators:
            if s == "" or s in text:
                separator = s
                break
                
        if separator == ". ":
            # Negative lookbehind to prevent splitting on financial abbreviations (Rs., approx., vs., e.g., i.e.)
            splits = re.split(r'(?<!\bRs)(?<!\bapprox)(?<!\be\.g)(?<!\bi\.e)(?<!\bvs)\.\s+', text)
        elif separator:
            splits = text.split(separator)
        else:
            splits = list(text)
            
        good_splits = []
        for i, s in enumerate(splits):
            if separator != "" and i < len(splits) - 1:
                if separator == ". " and not s.endswith("."):
                    s = s + ". "
                elif separator != ". ":
                    s = s + separator
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                if good_splits:
                    merged = self._merge_splits(good_splits)
                    final_chunks.extend(merged)
                    good_splits = []
                if len(separators) > 1:
                    sub_chunks = self._split_recursive(s, separators[1:])
                    final_chunks.extend(sub_chunks)
                else:
                    final_chunks.append(s)
                    
        if good_splits:
            merged = self._merge_splits(good_splits)
            final_chunks.extend(merged)
            
        return [c.strip() for c in final_chunks if c.strip()]

    def _merge_splits(self, splits: List[str]) -> List[str]:
        merged = []
        current_chunk = []
        current_len = 0
        
        for s in splits:
            if current_len + len(s) > self.chunk_size and current_chunk:
                chunk_str = "".join(current_chunk).strip()
                merged.append(chunk_str)
                # Keep overlap
                while current_len > self.chunk_overlap and len(current_chunk) > 1:
                    removed = current_chunk.pop(0)
                    current_len -= len(removed)
            current_chunk.append(s)
            current_len += len(s)
            
        if current_chunk:
            merged.append("".join(current_chunk).strip())
            
        return merged

# ==========================================
# 2. 100% FREE LOCAL EMBEDDING ENGINE
# ==========================================
class FreeLocalEmbedder:
    """
    A 100% free embedding engine supporting zero-cost statistical embeddings (TF-IDF)
    and exclusively open-source BGE neural embeddings (BAAI/bge-small-en-v1.5).
    """
    def __init__(self, model_type: str = "bge", model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_type = model_type.lower()
        self.model_name = "BAAI/bge-small-en-v1.5" if "bge" in self.model_type or "neural" in self.model_type else model_name
        self.vectorizer = None
        self.hf_model = None
        
        if self.model_type == "tfidf":
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            except ImportError:
                raise RuntimeError("scikit-learn is required for free TF-IDF embeddings. Run: pip install scikit-learn")
        elif self.model_type in ["bge", "neural", "sentence-transformers", "huggingface"]:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading open-source BGE model: {self.model_name}...")
                self.hf_model = SentenceTransformer(self.model_name)
            except ImportError:
                print("sentence-transformers not installed. Falling back to free TF-IDF vectorizer...")
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.model_type = "tfidf"
                self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

    def fit_and_embed(self, documents: List[str]) -> Any:
        if not documents:
            return []
            
        if self.model_type == "tfidf":
            matrix = self.vectorizer.fit_transform(documents)
            return matrix
        else:
            embeddings = self.hf_model.encode(documents, show_progress_bar=False, normalize_embeddings=True)
            return embeddings

    def embed_query(self, query: str) -> Any:
        if self.model_type == "tfidf":
            return self.vectorizer.transform([query])
        else:
            return self.hf_model.encode([query], normalize_embeddings=True)

# ==========================================
# 3. PIPELINE DEMO / TEST FUNCTION
# ==========================================
def run_free_pipeline_demo():
    print("--- Running 100% Free Chunking & Embedding Demo ---")
    raw_amc_text = (
        "ICICI Prudential Large Cap Fund is an open-ended equity scheme predominantly investing in large cap stocks. "
        "The Total Expense Ratio (TER) of the direct plan growth option is approximately 0.88% per annum. "
        "An exit load of 1.00% is applicable if units are redeemed or switched out within 1 year from the date of allotment. "
        "The minimum SIP investment amount is Rs. 100 per month. There is no statutory lock-in period for this equity scheme. "
        "The scheme is categorized as Very High Risk on the SEBI Riskometer and is benchmarked against the NIFTY 100 TRI index."
    )
    
    # 1. Chunking
    chunker = FreeRecursiveTextChunker(chunk_size=200, chunk_overlap=30)
    chunks = chunker.split_text(raw_amc_text)
    print(f"Generated {len(chunks)} semantic chunks using FreeRecursiveTextChunker:")
    for i, c in enumerate(chunks):
        print(f"  [{i+1}] ({len(c)} chars): {c[:60]}...")
        
    # 2. Embedding
    embedder = FreeLocalEmbedder(model_type="bge")
    matrix = embedder.fit_and_embed(chunks)
    print(f"Generated embeddings matrix of shape: {matrix.shape}")
    print("--- Demo Completed Successfully ---")

if __name__ == "__main__":
    run_free_pipeline_demo()
