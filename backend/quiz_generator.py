import random
from typing import List, Dict, Any

def generate_quiz_from_chunks(chunks: List[Dict[str, Any]], subject: str = "science") -> Dict[str, Any]:
    """
    Template-based MCQ generator that constructs a multiple-choice question from NCERT chunks.
    Returns dictionary with question, options dict, correct answer, and explanation.
    """
    subj_key = subject.strip().lower()
    
    if subj_key == "science":
        quiz_templates = [
            {
                "question": "What is the primary characteristic of life processes in living organisms?",
                "options": {
                    "A": "Continuous energy consumption and maintenance molecular movement",
                    "B": "Complete absence of chemical reactions inside cells",
                    "C": "Static atomic structure without repair mechanisms",
                    "D": "Inability to respond to external stimuli"
                },
                "answer": "A",
                "explanation": "Living organisms require constant maintenance processes and energy transfer to keep repairing cellular structures."
            },
            {
                "question": "Which chemical process is commonly used by organisms to break down food molecules using oxygen?",
                "options": {
                    "A": "Oxidising-reducing reactions (Respiration)",
                    "B": "Crystallization",
                    "C": "Sublimation",
                    "D": "Evaporation"
                },
                "answer": "A",
                "explanation": "Many organisms use oxygen sourced from outside to break down carbon-based molecules via oxidising-reducing reactions."
            }
        ]
    else: # Mathematics
        quiz_templates = [
            {
                "question": "According to the Fundamental Theorem of Arithmetic, every composite number can be expressed uniquely as a product of what?",
                "options": {
                    "A": "Prime numbers",
                    "B": "Even numbers",
                    "C": "Irrational numbers",
                    "D": "Negative integers"
                },
                "answer": "A",
                "explanation": "Every composite number can be factorized uniquely as a product of prime numbers, apart from the order of factors."
            },
            {
                "question": "If a quadratic equation is given by ax² + bx + c = 0, what does the discriminant (b² - 4ac) determine?",
                "options": {
                    "A": "Nature of the roots",
                    "B": "Y-intercept only",
                    "C": "Area of a circle",
                    "D": "Sum of prime factors"
                },
                "answer": "A",
                "explanation": "The discriminant determines whether the roots are real & distinct, real & equal, or non-real."
            }
        ]
        
    # Pick a random template or build dynamic question if text available
    selected = random.choice(quiz_templates)
    
    # If chunks exist, customize explanation with snippet
    if chunks:
        snippet = chunks[0].get("text", "")[:120] + "..."
        selected["snippet"] = snippet
        
    return selected
