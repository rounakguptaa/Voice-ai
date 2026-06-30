from typing import Dict, Any
from backend.guardrails import evaluate_query_and_retrieve

def process_rag_query(query: str, subject: str, top_k: int = 3, threshold: float = 0.7) -> Dict[str, Any]:
    """
    Retrieve relevant NCERT context chunks for a given query and subject using guardrails.
    """
    result = evaluate_query_and_retrieve(query, subject, top_k=top_k, threshold=threshold)
    return result
