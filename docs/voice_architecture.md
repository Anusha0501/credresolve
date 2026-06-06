# CredResolve AI - Voice Architecture

## Overview

The Voice AI module integrates Sarvam AI's speech services with the existing LangGraph-based debt collection agent, enabling natural Hindi and Hinglish voice interactions while preserving all existing functionality.

## Architecture Diagram

```
User Voice Input
    ↓
Sarvam Saaras v3 (Speech To Text)
    ↓
LangGraph Agent
    ↓
Gemini LLM
    ↓
RAG (ChromaDB)
    ↓
Tool Calling (CRM, Payment, Ticket, SMS)
    ↓
Memory Updates (SQLite)
    ↓
Sarvam Bulbul v3 (Text To Speech)
    ↓
User Audio Response
```

## Component Architecture

### 1. Voice Layer (Sarvam AI)

**Speech-to-Text (STT)**
- Model: Saaras v3
- Service: `SarvamSTTService`
- Location: `backend/services/sarvam_stt.py`
- Features:
  - Hindi support
  - Hinglish support
  - Code-mixed speech support
  - Error handling with retry mechanism
  - Mode: "codemix" (default) or "transcribe"

**Text-to-Speech (TTS)**
- Model: Bulbul v3
- Service: `SarvamTTSService`
- Location: `backend/services/sarvam_tts.py`
- Features:
  - Hindi language (hi-IN)
  - Multiple speakers (shubh, arjun, meera, priya, rahul)
  - Audio file generation
  - Audio URL generation
  - Error handling with retry mechanism

### 2. Voice Orchestrator

**Service**: `VoiceOrchestrator`
**Location**: `backend/services/voice_agent.py`

**Responsibilities**:
1. Receive audio input
2. Transcribe using Sarvam STT
3. Pass transcript to LangGraph agent
4. Execute complete agent pipeline:
   - RAG retrieval
   - Tool calls
   - Memory updates
5. Generate final response text
6. Convert response to speech using Sarvam TTS
7. Return transcript + response + audio + metadata

**Key Methods**:
- `process_voice_interaction()`: Complete voice pipeline
- `transcribe_audio_only()`: STT only
- `text_to_speech_only()`: TTS only

### 3. FastAPI Routes

**Router**: `voice_router`
**Location**: `backend/app/voice_routes.py`

**Endpoints**:

1. `POST /voice/transcribe`
   - Input: Audio file
   - Output: Transcript with metadata
   - Features: Hindi/Hinglish transcription

2. `POST /voice/chat`
   - Input: Audio file + phone number
   - Process: STT → LangGraph → Gemini → Tools → Memory → TTS
   - Output: Transcript, response, audio URL, state, tools, sources, latency

3. `POST /voice/tts`
   - Input: Text
   - Output: Audio file URL
   - Features: Hindi speech generation

4. `GET /voice/audio/{filename}`
   - Output: Audio file stream
   - Media type: audio/wav

5. `GET /voice/speakers`
   - Output: List of available TTS speakers

6. `GET /voice/metrics`
   - Output: Voice-specific metrics
   - Features: STT/TTS latency, success rates

### 4. React Frontend

**Component**: `VoiceChat`
**Location**: `frontend/src/pages/VoiceChat.tsx`

**Features**:
- Start/Stop recording (browser MediaRecorder API)
- Upload audio file
- Display transcript
- Display agent response
- Play audio response
- Show current state
- Show tools used
- Show retrieved documents
- Show latency metrics

**UI Components**:
- Phone number input
- Recording controls
- File upload
- Transcript display
- Response display with audio player
- State indicator
- Tool calls list
- Sources list
- Latency metrics

## Data Flow

### Voice Chat Flow

```
1. User speaks (Hindi/Hinglish)
   ↓
2. Frontend captures audio (MediaRecorder)
   ↓
3. Upload to POST /voice/chat
   ↓
4. Sarvam STT transcribes audio
   ↓
5. Transcript passed to LangGraph
   ↓
6. LangGraph executes state machine
   ↓
7. Gemini generates response
   ↓
8. RAG retrieves relevant documents
   ↓
9. Tools execute (CRM, Payment, etc.)
   ↓
10. Memory updates (SQLite)
   ↓
11. Sarvam TTS converts response to speech
   ↓
12. Audio file saved and URL generated
   ↓
13. Response returned to frontend
   ↓
14. Frontend displays transcript and plays audio
```

### State Preservation

Voice interactions preserve:
- Conversation memory (previous turns)
- User memory (preferences, language)
- State machine position (current state)
- Tool call history
- RAG retrieval context

This ensures voice conversations continue seamlessly from previous text or voice interactions.

## Integration Points

### With LangGraph

The voice orchestrator uses the existing LangGraph agent graph without modification:

```python
agent_graph = create_agent_graph()
result = agent_graph.invoke(initial_state)
```

The state is initialized with the transcript as the message, and all existing state transitions, tool calls, and memory operations work identically.

### With Memory

Voice conversations use the same SQLite memory layer:

```python
memory_db.save_conversation(
    phone_number,
    current_state,
    transcript,
    response_text,
    metadata
)
```

This ensures voice and text conversations share the same memory context.

### With RAG

Voice queries trigger the same RAG retrieval:

```python
retrieved_knowledge = knowledge_retriever.retrieve(query, top_k)
```

The transcript is used as the query for semantic search.

### With Tools

Voice interactions trigger the same tool calls:

```python
tool_calls = result.get("tool_calls", [])
```

All tools (CRM, Payment, Ticket, SMS) work identically for voice and text.

## Error Handling

### STT Errors

- Retry mechanism with exponential backoff
- Max 3 retries
- Fallback to text input if STT fails
- Error logging with metrics

### TTS Errors

- Retry mechanism with exponential backoff
- Max 3 retries
- Fallback to text response if TTS fails
- Error logging with metrics

### Agent Errors

- Existing LangGraph error handling
- Graceful degradation
- Error response returned to frontend
- Error logging with metrics

## Metrics and Observability

### Voice-Specific Metrics

Tracked via existing metrics system:

- `voice_stt_start`: STT request start
- `voice_stt_success`: STT success
- `voice_stt_error`: STT error
- `voice_tts_start`: TTS request start
- `voice_tts_success`: TTS success
- `voice_tts_error`: TTS error
- `voice_agent_start`: Agent processing start
- `voice_agent_success`: Agent success
- `voice_agent_error`: Agent error
- `voice_roundtrip_success`: Complete voice interaction success
- `voice_transcribe_only_start`: STT-only start
- `voice_transcribe_only_success`: STT-only success
- `voice_transcribe_only_error`: STT-only error
- `voice_tts_only_start`: TTS-only start
- `voice_tts_only_success`: TTS-only success
- `voice_tts_only_error`: TTS-only error

### Latency Metrics

- STT latency (seconds)
- TTS latency (seconds)
- Total roundtrip latency (seconds)

### Endpoint

`GET /voice/metrics` returns voice-specific metrics filtered from the main metrics system.

## Configuration

### Environment Variables

```env
SARVAM_API_KEY=your_sarvam_api_key_here
```

### Sarvam Models

**STT Model**: `saaras:v3`
- Supports Hindi
- Supports Hinglish
- Supports code-mixed speech
- Mode: "codemix" (default) or "transcribe"

**TTS Model**: `bulbul:v3`
- Language: hi-IN (Hindi)
- Speakers: shubh (default), arjun, meera, priya, rahul
- Output format: WAV

### Audio Storage

Generated audio files stored in: `backend/audio_uploads/`
- Served via: `GET /voice/audio/{filename}`
- Cleanup: Manual or scheduled task (not implemented)

## Security Considerations

### API Key Management

- SARVAM_API_KEY stored in environment variables
- Never hardcoded in source code
- Loaded via python-dotenv
- Included in .env.example for reference

### File Upload Security

- File size limits (can be added)
- File type validation (audio/*)
- Temporary file cleanup
- No execution of uploaded files

### CORS Configuration

- Existing CORS middleware applies
- Voice routes inherit CORS settings
- Configured for development (allow all origins)
- Should be restricted in production

## Performance Considerations

### Latency Optimization

- Async processing (can be enhanced)
- Audio compression (can be added)
- Caching of TTS responses (can be added)
- Streaming audio (can be added)

### Scalability

- Sarvam API rate limits
- Audio storage scaling
- Concurrent voice sessions
- Load balancing (for production)

## Future Enhancements

### Short-term

1. Audio compression for faster upload/download
2. Streaming TTS for lower latency
3. Audio file cleanup job
4. Voice activity detection
5. Noise reduction

### Long-term

1. Real-time streaming STT
2. WebSocket-based voice communication
3. Multi-language support (beyond Hindi)
4. Voice biometrics for authentication
5. Sentiment analysis from voice
6. Custom voice training

## Testing

### Unit Tests

- STT service tests
- TTS service tests
- Voice orchestrator tests
- Error handling tests

### Integration Tests

- Voice chat end-to-end
- State preservation
- Memory integration
- Tool integration
- RAG integration

### Voice Scenarios

Test with Hindi phrases:
- "Meri salary late aayi hai" (Payment delay)
- "Mujhe agle hafte tak time chahiye" (Request extension)
- "Maine payment kar diya hai" (Payment confirmation)
- "Mujhe settlement option chahiye" (Settlement request)
- "Mujhe baar baar call mat kariye" (Do not call preference)

## Troubleshooting

### Common Issues

1. **SARVAM_API_KEY not set**
   - Check .env file
   - Verify environment variable loading

2. **Audio file not uploading**
   - Check file size limits
   - Verify file type
   - Check network connectivity

3. **STT not transcribing**
   - Verify audio quality
   - Check Sarvam API status
   - Review error logs

4. **TTS not generating audio**
   - Verify text is not empty
   - Check Sarvam API status
   - Review error logs

5. **Audio not playing**
   - Check audio URL
   - Verify file exists
   - Check browser audio support

## Conclusion

The Voice AI module seamlessly integrates Sarvam AI's speech services with the existing LangGraph-based debt collection agent, enabling natural Hindi and Hinglish voice interactions while preserving all existing functionality including state management, memory persistence, RAG retrieval, and tool execution.

The architecture is modular, maintainable, and production-ready with proper error handling, metrics tracking, and security considerations.
