import time
import os
from typing import Dict, Optional
from app.agent.graph import create_agent_graph
from app.agent.state import AgentState
from app.services.sarvam_stt import sarvam_stt_service
from app.services.sarvam_tts import sarvam_tts_service
from app.memory.database import memory_db
from app.monitoring.metrics import track_metric

class VoiceOrchestrator:
    """Orchestrates voice interactions through the debt collection agent"""
    
    def __init__(self):
        self.agent_graph = create_agent_graph()
        self.stt_service = sarvam_stt_service
        self.tts_service = sarvam_tts_service
    
    def process_voice_interaction(
        self,
        audio_file_path: str,
        phone_number: str,
        language: str = "hi-IN"
    ) -> Dict:
        """
        Complete voice interaction pipeline:
        1. Transcribe audio using Sarvam STT
        2. Pass transcript to LangGraph agent
        3. Execute RAG, Tool Calls, Memory Updates
        4. Generate final response text
        5. Convert response to speech using Sarvam TTS
        6. Return transcript + response + audio
        
        Args:
            audio_file_path: Path to uploaded audio file
            phone_number: User's phone number
            language: Language code (default: hi-IN)
        
        Returns:
            Dict containing transcript, response, audio_url, and metadata
        """
        total_start_time = time.time()
        
        # Step 1: Transcribe audio using Sarvam STT
        track_metric("voice_stt_start", {"phone_number": phone_number})
        stt_result = self.stt_service.convert_audio_to_text(
            audio_file_path,
            mode="codemix",
            language=language
        )
        
        if not stt_result["success"]:
            track_metric("voice_stt_error", {"phone_number": phone_number, "error": stt_result["error"]})
            return {
                "success": False,
                "error": "STT failed",
                "details": stt_result
            }
        
        transcript = stt_result["transcript"]
        track_metric("voice_stt_success", {"phone_number": phone_number, "latency": stt_result["latency"]})
        
        # Step 2: Pass transcript to LangGraph agent
        track_metric("voice_agent_start", {"phone_number": phone_number})
        
        # Initialize state with transcript
        initial_state: AgentState = {
            "phone_number": phone_number,
            "current_state": "",
            "customer_data": None,
            "conversation_history": [{"message": transcript, "timestamp": time.time()}],
            "user_memory": None,
            "retrieved_knowledge": [],
            "tool_calls": [],
            "agent_response": "",
            "next_state": "",
            "metadata": {"language": language, "mode": "voice"},
            "timestamp": time.time()
        }
        
        # Run agent graph
        try:
            agent_result = self.agent_graph.invoke(initial_state)
            track_metric("voice_agent_success", {"phone_number": phone_number})
        except Exception as e:
            track_metric("voice_agent_error", {"phone_number": phone_number, "error": str(e)})
            return {
                "success": False,
                "error": "Agent execution failed",
                "transcript": transcript,
                "details": str(e)
            }
        
        response_text = agent_result.get("agent_response", "")
        current_state = agent_result.get("current_state", "")
        tool_calls = agent_result.get("tool_calls", [])
        retrieved_knowledge = agent_result.get("retrieved_knowledge", [])
        
        # Step 3: Save conversation to memory
        memory_db.save_conversation(
            phone_number,
            current_state,
            transcript,
            response_text,
            agent_result.get("metadata", {})
        )
        
        # Step 4: Convert response to speech using Sarvam TTS
        track_metric("voice_tts_start", {"phone_number": phone_number})
        tts_result = self.tts_service.generate_speech(
            text=response_text,
            speaker="shubh",
            language=language
        )
        
        if not tts_result["success"]:
            track_metric("voice_tts_error", {"phone_number": phone_number, "error": tts_result["error"]})
            # Return text response even if TTS fails
            total_latency = time.time() - total_start_time
            return {
                "success": True,
                "transcript": transcript,
                "response": response_text,
                "audio_url": None,
                "current_state": current_state,
                "tools_used": tool_calls,
                "sources": retrieved_knowledge,
                "latency": {
                    "stt": stt_result["latency"],
                    "agent": 0,  # Would need to track this
                    "tts": tts_result["latency"],
                    "total": total_latency
                }
            }
        
        track_metric("voice_tts_success", {"phone_number": phone_number, "latency": tts_result["latency"]})
        
        total_latency = time.time() - total_start_time
        track_metric("voice_roundtrip_success", {
            "phone_number": phone_number,
            "total_latency": total_latency
        })
        
        # Step 5: Return complete response
        return {
            "success": True,
            "transcript": transcript,
            "response": response_text,
            "audio_url": tts_result["audio_url"],
            "current_state": current_state,
            "tools_used": tool_calls,
            "sources": retrieved_knowledge,
            "latency": {
                "stt": stt_result["latency"],
                "tts": tts_result["latency"],
                "total": total_latency
            }
        }
    
    def transcribe_audio_only(
        self,
        audio_file_path: str,
        language: str = "hi-IN"
    ) -> Dict:
        """
        Transcribe audio only without agent processing
        
        Args:
            audio_file_path: Path to audio file
            language: Language code
        
        Returns:
            Dict containing transcript
        """
        track_metric("voice_transcribe_only_start", {})
        
        result = self.stt_service.convert_audio_to_text(
            audio_file_path,
            mode="codemix",
            language=language
        )
        
        if result["success"]:
            track_metric("voice_transcribe_only_success", {"latency": result["latency"]})
        else:
            track_metric("voice_transcribe_only_error", {"error": result["error"]})
        
        return result
    
    def text_to_speech_only(
        self,
        text: str,
        speaker: str = "shubh",
        language: str = "hi-IN"
    ) -> Dict:
        """
        Convert text to speech only without agent processing
        
        Args:
            text: Text to convert
            speaker: Speaker voice
            language: Language code
        
        Returns:
            Dict containing audio file info
        """
        track_metric("voice_tts_only_start", {})
        
        result = self.tts_service.generate_speech(
            text=text,
            speaker=speaker,
            language=language
        )
        
        if result["success"]:
            track_metric("voice_tts_only_success", {"latency": result["latency"]})
        else:
            track_metric("voice_tts_only_error", {"error": result["error"]})
        
        return result

# Global instance
voice_orchestrator = VoiceOrchestrator()
