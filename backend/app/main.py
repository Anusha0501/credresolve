from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import os

from app.config import config
from app.agent.graph import create_agent_graph
from app.agent.state import AgentState
from app.tools.mock_tools import crm_tool, ticket_tool, payment_tool, sms_tool
from app.memory.database import memory_db
from app.rag.ingestion import document_ingestion
from app.rag.retriever import knowledge_retriever
from app.monitoring.metrics import metrics_tracker, track_metric

# Initialize FastAPI app
app = FastAPI(title="CredResolve AI Debt Collection Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent graph
agent_graph = create_agent_graph()

# Request/Response models
class ChatRequest(BaseModel):
    phone_number: str
    message: str
    language: str = "hindi"

class ChatResponse(BaseModel):
    response: str
    current_state: str
    tool_calls: List[Dict]
    customer_data: Optional[Dict]
    retrieved_knowledge: List[Dict]

class MetricsResponse(BaseModel):
    counters: Dict[str, int]
    recent_metrics: Dict[str, List[Dict]]

class MemoryResponse(BaseModel):
    user_memory: Optional[Dict]
    conversation_history: List[Dict]
    promises_to_pay: List[Dict]

class ToolCallRequest(BaseModel):
    tool_name: str
    function: str
    parameters: Dict

class ToolCallResponse(BaseModel):
    result: Dict
    success: bool

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("Starting CredResolve AI Agent...")
    
    # Ingest knowledge base documents
    knowledge_dir = os.path.join(os.path.dirname(__file__), "..", "knowledge")
    if os.path.exists(knowledge_dir):
        document_ingestion.knowledge_dir = knowledge_dir
        document_ingestion.ingest_all()
        print("Knowledge base documents ingested successfully")
    
    print("CredResolve AI Agent started successfully")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for debt collection agent"""
    track_metric("chat_request", {"phone_number": request.phone_number, "language": request.language})
    metrics_tracker.start_timer("chat_processing")
    
    try:
        # Initialize state
        initial_state: AgentState = {
            "phone_number": request.phone_number,
            "current_state": "",
            "customer_data": None,
            "conversation_history": [{"message": request.message, "timestamp": datetime.now().isoformat()}],
            "user_memory": None,
            "retrieved_knowledge": [],
            "tool_calls": [],
            "agent_response": "",
            "next_state": "",
            "metadata": {"language": request.language},
            "timestamp": datetime.now().isoformat()
        }
        
        # Run the agent graph
        result = agent_graph.invoke(initial_state)
        
        # Save conversation to memory
        memory_db.save_conversation(
            request.phone_number,
            result.get("current_state", ""),
            request.message,
            result.get("agent_response", ""),
            result.get("metadata", {})
        )
        
        metrics_tracker.end_timer("chat_processing")
        track_metric("chat_success", {"phone_number": request.phone_number})
        
        return ChatResponse(
            response=result.get("agent_response", ""),
            current_state=result.get("current_state", ""),
            tool_calls=result.get("tool_calls", []),
            customer_data=result.get("customer_data"),
            retrieved_knowledge=result.get("retrieved_knowledge", [])
        )
    
    except Exception as e:
        metrics_tracker.end_timer("chat_processing")
        track_metric("chat_error", {"phone_number": request.phone_number, "error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

# Metrics endpoint
@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get application metrics"""
    summary = metrics_tracker.get_metrics_summary()
    return MetricsResponse(
        counters=summary["counters"],
        recent_metrics=summary["recent_metrics"]
    )

# Memory endpoint
@app.get("/memory/{phone_number}", response_model=MemoryResponse)
async def get_memory(phone_number: str):
    """Get memory for a phone number"""
    user_memory = memory_db.get_user_memory(phone_number)
    conversation_history = memory_db.get_conversation_history(phone_number)
    promises_to_pay = memory_db.get_promises_to_pay(phone_number)
    
    return MemoryResponse(
        user_memory=user_memory,
        conversation_history=conversation_history,
        promises_to_pay=promises_to_pay
    )

# Tool call endpoint
@app.post("/tool", response_model=ToolCallResponse)
async def call_tool(request: ToolCallRequest):
    """Direct tool call endpoint"""
    track_metric("tool_call_direct", {"tool": request.tool_name, "function": request.function})
    
    try:
        result = {}
        success = True
        
        if request.tool_name == "crm":
            if request.function == "fetch_customer_data":
                result = crm_tool.fetch_customer_data(request.parameters.get("phone_number"))
            elif request.function == "get_customer_summary":
                result = {"summary": crm_tool.get_customer_summary(request.parameters.get("phone_number"))}
        
        elif request.tool_name == "payment":
            if request.function == "calculate_settlement":
                result = payment_tool.calculate_settlement(request.parameters.get("amount"))
            elif request.function == "calculate_emi_restructuring":
                result = payment_tool.calculate_emi_restructuring(request.parameters.get("amount"))
        
        elif request.tool_name == "ticket":
            if request.function == "create_ticket":
                result = ticket_tool.create_ticket(
                    request.parameters.get("phone_number"),
                    request.parameters.get("issue_type"),
                    request.parameters.get("description")
                )
            elif request.function == "get_tickets":
                result = {"tickets": ticket_tool.get_tickets(request.parameters.get("phone_number"))}
        
        elif request.tool_name == "sms":
            if request.function == "send_reminder":
                result = sms_tool.send_reminder(
                    request.parameters.get("phone_number"),
                    request.parameters.get("message")
                )
            elif request.function == "send_confirmation":
                result = sms_tool.send_confirmation(
                    request.parameters.get("phone_number"),
                    request.parameters.get("message")
                )
        
        else:
            success = False
            result = {"error": "Unknown tool"}
        
        track_metric("tool_call_success", {"tool": request.tool_name, "success": success})
        
        return ToolCallResponse(result=result, success=success)
    
    except Exception as e:
        track_metric("tool_call_error", {"tool": request.tool_name, "error": str(e)})
        return ToolCallResponse(result={"error": str(e)}, success=False)

# Knowledge retrieval endpoint
@app.post("/knowledge/retrieve")
async def retrieve_knowledge(query: str, top_k: int = 3):
    """Retrieve knowledge from the knowledge base"""
    track_metric("knowledge_retrieval", {"query": query, "top_k": top_k})
    
    try:
        results = knowledge_retriever.retrieve(query, top_k)
        return {"results": results, "count": len(results)}
    except Exception as e:
        track_metric("knowledge_retrieval_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))

# Customer data endpoint
@app.get("/customer/{phone_number}")
async def get_customer(phone_number: str):
    """Get customer data"""
    track_metric("customer_lookup", {"phone_number": phone_number})
    
    customer_data = crm_tool.fetch_customer_data(phone_number)
    if customer_data:
        return customer_data
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
