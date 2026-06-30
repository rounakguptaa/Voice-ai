import os
import time
import asyncio
import edge_tts
from gtts import gTTS
from backend.config import TEMP_AUDIO_DIR

async def _edge_tts_async(text: str, output_path: str, voice: str = "hi-IN-SwaraNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_tts_audio(text: str, filename_prefix: str = "response") -> str:
    """
    Generate TTS audio file using edge-tts (hi-IN-SwaraNeural).
    Falls back to gTTS if edge-tts fails.
    Saves audio to TEMP_AUDIO_DIR and returns the relative filename.
    """
    filename = f"{filename_prefix}_{int(time.time()*1000)}.mp3"
    output_path = os.path.join(TEMP_AUDIO_DIR, filename)
    
    # Try Edge TTS first
    try:
        # Check if there's already an active event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
            
        if loop and loop.is_running():
            # Use run_until_complete in a separate thread or new loop executor if needed, or nest_asyncio
            # Or use concurrent.futures
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                pool.submit(lambda: asyncio.run(_edge_tts_async(text, output_path))).result()
        else:
            asyncio.run(_edge_tts_async(text, output_path))
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return filename
    except Exception as e:
        print(f"Edge TTS failed with error: {e}. Falling back to gTTS...")
        
    # Fallback to gTTS
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save(output_path)
        return filename
    except Exception as e2:
        print(f"gTTS fallback also failed with error: {e2}")
        return ""
