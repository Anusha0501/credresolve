# CredResolve AI - System Architecture

## Overview

CredResolve AI is a full-stack debt collection agent system built with a Python FastAPI backend and React frontend. The system uses LangGraph for state machine orchestration, ChromaDB for RAG, and browser Speech APIs for voice interaction.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Dashboard│ │   Chat   │ │  Memory  │ │ Metrics  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐                                     │
│  │Knowledge │ │  Tools   │                                     │
│  └──────────┘ └──────────┘                                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    API Layer                          │  │
│  │  /chat, /metrics, /memory, /tool, /knowledge         │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  LangGraph   │  │     RAG      │  │    Tools     │     │
│  │   Agent      │  │    Layer     │  │    Layer     │     │
│  │              │  │              │  │              │     │
│  │  11 States   │  │  ChromaDB    │  │  CRM, Pay,   │     │
│  │  State M/C   │  │  Gemini Emb  │  │  Ticket, SMS │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                              │                               │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    Memory    │  │  Monitoring  │                        │
│  │    Layer     │  │    Layer     │                        │
│  │              │  │              │                        │
│  │   SQLite     │  │  Metrics     │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ┌─────────┐         ┌─────────┐
              │ChromaDB │         │ SQLite  │
              │Vector DB│         │Database │
              └─────────┘         └─────────┘
```

## Component Details

### Frontend Layer

**Technology Stack:**
- React 18.2
- React Router DOM 6.20
- Axios 1.6
- Lucide React (icons)
- TailwindCSS 3.3
- Vite 5.0

**Pages:**
1. **Dashboard** - Overview and navigation hub
2. **Chat Interface** - Main interaction page with voice support
3. **Memory Viewer** - Browse user and conversation memory
4. **Metrics Viewer** - Real-time system metrics
5. **Knowledge Base Viewer** - Search and browse RAG documents
6. **Tool Logs Viewer** - Direct tool testing interface

**Voice Features:**
- SpeechRecognition API for Hindi/Hinglish input
- SpeechSynthesis API for AI voice output
- Start/Stop voice buttons
- Speak response button

### Backend Layer

**Technology Stack:**
- Python 3.12
- FastAPI 0.104
- LangGraph 0.0.26
- LangChain 0.1.0
- ChromaDB 0.4.22
- Google Generative AI 0.3.2
- Pydantic 2.5.2

**API Endpoints:**
- `POST /chat` - Main chat endpoint
- `GET /metrics` - System metrics
- `GET /memory/{phone_number}` - User memory
- `POST /tool` - Direct tool calls
- `POST /knowledge/retrieve` - RAG retrieval
- `GET /customer/{phone_number}` - Customer data
- `GET /health` - Health check

### LangGraph Agent Layer

**State Machine:**
- 11 states for conversation flow
- Conditional routing based on context
- Tool execution integration
- Memory persistence hooks

**States:**
1. Greeting - Welcome and establish contact
2. Authentication - Verify borrower identity
3. ContextGathering - Gather borrower situation
4. Diagnosis - Analyze and determine path
5. KnowledgeRetrieval - Retrieve relevant information
6. ToolExecution - Execute tools
7. Negotiation - Discuss payment terms
8. Escalation - Handle human intervention cases
9. Resolution - Confirm agreement
10. FollowUp - Schedule callback
11. EndConversation - Close and save

### RAG Layer

**Components:**
- ChromaDB vector store
- Gemini embeddings
- Document ingestion pipeline
- Knowledge retriever

**Knowledge Base:**
- RBI collection guidelines
- Settlement policy
- Payment dispute policy
- Escalation policy
- FAQ

**Process:**
1. Documents chunked and embedded
2. Stored in ChromaDB with metadata
3. Retrieved using semantic search
4. Formatted for context in prompts

### Tools Layer

**Mock Tools:**
1. **CRM Tool**
   - fetch_customer_data
   - get_customer_summary

2. **Payment Tool**
   - calculate_settlement
   - calculate_emi_restructuring
   - calculate_outstanding

3. **Ticket Tool**
   - create_ticket
   - update_ticket
   - get_tickets

4. **SMS Tool**
   - send_reminder
   - send_confirmation
   - get_sms_history

All tool calls are logged and visible in the UI.

### Memory Layer

**SQLite Database:**
- User memory table
- Conversation memory table
- Promises-to-pay table

**User Memory:**
- Phone number
- Preferred callback time
- Settlement preference
- Language preference

**Conversation Memory:**
- Phone number
- State
- Message
- Response
- Timestamp
- Metadata

**Promises-to-Pay:**
- Phone number
- Amount
- Promise date
- Status

### Monitoring Layer

**Metrics Tracked:**
- Conversation count
- Resolution rate
- Escalation count
- Tool call success rate
- State transition counts
- Latency measurements
- Retrieval success rate

**Dashboard:**
- Real-time counters
- Recent events
- State transition tracking
- Tool call history

## Data Flow

### Chat Flow

```
User Input (Text/Voice)
    ↓
Frontend (React)
    ↓
HTTP POST /chat
    ↓
FastAPI Backend
    ↓
LangGraph State Machine
    ↓
┌─────────────────────────────────┐
│  State Routing & Execution       │
│  - Greeting                     │
│  - Authentication                │
│  - Context Gathering            │
│  - Diagnosis                    │
│  - Knowledge Retrieval (RAG)    │
│  - Tool Execution               │
│  - Negotiation                  │
│  - Resolution/Escalation        │
│  - FollowUp                     │
│  - End Conversation             │
└─────────────────────────────────┘
    ↓
Memory Persistence (SQLite)
    ↓
Response Generation
    ↓
HTTP Response
    ↓
Frontend Display
    ↓
Voice Output (if enabled)
```

### RAG Flow

```
Query from Agent
    ↓
Knowledge Retriever
    ↓
ChromaDB Vector Search
    ↓
Top-k Results
    ↓
Format for Context
    ↓
Inject into Prompt
    ↓
Enhanced Response
```

### Tool Execution Flow

```
Agent Decision
    ↓
Tool Call
    ↓
Mock Tool Execution
    ↓
Result Logging
    ↓
Metrics Tracking
    ↓
Return to Agent
    ↓
Continue Conversation
```

## Security Considerations

1. **API Key Management** - Environment variables for Gemini API
2. **CORS Configuration** - Proper CORS settings for frontend
3. **Input Validation** - Pydantic models for request validation
4. **Privacy Protection** - No disclosure to third parties
5. **Rate Limiting** - Can be added for production

## Scalability Considerations

1. **Database** - SQLite can be replaced with PostgreSQL
2. **Vector Store** - ChromaDB can be scaled or replaced with Pinecone
3. **API** - FastAPI supports async and can be deployed with Gunicorn
4. **Frontend** - React can be deployed to Vercel or Netlify
5. **Monitoring** - Can integrate with Prometheus/Grafana

## Deployment Architecture

**Development:**
- Backend: Localhost on port 8000
- Frontend: Localhost on port 3000
- Proxy: Vite proxy for API calls

**Production:**
- Backend: Cloud server (AWS/GCP/Azure)
- Frontend: Vercel/Netlify
- Database: Managed PostgreSQL
- Vector Store: Pinecone/Weaviate
- Monitoring: Datadog/New Relic

## Technology Rationale

### Why LangGraph?
- Declarative state machine definition
- Built-in state management
- Easy to visualize and debug
- Integrates with LangChain

### Why ChromaDB?
- Open source and free
- Easy to set up locally
- Good performance for small to medium datasets
- Python-native

### Why FastAPI?
- Fast performance
- Automatic API documentation
- Type hints with Pydantic
- Async support

### Why React + TailwindCSS?
- Component-based architecture
- Large ecosystem
- TailwindCSS for rapid styling
- Modern and maintainable

### Why Browser Speech APIs?
- No additional dependencies
- Works in modern browsers
- Free and built-in
- Good for prototyping

## Future Enhancements

1. **Real LLM Integration** - Replace mock responses with actual Gemini API
2. **Advanced Voice** - Add Whisper for better speech recognition
3. **Multi-language** - Support more Indian languages
4. **Analytics** - Advanced analytics dashboard
5. **Integration** - Real CRM and payment gateway integration
6. **Authentication** - User authentication and authorization
7. **Webhooks** - Real-time notifications
8. **Mobile App** - React Native mobile application
