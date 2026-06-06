import os
import time
import uuid
from typing import Optional, Dict
from sarvamai import SarvamAI
from app.config import config

class SarvamTTSService:
    """Sarvam AI Text-to-Speech Service using Bulbul v3"""
    
    def __init__(self):
        self.api_key = os.getenv("SARVAM_API_KEY")
        if not self.api_key:
            raise ValueError("SARVAM_API_KEY environment variable not set")
        
        self.client = SarvamAI(api_key=self.api_key)
        self.model = "bulbul:v3"
        self.language = "hi-IN"
        self.default_speaker = "shubh"
        self.audio_output_dir = "audio_uploads"
        
        # Create audio output directory if it doesn't exist
        os.makedirs(self.audio_output_dir, exist_ok=True)
    
    def generate_speech(
        self,
        text: str,
        speaker: str = "shubh",
        language: str = "hi-IN"
    ) -> Dict:
        """
        Generate speech from text using Sarvam Bulbul v3
        
        Args:
            text: Text to convert to speech
            speaker: Speaker voice (default: shubh)
            language: Language code (default: hi-IN)
        
        Returns:
            Dict containing audio file path and metadata
        """
        start_time = time.time()
        
        try:
            # Call Sarvam TTS API
            response = self.client.audio.speech.create(
                text=text,
                model=self.model,
                speaker=speaker,
                language=language
            )
            
            latency = time.time() - start_time
            
            # Save audio file
            audio_filename = f"{uuid.uuid4()}.wav"
            audio_file_path = os.path.join(self.audio_output_dir, audio_filename)
            
            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(response.content)
            
            # Generate audio URL (relative path)
            audio_url = f"/audio/{audio_filename}"
            
            return {
                "success": True,
                "audio_file_path": audio_file_path,
                "audio_url": audio_url,
                "text": text,
                "speaker": speaker,
                "language": language,
                "latency": latency,
                "model": self.model
            }
        
        except Exception as e:
            latency = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "audio_file_path": "",
                "audio_url": "",
                "latency": latency
            }
    
    def save_audio(self, audio_data: bytes, filename: Optional[str] = None) -> Dict:
        """
        Save audio data to file
        
        Args:
            audio_data: Audio data as bytes
            filename: Optional custom filename
        
        Returns:
            Dict containing file path and URL
        """
        try:
            if filename is None:
                filename = f"{uuid.uuid4()}.wav"
            
            audio_file_path = os.path.join(self.audio_output_dir, filename)
            
            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(audio_data)
            
            audio_url = f"/audio/{filename}"
            
            return {
                "success": True,
                "audio_file_path": audio_file_path,
                "audio_url": audio_url
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "audio_file_path": "",
                "audio_url": ""
            }
    
    def generate_speech_with_retry(
        self,
        text: str,
        speaker: str = "shubh",
        language: str = "hi-IN",
        max_retries: int = 3
    ) -> Dict:
        """
        Generate speech with retry mechanism
        
        Args:
            text: Text to convert to speech
            speaker: Speaker voice
            language: Language code
            max_retries: Maximum retry attempts
        
        Returns:
            Dict containing audio file path and metadata
        """
        for attempt in range(max_retries):
            result = self.generate_speech(text, speaker, language)
            
            if result["success"]:
                return result
            
            # If failed and not last attempt, wait and retry
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            
            # All retries failed
            return result
    
    def get_available_speakers(self) -> list:
        """
        Get list of available speakers for Bulbul v3
        
        Returns:
            List of speaker names
        """
        # Common speakers for Bulbul v3 Hindi
        return [
            "shubh",
            "arjun",
            "meera",
            "priya",
            "rahul"
        ]

# Global instance
sarvam_tts_service = SarvamTTSService()
