import json
import os
import re
from typing import List, Dict, Any
from src.backend.chunker_and_embedder import FreeLocalEmbedder

try:
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

OUT_OF_SCOPE_AMCS = [
    "hdfc", "sbi", "nippon", "axis", "kotak", "tata", "mirae", 
    "quant", "uti", "aditya birla", "dsp", "canara robeco", "motilal oswal"
]

ACRONYM_MAP = {
    "ter": "expense ratio",
    "sip": "systematic investment plan",
    "cas": "statement of account download",
    "nav": "net asset value",
    "aum": "assets under management",
    "kim": "key information memorandum",
    "sid": "scheme information document",
    "elss": "tax saver lock in"
}

class Retriever:
    """
    Adaptive Hybrid RAG Retrieval Engine (Layer 4) combining BGE/TF-IDF vector similarity
    with acronym expansion, tiered keyword boosting, and out-of-scope AMC suppression.
    """
    def __init__(self, corpus_path: str = None):
        if corpus_path is None:
            # Default to data/corpus.json relative to project root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            corpus_path = os.path.join(base_dir, "data", "corpus.json")
        
        self.corpus_path = corpus_path
        self.chunks = []
        self.documents = []
        self.embedder = None
        self.doc_embeddings = None
        
        self.load_corpus()
        if self.documents:
            print("Initializing FreeLocalEmbedder (Adaptive BGE / TF-IDF Hybrid) for Retriever...")
            self.embedder = FreeLocalEmbedder(model_type="bge")
            self.doc_embeddings = self.embedder.fit_and_embed(self.documents)

    def load_corpus(self):
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found at {self.corpus_path}")
        
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.chunks = data.get("chunks", [])
            
        # Build search text document for each chunk
        for chunk in self.chunks:
            scheme = chunk.get("scheme", "")
            topic = chunk.get("topic", "")
            keywords = " ".join(chunk.get("keywords", []))
            content = chunk.get("content", "")
            doc = f"{scheme} {topic} {keywords} {content}".lower()
            self.documents.append(doc)

    def _keyword_score(self, query: str, chunk: Dict[str, Any]) -> float:
        query_lower = query.lower()
        query_words = set(re.findall(r'\b\w+\b', query_lower))
        if not query_words:
            return 0.0
            
        score = 0.0
        scheme = chunk.get("scheme", "").lower()
        topic = chunk.get("topic", "").lower()
        keywords = [k.lower() for k in chunk.get("keywords", [])]
        
        # Exact Scheme match boost (+3.5)
        if "large cap" in query_lower and "large cap" in scheme:
            score += 3.5
        elif ("dynamic" in query_lower or "balanced" in query_lower) and "dynamic" in scheme:
            score += 3.5
        elif "short term" in query_lower and "short term" in scheme:
            score += 3.5
        elif ("flexi" in query_lower or "flexicap" in query_lower) and "flexi" in scheme:
            score += 3.5
        elif "top 100" in query_lower and "top 100" in scheme:
            score += 3.5
        elif "elss" in query_lower and ("elss" in topic or "elss" in keywords):
            score += 3.5
        elif ("statement" in query_lower or "cas" in query_lower or "download" in query_lower) and "statement" in topic:
            score += 3.5
        elif "tax" in query_lower and "tax" in topic:
            score += 3.5
            
        # Topic match boost (+2.0 per matching token)
        topic_words = set(re.findall(r'\b\w+\b', topic))
        if query_words.intersection(topic_words):
            score += 2.0 * len(query_words.intersection(topic_words))
            
        # Keyword match (+1.5 exact, +0.5 token overlap)
        for kw in keywords:
            if kw in query_lower:
                score += 1.5
            else:
                kw_words = set(re.findall(r'\b\w+\b', kw))
                overlap = query_words.intersection(kw_words)
                if overlap:
                    score += 0.5 * len(overlap)
                    
        return score

    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        if not self.chunks:
            return []
            
        query_lower = query.lower()
        
        # Edge Case 2.1: Out-of-Scope AMC Suppression
        for comp in OUT_OF_SCOPE_AMCS:
            if comp in query_lower and "icici" not in query_lower:
                return [{
                    "id": "out_of_scope",
                    "scheme": f"Out-of-Scope AMC Query ({comp.upper()})",
                    "topic": "Competitor Fund Query Refusal",
                    "keywords": ["out of scope", "competitor"],
                    "content": f"We could not find verified factual information regarding competitor mutual fund schemes ({comp.upper()}) in our ICICI Prudential corpus. FundIQ provides verified facts exclusively for ICICI Prudential mutual fund schemes. For details on competitor funds, please visit official AMFI documentation.",
                    "source_url": "https://www.amfiindia.com/investor-corner/knowledge-center/what-is-mutual-fund.html",
                    "last_updated": "July 2026"
                }]
                
        # Acronym & Synonym Expansion for enhanced recall
        expanded_query = query_lower
        for acronym, full_form in ACRONYM_MAP.items():
            if re.search(r'\b' + acronym + r'\b', query_lower):
                expanded_query += f" {full_form}"
                
        results = []
        dense_scores = [0.0] * len(self.chunks)
        
        if SKLEARN_AVAILABLE and self.embedder is not None and self.doc_embeddings is not None:
            try:
                query_vec = self.embedder.embed_query(expanded_query)
                cosine_sim = cosine_similarity(query_vec, self.doc_embeddings).flatten()
                dense_scores = list(cosine_sim)
            except Exception as e:
                print(f"Dense scoring failed: {e}")
                
        # Adaptive Scaling Factor (Alpha): Scale BGE neural vectors by 4.0 and TF-IDF statistical vectors by 5.0
        is_neural = hasattr(self.embedder, "model") and getattr(self.embedder, "model", None) is not None
        alpha = 4.0 if is_neural else 5.0
        
        for idx, chunk in enumerate(self.chunks):
            kw_score = self._keyword_score(expanded_query, chunk)
            dense_score = dense_scores[idx] * alpha
            total_score = kw_score + dense_score
            
            results.append({
                "chunk": chunk,
                "score": total_score,
                "dense_score": dense_score,
                "keyword_score": kw_score
            })
            
        # Sort by total score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top_k chunks with score > 0
        top_chunks = []
        for r in results[:top_k]:
            if r["score"] > 0:
                top_chunks.append(r["chunk"])
                
        # If no score > 0, return the highest scoring chunk anyway if requested
        if not top_chunks and results and top_k > 0:
            top_chunks.append(results[0]["chunk"])
            
        return top_chunks

# Global singleton instance for quick importing
_retriever_instance = None

def get_retriever() -> Retriever:
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = Retriever()
    return _retriever_instance

def retrieve_facts(query: str, top_k: int = 2) -> List[Dict[str, Any]]:
    retriever = get_retriever()
    return retriever.retrieve(query, top_k=top_k)
