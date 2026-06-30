import os
import tempfile
from typing import Optional
from backend.config import GROQ_API_KEY

def transcribe_audio_bytes(audio_bytes: bytes, filename_hint: str = "input.wav") -> str:
    """
    Transcribe audio bytes using Groq's Cloud Whisper API.
    Saves a local temp file, pushes it to Groq API, and cleans up the temp file.
    """
    if not audio_bytes:
        return ""
        
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_your_api_key_here") or not GROQ_API_KEY.strip():
        print("Groq API key not configured for STT. Falling back to default query.")
        return "Audio transcribe nahi ho paya. API key configured nahi hai."

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"temp_stt_{os.getpid()}_{filename_hint}")
    
    try:
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
            
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        
        # Optimize transcription with a custom Hinglish science/math vocabulary prompt
        prompt_vocab = (
            "Class 10 NCERT Science and Maths syllabus doubts. Respiration, chemical reactions, "
            "equations, photosynthesis, quadratic equations, real numbers, trigonometry, metals, "
            "non-metals, acids, bases, carbon, coordinate geometry, electricity, magnetic effects, "
            "Hinglish language mix of Hindi and English."
        )
        
        with open(temp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename_hint, audio_file.read()),
                model="whisper-large-v3",
                prompt=prompt_vocab,
                response_format="json"
            )
            
        return transcription.text.strip()
    except Exception as e:
        print(f"Error during Groq audio transcription: {e}")
        return "Audio transcribe nahi ho paya. Kripya dobara koshish karein."
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
