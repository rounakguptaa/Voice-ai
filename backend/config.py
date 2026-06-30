import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Define paths using os.path.join for cross-platform compatibility
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

ROOT_DIR = BASE_DIR
NCERT_CHUNKS_PATH = os.path.join(ROOT_DIR, "ncert_chunks.json")
SYLLABUS_DATA_DIR = os.path.join(ROOT_DIR, "syllabus_data")
INDEXES_DIR = os.path.join(SYLLABUS_DATA_DIR, "indexes")
TEMP_AUDIO_DIR = os.path.join(ROOT_DIR, "temp_audio")

# Ensure directories exist
os.makedirs(INDEXES_DIR, exist_ok=True)
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# Fallback syllabus dictionary for topics when index or data is unavailable
SYLLABUS_FALLBACK: Dict[str, List[str]] = {
    "science": [
        "Chemical Reactions and Equations",
        "Acids, Bases and Salts",
        "Metals and Non-metals",
        "Carbon and its Compounds",
        "Life Processes",
        "Control and Coordination",
        "How do Organisms Reproduce?",
        "Heredity and Evolution",
        "Light – Reflection and Refraction",
        "The Human Eye and the Colorful World",
        "Electricity",
        "Magnetic Effects of Electric Current",
        "Our Environment"
    ],
    "mathematics": [
        "Real Numbers",
        "Polynomials",
        "Pair of Linear Equations in Two Variables",
        "Quadratic Equations",
        "Arithmetic Progressions",
        "Triangles",
        "Coordinate Geometry",
        "Introduction to Trigonometry",
        "Some Applications of Trigonometry",
        "Circles",
        "Areas Related to Circles",
        "Surface Areas and Volumes",
        "Statistics",
        "Probability"
    ]
}

def load_all_chunks() -> List[Dict[str, Any]]:
    """Load all chunks from ncert_chunks.json in the root directory."""
    if not os.path.exists(NCERT_CHUNKS_PATH):
        raise FileNotFoundError(f"NCERT chunks file not found at: {NCERT_CHUNKS_PATH}")
    
    with open(NCERT_CHUNKS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def load_chunks_by_subject(subject: str) -> List[Dict[str, Any]]:
    """
    Filter chunks by subject ('Science' or 'Mathematics'/'Maths') based on the 'source' field.
    """
    all_chunks = load_all_chunks()
    subj_lower = subject.strip().lower()
    
    filtered_chunks = []
    for chunk in all_chunks:
        source_lower = chunk.get("source", "").lower()
        if "math" in subj_lower:
            if "math" in source_lower:
                filtered_chunks.append(chunk)
        elif "sci" in subj_lower:
            if "sci" in source_lower:
                filtered_chunks.append(chunk)
        elif subj_lower in source_lower:
            filtered_chunks.append(chunk)
            
    return filtered_chunks

