import os
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from backend.config import INDEXES_DIR, SYLLABUS_FALLBACK

# Global lazy loaded models & indices cache
_MODEL = None
_INDEX_CACHE = {}
_CHUNKS_CACHE = {}

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL

def load_subject_index_and_chunks(subject: str) -> Tuple[Any, List[Dict[str, Any]]]:
    """Load or retrieve cached FAISS index and chunks pickle for given subject."""
    subj_key = subject.strip().lower()
    if subj_key not in ["science", "mathematics"]:
        subj_key = "science"
        
    if subj_key in _INDEX_CACHE and subj_key in _CHUNKS_CACHE:
        return _INDEX_CACHE[subj_key], _CHUNKS_CACHE[subj_key]
        
    index_file = os.path.join(INDEXES_DIR, f"10_{subj_key}.faiss")
    pickle_file = os.path.join(INDEXES_DIR, f"10_{subj_key}_chunks.pkl")
    
    if not os.path.exists(index_file) or not os.path.exists(pickle_file):
        return None, []
        
    try:
        index = faiss.read_index(index_file)
        with open(pickle_file, "rb") as f:
            chunks = pickle.load(f)
            
        _INDEX_CACHE[subj_key] = index
        _CHUNKS_CACHE[subj_key] = chunks
        return index, chunks
    except Exception as e:
        print(f"Error loading index/chunks for {subj_key}: {e}")
        return None, []

def evaluate_query_and_retrieve(query: str, subject: str, top_k: int = 3, threshold: float = 0.7) -> Dict[str, Any]:
    """
    Check query relevance using FAISS vector search (threshold = 0.7).
    Returns dictionary with retrieved chunks, relevance boolean, and blocked flag.
    """
    subj_key = subject.strip().lower()
    index, chunks = load_subject_index_and_chunks(subj_key)
    
    # Fallback if index is missing
    if index is None or not chunks:
        fallback_topics = SYLLABUS_FALLBACK.get(subj_key, SYLLABUS_FALLBACK["science"])
        fallback_chunks = [
            {
                "source": f"{subj_key.capitalize()}/syllabus_fallback",
                "chunk_id": idx + 1,
                "text": f"Chapter Topic: {topic}. This is part of the Class 10 {subj_key.capitalize()} curriculum.",
                "sentence_count": 2
            }
            for idx, topic in enumerate(fallback_topics[:top_k])
        ]
        return {
            "is_relevant": True,
            "blocked_flag": False,
            "retrieved_chunks": fallback_chunks,
            "max_score": 1.0,
            "rejection_message": ""
        }
        
    model = get_model()
    query_vector = model.encode([query], convert_to_numpy=True).astype(np.float32)
    faiss.normalize_L2(query_vector)
    
    # Perform IP search (cosine similarity since vectors are normalized)
    distances, indices = index.search(query_vector, top_k)
    
    top_scores = distances[0]
    top_indices = indices[0]
    
    max_score = float(top_scores[0]) if len(top_scores) > 0 else 0.0
    
    if max_score < threshold:
        return {
            "is_relevant": False,
            "blocked_flag": True,
            "retrieved_chunks": [],
            "max_score": max_score,
            "rejection_message": (
                "Bhai/Beta, main sirf Class 10 Science aur Maths ke syllabus se jude sawalon ka jawab de sakta hoon. "
                "Kripya apne padhai se sambandhit sawal poochein!"
            )
        }
        
    retrieved = []
    for score, idx in zip(top_scores, top_indices):
        if idx >= 0 and idx < len(chunks):
            chunk_data = dict(chunks[idx])
            chunk_data["similarity_score"] = float(score)
            retrieved.append(chunk_data)
            
    return {
        "is_relevant": True,
        "blocked_flag": False,
        "retrieved_chunks": retrieved,
        "max_score": max_score,
        "rejection_message": ""
    }
