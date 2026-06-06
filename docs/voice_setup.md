# CredResolve AI - Voice Setup Guide

## Overview

This guide provides step-by-step instructions for setting up the Voice AI module with Sarvam AI integration for the CredResolve Debt Collection Agent.

## Prerequisites

- Python 3.12+
- Node.js 18+
- Sarvam AI API Key
- Existing CredResolve backend and frontend setup

## Step 1: Get Sarvam AI API Key

1. Visit [Sarvam AI](https://sarvam.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the API key

## Step 2: Install Sarvam AI SDK

### Backend Installation

```bash
cd backend

# Install Sarvam AI SDK
pip install -U sarvamai

# Or update requirements.txt and install
pip install -r requirements.txt
```

### Verify Installation

```bash
python -c "import sarvamai; print('Sarvam AI SDK installed successfully')"
```

## Step 3: Configure Environment Variables

### Create/Update .env File

```bash
cd backend
cp .env.example .env
```

### Edit .env File

```env
GEMINI_API_KEY=your_gemini_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here
```

**Important**: Never commit .env file to version control. It's already in .gitignore.

## Step 4: Backend Setup

### Directory Structure

The voice module requires the following directory structure:

```
backend/
├── services/
│   ├── __init__.py
│   ├── sarvam_stt.py
│   ├── sarvam_tts.py
│   └── voice_agent.py
├── audio_uploads/
└── app/
    └── voice_routes.py
```

### Create Directories

```bash
cd backend
mkdir -p services audio_uploads
```

### Verify Files

Ensure the following files exist:
- `backend/services/sarvam_stt.py`
- `backend/services/sarvam_tts.py`
- `backend/services/voice_agent.py`
- `backend/app/voice_routes.py`

### Update Main Application

The `backend/app/main.py` should include:
```python
from app.voice_routes import router as voice_router
app.include_router(voice_router)
```

### Update Configuration

The `backend/app/config.py` should include:
```python
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
```

## Step 5: Frontend Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Verify VoiceChat Component

Ensure `frontend/src/pages/VoiceChat.tsx` exists.

### Update App.jsx

The `frontend/src/App.jsx` should include:
```javascript
import VoiceChat from './pages/VoiceChat'
import { Mic } from 'lucide-react'
```

And add the route:
```javascript
<Route path="/voice" element={<VoiceChat />} />
```

And add navigation link:
```javascript
<Link to="/voice" className="flex items-center space-x-1 hover:text-gray-200">
  <Mic className="w-5 h-5" />
  <span>Voice</span>
</Link>
```

## Step 6: Start Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
```

The backend should start on `http://localhost:8000`

### Verify Voice Endpoints

Test the voice endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Voice metrics
curl http://localhost:8000/voice/metrics

# Get speakers
curl http://localhost:8000/voice/speakers
```

Expected response for speakers:
```json
{
  "speakers": ["shubh", "arjun", "meera", "priya", "rahul"]
}
```

## Step 7: Start Frontend Server

```bash
cd frontend
npm run dev
```

The frontend should start on `http://localhost:3000`

## Step 8: Test Voice Features

### Test STT (Speech-to-Text)

1. Navigate to Voice Chat page
2. Enter phone number: `+919876543210`
3. Click "Start Recording"
4. Speak in Hindi: "Namaste, main Rajesh bol raha hoon"
5. Click "Stop Recording"
6. Wait for transcription
7. Verify transcript appears

### Test TTS (Text-to-Speech)

1. Use the text chat interface
2. Send a message
3. Click "Speak Last Response" button
4. Verify audio plays

### Test Complete Voice Chat

1. Navigate to Voice Chat page
2. Enter phone number: `+919876543210`
3. Click "Start Recording"
4. Speak: "Meri salary late aayi hai"
5. Click "Stop Recording"
6. Wait for processing
7. Verify:
   - Transcript appears
   - Agent response appears
   - Audio plays automatically
   - Current state displayed
   - Tools used shown
   - Sources shown
   - Latency metrics shown

### Test File Upload

1. Prepare an audio file (WAV format)
2. Navigate to Voice Chat page
3. Enter phone number
4. Click "Upload Audio"
5. Select audio file
6. Wait for processing
7. Verify response

## Step 9: Test Hindi Scenarios

### Scenario 1: Payment Delay

**Input**: "Meri salary late aayi hai"
**Expected**: Agent understands payment delay, offers solutions

### Scenario 2: Request Extension

**Input**: "Mujhe agle hafte tak time chahiye"
**Expected**: Agent creates Promise to Pay, schedules callback

### Scenario 3: Payment Confirmation

**Input**: "Maine payment kar diya hai"
**Expected**: Agent runs payment verification tool

### Scenario 4: Settlement Request

**Input**: "Mujhe settlement option chahiye"
**Expected**: Agent uses RAG, retrieves settlement policy

### Scenario 5: Do Not Call Preference

**Input**: "Mujhe baar baar call mat kariye"
**Expected**: Agent logs callback preference, schedules follow-up

## Step 10: Verify Metrics

### Check Voice Metrics

```bash
curl http://localhost:8000/voice/metrics
```

Expected output includes:
- STT success/error counts
- TTS success/error counts
- Voice roundtrip counts
- Latency measurements

### Check General Metrics

```bash
curl http://localhost:8000/metrics
```

Voice metrics should appear in the general metrics output.

## Troubleshooting

### SARVAM_API_KEY Error

**Error**: `SARVAM_API_KEY environment variable not set`

**Solution**:
1. Check .env file exists in backend directory
2. Verify SARVAM_API_KEY is set
3. Restart backend server

### Sarvam SDK Import Error

**Error**: `ModuleNotFoundError: No module named 'sarvamai'`

**Solution**:
```bash
pip install -U sarvamai
```

### Audio Upload Error

**Error**: File upload fails

**Solution**:
1. Check audio_uploads directory exists
2. Verify directory permissions
3. Check file size (should be reasonable)
4. Verify file format (WAV recommended)

### STT Transcription Fails

**Error**: Transcription returns empty or error

**Solution**:
1. Verify audio quality
2. Check Sarvam API status
3. Verify API key is valid
4. Check network connectivity
5. Review backend logs

### TTS Generation Fails

**Error**: Audio generation fails

**Solution**:
1. Verify text is not empty
2. Check Sarvam API status
3. Verify API key is valid
4. Check network connectivity
5. Review backend logs

### Audio Not Playing

**Error**: Audio doesn't play in browser

**Solution**:
1. Check audio URL is correct
2. Verify audio file exists in audio_uploads
3. Check browser audio support
4. Check CORS configuration
5. Verify audio file format

### Microphone Access Denied

**Error**: Browser denies microphone access

**Solution**:
1. Check browser permissions
2. Allow microphone access
3. Use HTTPS (required for microphone in production)
4. Try different browser (Chrome/Edge recommended)

## Configuration Options

### STT Mode

In `backend/services/sarvam_stt.py`:
- `mode="codemix"`: Supports Hindi, Hinglish, code-mixed (default)
- `mode="transcribe"`: Standard transcription

### TTS Speaker

In `backend/services/sarvam_tts.py`:
- Default: `shubh`
- Available: `shubh`, `arjun`, `meera`, `priya`, `rahul`

### Audio Format

- Input: WAV recommended
- Output: WAV
- Can be extended to support MP3, OGG

### Language

- Default: `hi-IN` (Hindi)
- Can be extended for other languages

## Production Considerations

### Security

1. **API Key Protection**
   - Use environment variables
   - Never hardcode in source
   - Use secrets management in production

2. **File Upload Security**
   - Add file size limits
   - Validate file types
   - Scan for malware
   - Implement rate limiting

3. **CORS Configuration**
   - Restrict allowed origins
   - Use specific domains
   - Enable credentials

### Performance

1. **Audio Compression**
   - Compress audio before upload
   - Use efficient formats
   - Implement streaming

2. **Caching**
   - Cache TTS responses
   - Cache common phrases
   - Implement CDN for audio

3. **Scalability**
   - Load balance backend
   - Use distributed storage
   - Implement queue for processing

### Monitoring

1. **Metrics**
   - Monitor STT/TTS latency
   - Track success rates
   - Alert on failures
   - Log errors

2. **Logging**
   - Enable detailed logging
   - Log all voice interactions
   - Monitor error rates
   - Implement log aggregation

### Audio Storage

1. **Storage**
   - Use cloud storage (S3, GCS)
   - Implement lifecycle policies
   - Backup audio files
   - Clean up old files

2. **CDN**
   - Serve audio via CDN
   - Improve delivery speed
   - Reduce latency
   - Handle global distribution

## Testing

### Unit Tests

```bash
cd backend
python -m pytest tests/test_voice_services.py
```

### Integration Tests

```bash
cd backend
python -m pytest tests/test_voice_integration.py
```

### Voice Quality Tests

Test with various:
- Accents
- Background noise
- Speaking speeds
- Audio quality levels

## Maintenance

### Regular Tasks

1. **Weekly**
   - Check API usage
   - Review error logs
   - Monitor latency
   - Verify audio storage

2. **Monthly**
   - Update SDK versions
   - Review costs
   - Optimize performance
   - Clean up old audio files

3. **Quarterly**
   - Review voice quality
   - Update models
   - Evaluate new features
   - Security audit

## Support

### Sarvam AI Documentation

- [Sarvam AI Docs](https://docs.sarvam.ai/)
- [API Reference](https://docs.sarvam.ai/api-reference/)
- [Support](https://sarvam.ai/support)

### CredResolve Documentation

- Architecture: `docs/voice_architecture.md`
- Demo Script: `docs/voice_demo_script.md`
- Main README: `README.md`

## Next Steps

After successful setup:

1. Test with real Hindi speakers
2. Collect feedback on voice quality
3. Optimize for common phrases
4. Add more speakers if needed
5. Implement audio compression
6. Add streaming support
7. Deploy to production

## Conclusion

The Voice AI module is now ready for use. Users can interact with the debt collection agent using natural Hindi and Hinglish speech, with full integration with the existing LangGraph agent, RAG system, tools, and memory layer.
