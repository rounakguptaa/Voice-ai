import os
import tempfile
from typing import Optional

_WHISPER_MODEL = None

def get_whisper_model():
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        import whisper
        print("Loading Whisper 'base' model for STT...")
        _WHISPER_MODEL = whisper.load_model("base")
    return _WHISPER_MODEL

def transcribe_audio_bytes(audio_bytes: bytes, filename_hint: str = "input.wav") -> str:
    """
    Save audio bytes to a temporary file, transcribe using Whisper 'base' model,
    and clean up the temp file.
    """
    if not audio_bytes:
        return ""
        
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"temp_stt_{os.getpid()}_{filename_hint}")
    
    try:
        with open(temp_path, "wb") as f:
            f.write(audio_bytes)
            
        model = get_whisper_model()
        # Optimize transcription with a custom Hinglish science/math vocabulary prompt
        prompt_vocab = (
            "Class 10 NCERT Science and Maths syllabus doubts. Respiration, chemical reactions, "
            "equations, photosynthesis, quadratic equations, real numbers, trigonometry, metals, "
            "non-metals, acids, bases, carbon, coordinate geometry, electricity, magnetic effects, "
            "Hinglish language mix of Hindi and English."
        )
        result = model.transcribe(
            temp_path,
            fp16=False,
            temperature=0.0,
            initial_prompt=prompt_vocab
        )
        transcription = result.get("text", "").strip()
        return transcription
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return "Audio transcribe nahi ho paya. Kripya dobara koshish karein."
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
