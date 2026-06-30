import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from backend.config import load_chunks_by_subject, INDEXES_DIR

def build_indexes():
    """
    Build FAISS indices for Science and Mathematics subjects using sentence-transformers.
    Saves index files (.faiss) and metadata pickles (.pkl) into INDEXES_DIR.
    """
    print("Loading embedding model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    subjects = ["science", "mathematics"]
    
    for subj in subjects:
        print(f"\n--- Processing subject: {subj.capitalize()} ---")
        chunks = load_chunks_by_subject(subj)
        print(f"Loaded {len(chunks)} chunks for {subj}.")
        
        if not chunks:
            print(f"Warning: No chunks found for {subj}!")
            continue
            
        texts = [c.get("text", "") for c in chunks]
        
        print(f"Encoding {len(texts)} texts...")
        embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # Ensure float32 and normalize for cosine similarity via IndexFlatIP
        embeddings = embeddings.astype(np.float32)
        faiss.normalize_L2(embeddings)
        
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)
        
        index_file = os.path.join(INDEXES_DIR, f"10_{subj}.faiss")
        pickle_file = os.path.join(INDEXES_DIR, f"10_{subj}_chunks.pkl")
        
        print(f"Saving FAISS index to {index_file}...")
        faiss.write_index(index, index_file)
        
        print(f"Saving chunks metadata to {pickle_file}...")
        with open(pickle_file, "wb") as f:
            pickle.dump(chunks, f)
            
        print(f"Successfully built index for {subj} with {index.ntotal} vectors.")

if __name__ == "__main__":
    build_indexes()
