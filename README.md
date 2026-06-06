# CredResolve AI Debt Collection Agent

A complete internship-assignment-grade project demonstrating Agentic AI, LangGraph workflows, tool calling, RAG, voice interaction, memory persistence, and Hindi debt collection conversations with monitoring and observability.

## 🎯 Project Overview

CredResolve AI is an intelligent debt collection agent that:
- Conducts ethical, RBI-compliant debt collection conversations
- Supports Hindi and Hinglish (Hindi written in English script)
- Uses LangGraph state machine with 11 states
- Implements RAG with ChromaDB for knowledge retrieval
- Provides voice interaction using browser Speech APIs
- Maintains conversation and user memory in SQLite
- Offers real-time monitoring and metrics

## 🏗️ Architecture

The project consists of:

### Backend (Python 3.12)
- **FastAPI**: REST API server
- **LangGraph**: State machine orchestration
- **LangChain**: AI framework integration
- **ChromaDB**: Vector database for RAG
- **SQLite**: Memory persistence
- **Gemini API**: Embeddings and AI capabilities

### Frontend (React + TailwindCSS)
- **Dashboard**: Overview and navigation
- **Chat Interface**: Text and voice interaction
- **Memory Viewer**: User and conversation history
- **Metrics Viewer**: System performance monitoring
- **Knowledge Base Viewer**: RAG document browser
- **Tool Logs Viewer**: Tool call history

### Voice Features
- **SpeechRecognition API**: Hindi/Hinglish speech input
- **SpeechSynthesis API**: AI voice output

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- Node.js 18+
- Gemini API Key

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the server
python -m app.main
```

The backend will start on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 📱 Usage

### Starting a Conversation

1. Navigate to the Chat Interface
2. Enter a phone number (try: `+919876543210`, `+919123456789`, or `+919876543211`)
3. Type your message or use voice input
4. Watch the agent navigate through states and use tools

### Test Phone Numbers

- `+919876543210` - Rajesh Kumar (Medium risk, ₹45,000 due)
- `+919123456789` - Priya Sharma (High risk, ₹75,000 due)
- `+919876543211` - Amit Singh (Low risk, ₹25,000 due)

### Hindi Scenarios

The agent handles 5 Hindi debt collection scenarios:

1. **Payment Delay** - Temporary financial difficulty
2. **Refusal to Pay** - Inability to pay
3. **Payment Dispute** - Amount discrepancy
4. **Settlement Negotiation** - Better terms requested
5. **Angry Borrower** - Emotional upset

## 🧠 LangGraph State Machine

The agent uses an 11-state state machine:

1. **Greeting** - Welcome and establish contact
2. **Authentication** - Verify borrower identity
3. **ContextGathering** - Gather borrower situation
4. **Diagnosis** - Analyze and determine path
5. **KnowledgeRetrieval** - Retrieve relevant information
6. **ToolExecution** - Execute tools (payment, SMS, etc.)
7. **Negotiation** - Discuss payment terms
8. **Escalation** - Handle cases needing human intervention
9. **Resolution** - Confirm agreement
10. **FollowUp** - Schedule callback
11. **EndConversation** - Close and save

See `state_machine.md` for detailed state definitions.

## 🔧 Tools

The agent has 4 mock tools:

1. **CRM Tool** - Fetch customer data
2. **Payment Tool** - Calculate settlements and restructuring
3. **Ticket Tool** - Create and manage tickets
4. **SMS Tool** - Send reminders and confirmations

## 📚 Knowledge Base

RAG system includes 5 documents:

- `rbi_collection_guidelines.md` - RBI compliance rules
- `settlement_policy.md` - Settlement options
- `payment_dispute_policy.md` - Dispute resolution
- `escalation_policy.md` - Escalation procedures
- `faq.md` - Frequently asked questions

## 📊 Monitoring

Real-time metrics available at `/metrics` endpoint:

- Conversation count
- Resolution rate
- Escalation count
- Tool call success rate
- State transition tracking
- Latency measurements

## 💾 Memory

Two types of memory:

### User Memory
- Preferred callback time
- Settlement preference
- Language preference

### Conversation Memory
- Message history
- State transitions
- Tool calls
- Promises-to-pay

## 🎨 Frontend Pages

- **Dashboard** - Overview and quick start
- **Chat Interface** - Main interaction page
- **Memory Viewer** - Browse stored memories
- **Metrics Viewer** - System performance
- **Knowledge Base Viewer** - Search documents
- **Tool Logs Viewer** - Direct tool testing

## 🔐 API Endpoints

- `POST /chat` - Send message to agent
- `GET /metrics` - Get system metrics
- `GET /memory/{phone_number}` - Get user memory
- `POST /tool` - Direct tool call
- `POST /knowledge/retrieve` - RAG retrieval
- `GET /customer/{phone_number}` - Get customer data
- `GET /health` - Health check

## 📁 Project Structure

```
credresolve/
├── backend/
│   ├── app/
│   │   ├── agent/          # LangGraph state machine
│   │   ├── rag/            # RAG layer
│   │   ├── tools/          # Mock tools
│   │   ├── memory/         # SQLite memory
│   │   ├── monitoring/     # Metrics tracking
│   │   ├── prompts/        # Prompt library
│   │   ├── scenarios/      # Hindi scenarios
│   │   └── main.py         # FastAPI app
│   ├── knowledge/          # RAG documents
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/          # React pages
│   │   ├── services/       # API services
│   │   └── App.jsx
│   └── package.json
└── docs/                   # Documentation
```

## 🎓 Learning Outcomes

This project demonstrates:

- **Agentic AI** - Autonomous decision-making
- **LangGraph** - Complex state machine workflows
- **Tool Calling** - External service integration
- **RAG** - Knowledge retrieval with citations
- **Voice AI** - Speech recognition and synthesis
- **Memory** - Persistent conversation context
- **Monitoring** - Observability and metrics
- **Ethical AI** - RBI-compliant debt collection

## 📝 Documentation

- `README.md` - This file
- `architecture.md` - System architecture details
- `architecture_mermaid.md` - Architecture diagram
- `state_machine.md` - State machine documentation
- `state_machine_mermaid.md` - State machine diagram
- `prompt_design.md` - Prompt engineering rationale
- `deployment.md` - Deployment instructions
- `demo_script.md` - Demo walkthrough

## 🤝 Contributing

This is an internship assignment project. For improvements or issues, please refer to the project guidelines.

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- LangChain for the AI framework
- LangGraph for state machine orchestration
- ChromaDB for vector storage
- FastAPI for the backend framework
- React and TailwindCSS for the frontend
