from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from app.services.voice_agent import voice_orchestrator
from app.services.sarvam_stt import sarvam_stt_service
from app.services.sarvam_tts import sarvam_tts_service
from app.monitoring.metrics import track_metric

router = APIRouter(prefix="/voice", tags=["voice"])

# Request/Response models
class TTSRequest(BaseModel):
    text: str
    speaker: str = "shubh"
    language: str = "hi-IN"

class VoiceChatRequest(BaseModel):
    phone_number: str
    language: str = "hi-IN"

# Create audio uploads directory if it doesn't exist
UPLOAD_DIR = "audio_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = "hi-IN"
):
    """
    Transcribe audio file to text using Sarvam Saaras v3
    
    - Supports Hindi and Hinglish
    - Code-mixed speech support
    - Returns transcript with metadata
    """
    track_metric("voice_transcribe_endpoint", {})
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"temp_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribe
        result = sarvam_stt_service.convert_audio_to_text(file_path, language=language)
        
        # Clean up temp file
        os.remove(file_path)
        
        if result["success"]:
            return {
                "transcript": result["transcript"],
                "language": result["language"],
                "mode": result["mode"],
                "latency": result["latency"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
    
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def voice_chat(
    file: UploadFile = File(...),
    phone_number: str = "",
    language: str = "hi-IN"
):
    """
    Complete voice chat pipeline:
    1. Transcribe audio using Sarvam STT
    2. Process through LangGraph agent
    3. Execute RAG, Tool Calls, Memory Updates
    4. Generate response using Gemini
    5. Convert response to speech using Sarvam TTS
    
    Returns transcript, response text, and audio URL
    """
    track_metric("voice_chat_endpoint", {"phone_number": phone_number})
    
    if not phone_number:
        raise HTTPException(status_code=400, detail="phone_number is required")
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, f"chat_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process voice interaction
        result = voice_orchestrator.process_voice_interaction(
            audio_file_path=file_path,
            phone_number=phone_number,
            language=language
        )
        
        # Clean up temp file
        os.remove(file_path)
        
        if result["success"]:
            return {
                "transcript": result["transcript"],
                "response": result["response"],
                "audio_url": result["audio_url"],
                "current_state": result["current_state"],
                "tools_used": result["tools_used"],
                "sources": result["sources"],
                "latency": result["latency"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Voice chat failed"))
    
    except Exception as e:
        # Clean up temp file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Sarvam Bulbul v3
    
    - Supports Hindi
    - Returns audio file URL
    """
    track_metric("voice_tts_endpoint", {})
    
    result = sarvam_tts_service.generate_speech(
        text=request.text,
        speaker=request.speaker,
        language=request.language
    )
    
    if result["success"]:
        return {
            "audio_url": result["audio_url"],
            "speaker": result["speaker"],
            "language": result["language"],
            "latency": result["latency"]
        }
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Serve generated audio files
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path, media_type="audio/wav")

@router.get("/speakers")
async def get_speakers():
    """
    Get list of available speakers for TTS
    """
    speakers = sarvam_tts_service.get_available_speakers()
    return {"speakers": speakers}

@router.get("/metrics")
async def get_voice_metrics():
    """
    Get voice-specific metrics
    """
    from app.monitoring.metrics import metrics_tracker
    
    summary = metrics_tracker.get_metrics_summary()
    
    # Filter for voice-related metrics
    voice_metrics = {
        "counters": {},
        "recent_metrics": {}
    }
    
    for key, value in summary["counters"].items():
        if "voice" in key.lower() or "stt" in key.lower() or "tts" in key.lower():
            voice_metrics["counters"][key] = value
    
    for key, events in summary["recent_metrics"].items():
        if "voice" in key.lower() or "stt" in key.lower() or "tts" in key.lower():
            voice_metrics["recent_metrics"][key] = events
    
    return voice_metrics
