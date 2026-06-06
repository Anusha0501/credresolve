import os
import time
from typing import Optional, Dict
from sarvamai import SarvamAI
from app.config import config

class SarvamSTTService:
    """Sarvam AI Speech-to-Text Service using Saaras v3"""
    
    def __init__(self):
        self.api_key = os.getenv("SARVAM_API_KEY")
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY environment variable not set")
        
        self.client = SarvamAI(api_key=self.api_key)
        self.model = "saaras:v3"
        self.default_mode = "codemix"  # Supports Hindi, Hinglish, code-mixed speech
    
    def transcribe_audio(
        self,
        audio_file_path: str,
        mode: str = "codemix",
        language: str = "hi-IN"
    ) -> Dict:
        """
        Transcribe audio file to text using Sarvam Saaras v3
        
        Args:
            audio_file_path: Path to audio file
            mode: "transcribe" or "codemix" (default: codemix)
            language: Language code (default: hi-IN for Hindi)
        
        Returns:
            Dict containing transcript and metadata
        """
        start_time = time.time()
        
        try:
            # Read audio file
            with open(audio_file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Call Sarvam STT API
            response = self.client.audio.transcriptions.create(
                file=audio_data,
                model=self.model,
                language=language,
                mode=mode
            )
            
            latency = time.time() - start_time
            
            return {
                "success": True,
                "transcript": response.text,
                "language": language,
                "mode": mode,
                "latency": latency,
                "model": self.model
            }
        
        except Exception as e:
            latency = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "transcript": "",
                "latency": latency
            }
    
    def convert_audio_to_text(
        self,
        audio_file_path: str,
        mode: str = "codemix",
        language: str = "hi-IN",
        max_retries: int = 3
    ) -> Dict:
        """
        Convert audio to text with retry mechanism
        
        Args:
            audio_file_path: Path to audio file
            mode: "transcribe" or "codemix"
            language: Language code
            max_retries: Maximum number of retry attempts
        
        Returns:
            Dict containing transcript and metadata
        """
        for attempt in range(max_retries):
            result = self.transcribe_audio(audio_file_path, mode, language)
            
            if result["success"]:
                return result
            
            # If failed and not last attempt, wait and retry
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            # All retries failed
            return result
    
    def transcribe_base64_audio(
        self,
        audio_base64: str,
        mode: str = "codemix",
        language: str = "hi-IN"
    ) -> Dict:
        """
        Transcribe base64-encoded audio
        
        Args:
            audio_base64: Base64-encoded audio data
            mode: "transcribe" or "codemix"
            language: Language code
        
        Returns:
            Dict containing transcript and metadata
        """
        import base64
        import tempfile
        
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(audio_base64)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # Transcribe
            result = self.convert_audio_to_text(temp_file_path, mode, language)
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "transcript": ""
            }

# Global instance
sarvam_stt_service = SarvamSTTService()
