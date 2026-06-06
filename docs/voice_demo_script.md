# CredResolve AI - Voice Demo Script

## Overview

This script provides a step-by-step walkthrough for demonstrating the Voice AI module with Sarvam AI integration for the CredResolve Debt Collection Agent.

## Pre-Demo Setup

### 1. Start Backend

```bash
cd backend
source venv/bin/activate
export SARVAM_API_KEY=your_sarvam_api_key
python -m app.main
```

Verify backend is running:
```bash
curl http://localhost:8000/health
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Prepare Demo Environment

- Open browser to `http://localhost:3000`
- Open browser DevTools (F12) for network inspection
- Have test phone numbers ready:
  - `+919876543210` (Rajesh Kumar, Medium risk)
  - `+919123456789` (Priya Sharma, High risk)
  - `+919876543211` (Amit Singh, Low risk)
- Test microphone access
- Prepare Hindi phrases for testing

## Demo Script

### Section 1: Introduction (2 minutes)

**Speaker Notes:**
"Today I'll be demonstrating the Voice AI module for CredResolve, which uses Sarvam AI's speech services to enable natural Hindi and Hinglish voice interactions with our debt collection agent."

**Key Points to Cover:**
- Sarvam AI integration (Saaras v3 for STT, Bulbul v3 for TTS)
- Hindi and Hinglish support
- Code-mixed speech support
- Integration with existing LangGraph agent
- Seamless preservation of state and memory

**Action:** Navigate to Voice Chat page

---

### Section 2: Voice Architecture Overview (3 minutes)

**Speaker Notes:**
"The Voice AI module adds a speech layer on top of our existing LangGraph-based agent. User speech is transcribed by Sarvam Saaras v3, passed through the LangGraph state machine with Gemini, RAG, and tools, then the response is converted back to speech by Sarvam Bulbul v3."

**Key Points to Cover:**
- STT: Sarvam Saaras v3 (Hindi, Hinglish, code-mixed)
- Agent: Existing LangGraph state machine
- LLM: Gemini
- RAG: ChromaDB
- Tools: CRM, Payment, Ticket, SMS
- Memory: SQLite
- TTS: Sarvam Bulbul v3 (Hindi)

**Action:** Show architecture diagram if available

---

### Section 3: Voice Chat Interface Tour (2 minutes)

**Speaker Notes:**
"The Voice Chat interface provides recording controls, file upload, transcript display, response display with audio playback, state tracking, tool call visualization, and latency metrics."

**Key Points to Cover:**
- Start/Stop recording buttons
- Upload audio option
- Transcript display
- Agent response with audio player
- Current state indicator
- Tools used list
- Retrieved documents
- Latency metrics (STT, TTS, Total)

**Action:** Point to each UI element and explain briefly

---

### Section 4: Hindi Scenario 1 - Payment Delay (5 minutes)

**Speaker Notes:**
"Let's start with Scenario 1: Payment Delay. Rajesh Kumar has missed his payment due to a salary delay. The agent will handle this empathetically in Hindi."

**Actions:**
1. Enter phone number: `+919876543210`
2. Click "Start Recording"
3. Speak: "Namaste, main Rajesh bol raha hoon. Meri salary late aayi hai isliye payment nahi ho payi"
4. Click "Stop Recording"
5. Wait for STT transcription
6. Observe transcript appears
7. Wait for agent processing
8. Observe agent response
9. Observe audio plays automatically
10. Show current state (Greeting → Authentication → ContextGathering → Diagnosis → ToolExecution → Negotiation)
11. Show tools used (CRM tool, Payment tool)
12. Show retrieved documents (settlement policy)
13. Show latency metrics

**Key Points to Demonstrate:**
- Hindi speech recognition
- Code-mixed transcription (Hindi + English words)
- State transitions visible in UI
- Tool execution (settlement calculation)
- RAG retrieval (settlement policy)
- Hindi speech synthesis
- Latency breakdown (STT, TTS, Total)

**Expected Flow:**
```
User speaks → STT transcribes → LangGraph processes → Tools execute → RAG retrieves → 
Memory updates → TTS generates audio → Response returned → Audio plays
```

---

### Section 5: Hindi Scenario 2 - Request Extension (4 minutes)

**Speaker Notes:**
"Now let's see Scenario 2: Request Extension. The borrower needs more time to pay. The agent will create a Promise to Pay and schedule a callback."

**Actions:**
1. Enter phone number: `+919876543210`
2. Click "Start Recording"
3. Speak: "Mujhe agle hafte tak time chahiye. Main tab payment kar paunga"
4. Click "Stop Recording"
5. Wait for processing
6. Observe Promise to Pay creation
7. Observe callback scheduling
8. Show memory update

**Key Points to Demonstrate:**
- Hinglish speech recognition
- Promise to Pay logging
- Callback scheduling
- Memory persistence
- State preservation across voice turns

**Expected Flow:**
```
User speaks → STT transcribes → Agent understands extension request → 
Creates Promise to Pay → Schedules callback → Updates memory → TTS response
```

---

### Section 6: Hindi Scenario 3 - Payment Confirmation (3 minutes)

**Speaker Notes:**
"Scenario 3: Payment Confirmation. The borrower claims to have made a payment. The agent will run payment verification tools."

**Actions:**
1. Enter phone number: `+919876543211`
2. Click "Start Recording"
3. Speak: "Maine payment kar diya hai. Please check kijiye"
4. Click "Stop Recording"
5. Wait for processing
6. Observe payment verification tool execution
7. Show tool result

**Key Points to Demonstrate:**
- Payment verification tool execution
- Tool result display
- Agent response based on tool output
- Hindi speech synthesis

---

### Section 7: Hindi Scenario 4 - Settlement Request (4 minutes)

**Speaker Notes:**
"Scenario 4: Settlement Request. The borrower wants to know about settlement options. The agent will use RAG to retrieve the settlement policy."

**Actions:**
1. Enter phone number: `+919876543210`
2. Click "Start Recording"
3. Speak: "Mujhe settlement option chahiye. Kya options hain?"
4. Click "Stop Recording"
5. Wait for processing
6. Observe RAG retrieval
7. Show retrieved documents (settlement_policy.md)
8. Show settlement options presented to user

**Key Points to Demonstrate:**
- RAG integration with voice
- Document retrieval from ChromaDB
- Source citations
- Settlement policy explanation
- Hindi response with policy details

---

### Section 8: Hindi Scenario 5 - Do Not Call Preference (3 minutes)

**Speaker Notes:**
"Scenario 5: Do Not Call Preference. The borrower requests not to be called frequently. The agent will log this preference and schedule a follow-up."

**Actions:**
1. Enter phone number: `+919123456789`
2. Click "Start Recording"
3. Speak: "Mujhe baar baar call mat kariye. Main pareshan hoon"
4. Click "Stop Recording"
5. Wait for processing
6. Observe preference logging
7. Observe callback scheduling
8. Show memory update

**Key Points to Demonstrate:**
- Preference logging in memory
- Callback scheduling
- Empathetic response
- De-escalation handling
- Memory persistence

---

### Section 9: File Upload Demo (3 minutes)

**Speaker Notes:**
"The system also supports uploading pre-recorded audio files. Let me demonstrate this feature."

**Actions:**
1. Prepare a pre-recorded Hindi audio file (WAV format)
2. Enter phone number: `+919876543210`
3. Click "Upload Audio"
4. Select audio file
5. Wait for processing
6. Observe same processing as live recording

**Key Points to Demonstrate:**
- File upload support
- WAV format support
- Same processing pipeline
- Consistent results

---

### Section 10: TTS-Only Demo (2 minutes)

**Speaker Notes:**
"We can also use the TTS service independently to convert any text to Hindi speech."

**Actions:**
1. Use the text chat interface
2. Send a message: "Namaste, aapka din kaisa hai?"
3. Click "Speak Last Response" button
4. Observe audio plays

**Key Points to Demonstrate:**
- TTS can be used independently
- Hindi speech synthesis
- Multiple speaker options (shubh, arjun, meera, priya, rahul)
- Audio quality

---

### Section 11: Voice Metrics Demo (3 minutes)

**Speaker Notes:**
"The system tracks detailed voice-specific metrics including STT latency, TTS latency, success rates, and error rates."

**Actions:**
1. Navigate to Metrics page or use API
2. Show voice metrics endpoint: `GET /voice/metrics`
3. Demonstrate metrics:
   - STT success/error counts
   - TTS success/error counts
   - Voice roundtrip counts
   - Latency measurements
   - Recent events

**Key Points to Demonstrate:**
- Real-time metrics tracking
- Latency breakdown
- Success/failure rates
- Event logging
- Observability

---

### Section 12: State Preservation Demo (3 minutes)

**Speaker Notes:**
"Voice conversations preserve all state and memory, allowing seamless continuation from previous text or voice interactions."

**Actions:**
1. Start a voice conversation
2. Note the current state
3. Switch to text chat
4. Continue conversation
5. Switch back to voice
6. Observe state is preserved
7. Show memory viewer to see conversation history

**Key Points to Demonstrate:**
- State preservation across modalities
- Memory persistence
- Conversation history
- Seamless switching
- Context continuity

---

### Section 13: Latency Breakdown (2 minutes)

**Speaker Notes:**
"Let me show you the latency breakdown for a typical voice interaction."

**Actions:**
1. Run a voice interaction
2. Show latency metrics:
   - STT latency: ~1-2 seconds
   - Agent processing: ~1-2 seconds
   - TTS latency: ~1-2 seconds
   - Total roundtrip: ~3-6 seconds

**Key Points to Demonstrate:**
- STT latency measurement
- TTS latency measurement
- Total roundtrip time
- Performance optimization opportunities

---

### Section 14: Error Handling Demo (2 minutes)

**Speaker Notes:**
"The system includes robust error handling with retry mechanisms for both STT and TTS services."

**Key Points to Cover:**
- STT retry mechanism (3 attempts with exponential backoff)
- TTS retry mechanism (3 attempts with exponential backoff)
- Graceful degradation (text fallback if audio fails)
- Error logging and metrics
- User-friendly error messages

---

### Section 15: Multi-Speaker Demo (2 minutes)

**Speaker Notes:**
"The TTS service supports multiple speakers for different voices. Let me show you the available speakers."

**Actions:**
1. Call `GET /voice/speakers` endpoint
2. Show available speakers: shubh, arjun, meera, priya, rahul
3. Explain each speaker's characteristics
4. Note that shubh is the default

**Key Points to Demonstrate:**
- Multiple speaker options
- Speaker selection capability
- Voice variety
- Customization options

---

### Section 16: Integration with Existing Features (3 minutes)

**Speaker Notes:**
"The Voice AI module integrates seamlessly with all existing features including LangGraph state machine, RAG, tools, and memory."

**Key Points to Cover:**
- LangGraph state machine unchanged
- RAG retrieval works identically
- All tools (CRM, Payment, Ticket, SMS) work with voice
- Memory layer preserves voice conversations
- No changes to existing text chat functionality

---

### Section 17: Hindi and Hinglish Support (2 minutes)

**Speaker Notes:**
"The system supports pure Hindi, Hinglish (Hindi written in English script), and code-mixed speech."

**Examples to Mention:**
- Pure Hindi: "Namaste, main Rajesh bol raha hoon"
- Hinglish: "My salary late aayi hai"
- Code-mixed: "Meri salary late aayi hai isliye payment nahi ho payi"

**Key Points to Demonstrate:**
- STT mode: "codemix" handles all variations
- Natural language understanding
- Cultural context preservation
- Appropriate responses

---

### Section 18: Summary and Q&A (5 minutes)

**Speaker Notes:**
"In summary, the Voice AI module with Sarvam AI integration enables natural Hindi and Hinglish voice interactions while preserving all existing LangGraph, RAG, tools, and memory functionality."

**Key Achievements:**
- Production-quality voice integration
- Hindi and Hinglish support
- Code-mixed speech recognition
- Seamless state and memory preservation
- Real-time metrics and observability
- Robust error handling
- Multiple speaker options
- File upload support
- Latency tracking

**Open Floor for Questions:**
- Technical implementation
- Sarvam AI integration
- Performance optimization
- Future enhancements
- Deployment considerations

---

## Demo Checklist

### Pre-Demo
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] SARVAM_API_KEY configured
- [ ] Microphone access granted
- [ ] Test phone numbers ready
- [ ] Hindi phrases prepared
- [ ] DevTools open for network inspection
- [ ] Audio file prepared for upload demo

### During Demo
- [ ] All voice endpoints respond correctly
- [ ] STT transcribes Hindi correctly
- [ ] TTS generates Hindi audio
- [ ] State transitions visible
- [ ] Tool calls execute
- [ ] RAG retrieves documents
- [ ] Memory updates work
- [ ] Latency metrics display
- [ ] Audio plays correctly
- [ ] File upload works
- [ ] Speaker options available
- [ ] Metrics update in real-time

### Post-Demo
- [ ] Clear audio uploads if needed
- [ ] Reset metrics if needed
- [ ] Document any issues
- [ ] Collect feedback

## Troubleshooting

### Backend Not Responding
```bash
# Check if running
ps aux | grep python

# Restart
cd backend
source venv/bin/activate
python -m app.main
```

### Frontend Not Loading
```bash
# Clear cache
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Microphone Not Working
- Use Chrome or Edge browser
- Check microphone permissions
- Ensure HTTPS (or localhost)
- Test with different browser

### STT Not Transcribing
- Check SARVAM_API_KEY
- Verify audio quality
- Check network connectivity
- Review backend logs

### TTS Not Generating
- Check SARVAM_API_KEY
- Verify text is not empty
- Check network connectivity
- Review backend logs

### Audio Not Playing
- Check audio URL
- Verify file exists
- Check browser audio support
- Check CORS configuration

## Alternative Demo Scenarios

If time permits, demonstrate:

### Scenario 6: Angry Borrower
- Phone: `+919123456789`
- Speak: "Main bahut gussa hoon! Aap log pareshan kar rahe ho!"
- Show de-escalation
- Demonstrate empathy

### Scenario 7: Dispute Resolution
- Phone: `+919876543211`
- Speak: "Amount galat hai. Maine already pay kar diya tha"
- Show dispute handling
- Demonstrate ticket creation

## Customization for Audience

### For Technical Audience
- Focus on Sarvam AI integration
- Show code snippets
- Explain STT/TTS implementation
- Demonstrate API endpoints
- Discuss error handling

### For Business Audience
- Focus on user experience
- Show natural conversation flow
- Demonstrate Hindi support
- Highlight efficiency gains
- Show compliance features

### For Academic Audience
- Focus on AI concepts
- Explain speech recognition
- Discuss state machine integration
- Show RAG with voice
- Explain metrics and observability

## Recording Tips

If recording the demo:
1. Use screen recording software
2. Ensure good audio quality
3. Speak clearly and at moderate pace
4. Highlight key actions with mouse
5. Keep demo under 30 minutes
6. Edit out long pauses
7. Add captions if possible

## Follow-Up Materials

After the demo, provide:
- voice_architecture.md
- voice_setup.md
- README.md (updated with voice features)
- Source code access
- Contact information
