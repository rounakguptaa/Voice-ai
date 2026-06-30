import os
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import TEMP_AUDIO_DIR
from backend.stt_handler import transcribe_audio_bytes
from backend.rag_engine import process_rag_query
from backend.agents import generate_subject_explanation
from backend.visual_generator import generate_concept_visual
from backend.quiz_generator import generate_quiz_from_chunks
from backend.tts_handler import generate_tts_audio

app = FastAPI(title="GuruAI - Voice-Enabled AI Teaching Assistant Backend")

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated TTS audio files
app.mount("/audio", StaticFiles(directory=TEMP_AUDIO_DIR), name="audio")

from typing import Optional

@app.post("/process-voice")
async def process_voice_endpoint(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text_query: Optional[str] = Form(None),
    class_id: str = Form("10"),
    subject: str = Form("science"),
    mode: str = Form("explain")
):
    """
    Main pipeline endpoint: Audio STT / Direct Text -> Guardrails/RAG -> Explanation Generation -> Visual summary card -> TTS audio synthesis.
    """
    subject_clean = subject.strip().lower()
    
    query_text = ""
    # 1. Prioritize text queries first (e.g. from syllabus explorer clicks)
    if text_query is not None and text_query.strip():
        query_text = text_query.strip()
    # 2. Otherwise read and transcribe voice audio file
    elif file is not None:
        try:
            audio_bytes = await file.read()
            if audio_bytes and len(audio_bytes) > 0:
                query_text = transcribe_audio_bytes(audio_bytes, filename_hint=file.filename or "input.wav")
        except Exception as e:
            print(f"Error reading file bytes: {e}")
            
    if not query_text or "Audio transcribe nahi ho paya" in query_text:
        query_text = "What is respiration in human body?" if subject_clean == "science" else "What is the fundamental theorem of arithmetic?"
        
    print(f"Active Query: {query_text} | Subject: {subject} | Mode: {mode}")
    
    # 3. Apply relevance guardrails and retrieve matching NCERT chunks
    rag_result = process_rag_query(query_text, subject=subject_clean, threshold=0.6)
    blocked_flag = rag_result["blocked_flag"]
    
    if blocked_flag:
        rejection_msg = rag_result["rejection_message"]
        # Generate TTS audio for the rejection message
        audio_filename = generate_tts_audio(rejection_msg, filename_prefix="blocked")
        base_url = str(request.base_url)
        audio_url = f"{base_url}audio/{audio_filename}" if audio_filename else ""
        
        return {
            "user_query": query_text,
            "text_response": rejection_msg,
            "audio_url": audio_url,
            "visual_base64": "",
            "quiz_data": None,
            "blocked_flag": True
        }
        
    retrieved_chunks = rag_result["retrieved_chunks"]
    
    # 4. Generate subject-specific Hinglish response
    response_text = generate_subject_explanation(query_text, subject=subject_clean, chunks=retrieved_chunks)
    
    # 5. Generate Matplotlib visual summary card (Base64)
    visual_b64 = generate_concept_visual(query_text, response_text, subject=subject_clean)
    
    # 6. Generate TTS response audio
    clean_audio_text = response_text.replace("**", "").replace("###", "").replace("🔬", "").replace("💡", "").replace("🎯", "")
    # Keep it reasonably concise for fast audio generation
    shortened_tts_text = clean_audio_text[:280] + "..." if len(clean_audio_text) > 300 else clean_audio_text
    
    audio_filename = generate_tts_audio(shortened_tts_text, filename_prefix=f"{subject_clean}_explain")
    base_url = str(request.base_url)
    audio_url = f"{base_url}audio/{audio_filename}" if audio_filename else ""
    
    # 7. Generate Quiz Card
    quiz_data = generate_quiz_from_chunks(retrieved_chunks, subject=subject_clean)
    
    return {
        "user_query": query_text,
        "text_response": response_text,
        "audio_url": audio_url,
        "visual_base64": visual_b64,
        "quiz_data": quiz_data,
        "blocked_flag": False
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "GuruAI"}
