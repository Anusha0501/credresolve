# CredResolve AI - Demo Script

## Overview

This script provides a step-by-step walkthrough for demonstrating the CredResolve AI Debt Collection Agent to stakeholders, evaluators, or during an internship presentation.

## Pre-Demo Setup

### 1. Start Backend

```bash
cd backend
source venv/bin/activate
export GEMINI_API_KEY=your_api_key_here
python -m app.main
```

Verify backend is running:
```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 3. Prepare Demo Environment

- Open browser to `http://localhost:3000`
- Open browser DevTools (F12) for network inspection
- Have phone numbers ready:
  - `+919876543210` (Rajesh Kumar, Medium risk)
  - `+919123456789` (Priya Sharma, High risk)
  - `+919876543211` (Amit Singh, Low risk)

## Demo Script

### Section 1: Introduction (2 minutes)

**Speaker Notes:**
"Today I'll be demonstrating CredResolve AI, an intelligent debt collection agent that uses Agentic AI, LangGraph workflows, and RAG to conduct ethical, RBI-compliant debt collection conversations in Hindi and Hinglish."

**Key Points to Cover:**
- Purpose: Ethical debt collection
- Technologies: LangGraph, RAG, Voice AI, Memory
- Compliance: RBI guidelines
- Languages: Hindi and Hinglish support

**Action:** Navigate to Dashboard page

---

### Section 2: Architecture Overview (3 minutes)

**Speaker Notes:**
"The system consists of a Python FastAPI backend with LangGraph state machine, ChromaDB for RAG, and SQLite for memory. The frontend is built with React and TailwindCSS with voice interaction using browser Speech APIs."

**Key Points to Cover:**
- Backend: Python, FastAPI, LangGraph
- Frontend: React, TailwindCSS
- Voice: Browser Speech APIs
- Knowledge: ChromaDB with 5 documents
- Memory: SQLite for persistence

**Action:** Click through different pages briefly to show navigation

---

### Section 3: Dashboard Tour (2 minutes)

**Speaker Notes:**
"The Dashboard provides an overview of all features. From here, we can access the Chat Interface, Memory Viewer, Metrics, Knowledge Base, and Tool Logs."

**Key Points to Cover:**
- Navigation structure
- Feature cards
- Quick start guide
- Feature highlights

**Action:** Point to each feature card and explain briefly

---

### Section 4: Hindi Scenario 1 - Payment Delay (5 minutes)

**Speaker Notes:**
"Let's start with Scenario 1: Payment Delay. Rajesh Kumar has missed his payment due to a job change. The agent will handle this empathetically and offer a settlement."

**Actions:**
1. Navigate to Chat Interface
2. Enter phone number: `+919876543210`
3. Type: "Namaste, main Rajesh bol raha hoon"
4. Watch agent navigate through states
5. Type: "Job change hua tha, isliye payment delay"
6. Observe tool execution (settlement calculation)
7. Type: "Haan, settlement accept karta hoon"
8. Observe resolution and SMS confirmation

**Key Points to Demonstrate:**
- State transitions (visible in UI)
- Tool calls (settlement calculation)
- Customer data display
- Empathetic response
- Hindi language support
- SMS confirmation

**Expected Flow:**
```
Greeting → Authentication → ContextGathering → Diagnosis 
→ ToolExecution → Negotiation → Resolution → EndConversation
```

---

### Section 5: Voice Interaction (3 minutes)

**Speaker Notes:**
"The system supports voice input and output using browser Speech APIs. Let me demonstrate the Hindi speech recognition."

**Actions:**
1. Click "Start Voice" button
2. Speak in Hindi: "Main payment kar sakta hoon"
3. Observe speech-to-text conversion
4. Click "Speak Last Response" button
5. Observe text-to-speech output

**Key Points to Demonstrate:**
- Speech recognition for Hindi
- Speech synthesis for AI responses
- Start/Stop voice controls
- Real-time transcription

**Note:** If browser doesn't support Speech API, mention it works in Chrome/Edge

---

### Section 6: Hindi Scenario 2 - Refusal to Pay (4 minutes)

**Speaker Notes:**
"Now let's see Scenario 2: Refusal to Pay. Priya Sharma is unable to pay and refuses. The agent maintains politeness and escalates appropriately without harassment."

**Actions:**
1. Enter phone number: `+919123456789`
2. Type: "Main payment nahi kar sakti"
3. Type: "Paisa nahi hai"
4. Observe escalation to senior team
5. Note ticket creation

**Key Points to Demonstrate:**
- Polite response to refusal
- No harassment or threats
- Appropriate escalation
- Ticket creation
- Professional closing

**Expected Flow:**
```
Greeting → Authentication → ContextGathering → Diagnosis 
→ Negotiation → Escalation → FollowUp → EndConversation
```

---

### Section 7: Memory Viewer (3 minutes)

**Speaker Notes:**
"The system maintains persistent memory. Let's check what was stored from our previous conversations."

**Actions:**
1. Navigate to Memory Viewer
2. Enter phone number: `+919876543210`
3. Click "Fetch Memory"
4. Show user memory (preferences)
5. Show conversation history
6. Show promises-to-pay (if any)

**Key Points to Demonstrate:**
- User memory (preferences, language)
- Conversation history with states
- State transitions
- Tool calls logged
- Timestamps

---

### Section 8: Metrics Viewer (3 minutes)

**Speaker Notes:**
"The system provides real-time monitoring and metrics. Let's check the current system performance."

**Actions:**
1. Navigate to Metrics Viewer
2. Show conversation count
3. Show resolution rate
4. Show escalation count
5. Show tool call count
6. Show state transitions
7. Show recent events

**Key Points to Demonstrate:**
- Real-time metrics
- State transition tracking
- Tool call monitoring
- Event logging
- Auto-refresh every 5 seconds

---

### Section 9: Knowledge Base (3 minutes)

**Speaker Notes:**
"The RAG system uses ChromaDB to retrieve relevant information from 5 knowledge base documents including RBI guidelines, settlement policy, and FAQs."

**Actions:**
1. Navigate to Knowledge Base Viewer
2. Show available documents list
3. Search: "settlement policy"
4. Show retrieved results with sources
5. Search: "RBI guidelines"
6. Show citations and distances

**Key Points to Demonstrate:**
- Document list
- Semantic search
- Source citations
- Relevance scores
- Chunked retrieval

---

### Section 10: Tool Logs (3 minutes)

**Speaker Notes:**
"The agent has 4 mock tools: CRM, Payment, Ticket, and SMS. Let's test them directly."

**Actions:**
1. Navigate to Tool Logs Viewer
2. Select CRM Tool → fetch_customer_data
3. Enter: `+919876543210`
4. Click "Call Tool"
5. Show customer data result
6. Select Payment Tool → calculate_settlement
7. Enter: `45000`
8. Click "Call Tool"
9. Show settlement calculation

**Key Points to Demonstrate:**
- Direct tool testing
- CRM tool (customer data)
- Payment tool (settlement calculation)
- Ticket tool (ticket creation)
- SMS tool (message sending)
- Tool descriptions

---

### Section 11: Hindi Scenario 3 - Payment Dispute (3 minutes)

**Speaker Notes:**
"Let's quickly demonstrate Scenario 3: Payment Dispute. Amit Singh claims he already paid but the amount wasn't credited."

**Actions:**
1. Enter phone number: `+919876543211`
2. Type: "Maine ₹20,000 pay kiya tha lekin amount nahi dikha"
3. Observe dispute handling
4. Note ticket creation for investigation
5. Note request for receipt

**Key Points to Demonstrate:**
- Dispute acknowledgment
- Policy retrieval
- Ticket creation
- Documentation request
- Investigation timeline

---

### Section 12: State Machine Visualization (2 minutes)

**Speaker Notes:**
"The agent uses an 11-state LangGraph state machine. Each state has specific entry criteria, exit criteria, and recovery paths."

**Key Points to Cover:**
- 11 states overview
- State transitions
- Conditional routing
- Tool integration
- Memory hooks

**Action:** Reference state_machine.md or show diagram if available

---

### Section 13: Architecture Deep Dive (3 minutes)

**Speaker Notes:**
"Let me explain the technical architecture in more detail."

**Key Points to Cover:**
- Frontend-Backend separation
- REST API design
- LangGraph integration
- RAG pipeline
- Memory persistence
- Monitoring layer

**Action:** Reference architecture.md or show diagram

---

### Section 14: Prompt Engineering (2 minutes)

**Speaker Notes:**
"The system uses 4 carefully designed prompts: System Prompt, Context Prompt, Reasoning Prompt, and Evaluation Prompt."

**Key Points to Cover:**
- System prompt: Role and principles
- Context prompt: Information synthesis
- Reasoning prompt: Decision framework
- Evaluation prompt: Quality assessment
- Ethical guardrails

**Action:** Reference prompt_design.md

---

### Section 15: Compliance and Ethics (2 minutes)

**Speaker Notes:**
"The system is designed with strict ethical guidelines and RBI compliance."

**Key Points to Cover:**
- RBI guidelines adherence
- Contact hours (8 AM - 7 PM)
- No harassment
- Privacy protection
- Ethical communication
- Prohibited behaviors

**Action:** Show relevant knowledge base document

---

### Section 16: Summary and Q&A (5 minutes)

**Speaker Notes:**
"In summary, CredResolve AI demonstrates a complete agentic AI system with LangGraph workflows, RAG, voice interaction, memory persistence, and ethical debt collection practices."

**Key Achievements:**
- Working prototype
- Clean architecture
- Demonstrable features
- Hindi language support
- RBI compliance
- Real-time monitoring

**Open Floor for Questions:**
- Technical implementation
- Architecture decisions
- Future enhancements
- Deployment considerations

---

## Demo Checklist

### Pre-Demo
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Gemini API key configured
- [ ] Phone numbers ready
- [ ] Browser supports Speech API
- [ ] DevTools open for network inspection

### During Demo
- [ ] All pages load correctly
- [ ] Chat interface works
- [ ] Voice features work
- [ ] Memory retrieval works
- [ ] Metrics update in real-time
- [ ] Knowledge search works
- [ ] Tool calls execute
- [ ] State transitions visible
- [ ] Hindi text displays correctly

### Post-Demo
- [ ] Clear conversation history if needed
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

### Voice Not Working
- Use Chrome or Edge browser
- Check microphone permissions
- Ensure HTTPS (or localhost)

### Memory Not Saving
- Check SQLite database file
- Verify write permissions
- Check backend logs

## Alternative Demo Scenarios

If time permits, demonstrate:

### Scenario 4: Settlement Negotiation
- Phone: `+919876543210`
- Request better terms
- Show EMI restructuring option

### Scenario 5: Angry Borrower
- Phone: `+919123456789`
- Express anger
- Show de-escalation
- Demonstrate empathy

## Customization for Audience

### For Technical Audience
- Focus on architecture
- Show code snippets
- Explain LangGraph
- Demonstrate API endpoints

### For Business Audience
- Focus on features
- Show ROI potential
- Demonstrate compliance
- Highlight efficiency

### For Academic Audience
- Focus on AI concepts
- Explain state machine
- Show RAG implementation
- Discuss prompt engineering

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
- README.md
- architecture.md
- state_machine.md
- prompt_design.md
- deployment.md
- Source code access
- Contact information
