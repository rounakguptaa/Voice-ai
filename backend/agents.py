from typing import List, Dict, Any
from backend.config import GROQ_API_KEY

def generate_subject_explanation(query: str, subject: str, chunks: List[Dict[str, Any]]) -> str:
    """
    Generate Hinglish explanation using Groq (llama-3.1-8b-instant) if API key is provided,
    otherwise fallback to robust template-based NCERT chunk synthesis.
    """
    subj_key = subject.strip().lower()
    
    if not chunks:
        return f"Beta, {subject.capitalize()} ke is topic par textbook mein explicit content abhi mil nahi paya. Kripya apne teacher se zaroor discuss karein!"
        
    combined_context = "\n".join([c.get("text", "") for c in chunks])
    clean_context = " ".join(combined_context.split())
    
    # Check if a valid Groq API key is configured
    if GROQ_API_KEY and not GROQ_API_KEY.startswith("gsk_your_api_key_here") and GROQ_API_KEY.strip():
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            
            system_prompt = (
                f"You are GuruAI, an encouraging Smart Board Teaching Assistant for Class 10 {subject.capitalize()} "
                "in a Haryana government school. Explain the concept to the student in friendly Hinglish (mix of Hindi and English) "
                "using clear markdown bullet points, cause-effect examples for Science, or step-by-step formulas and calculations for Math. "
                "Keep it highly readable, clear, and structured for classroom display. "
                "Keep the explanation under 150 words and base it strictly on the provided NCERT textbook context."
            )
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"NCERT Chunks Context:\n{clean_context}\n\nStudent Query: {query}"}
                ],
                temperature=0.3
            )
            explanation = completion.choices[0].message.content.strip()
            return explanation
        except Exception as e:
            print(f"Groq API call failed: {e}. Falling back to template explanation.")

    # Template Fallback
    if subj_key == "science":
        explanation = (
            f" Namaste Vidyarthi! Chaliye **Class 10 Science** ke is mazedar topic ko samajhte hain!\n\n"
            f"** Aapka Sawal:** '{query}'\n\n"
            f"🔬 **Mukhya Vigyanik Karan (Cause-Effect & Phenomena):**\n"
            f"{clean_context[:450]}...\n\n"
            f"💡 **Real-World Example (Rozmarra ki Zindagi mein):**\n"
            f"Hum apne aas-paas ke vatavaran mein is kriya (phenomenon) ko dekh sakte hain. "
            f"Jab hum is prakriya ko samajhte hain, toh vigyan hamari rozmarra ki zindagi se jud jata hai!\n\n"
            f"🎯 **Key Takeaway:** Vigyan mein 'kyun' aur 'kaise' samajhna sabse zaroori hai. Shabaash, padhte rahiye!"
        )
    else: # Mathematics
        explanation = (
            f" Namaste Vidyarthi! Chaliye **Class 10 Mathematics** ke is problem ko step-by-step hal karte hain!\n\n"
            f"** Aapka Sawal:** '{query}'\n\n"
            f"📐 **Step-by-Step Derivation & Formulas (Niyam aur Sutra):**\n"
            f"{clean_context[:450]}...\n\n"
            f"✍️ **Problem Solving Tip:**\n"
            f"Ganit mein hamesha given data ko dhyan se likhein, sahi formula apply karein, aur calculation step-by-step karein taaki koi galti na ho!\n\n"
            f"🎯 **Key Takeaway:** Practice makes perfect! Is formula par 2-3 extra question zaroor solve karein."
        )
        
    return explanation

