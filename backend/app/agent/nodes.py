from typing import Dict, Any
from datetime import datetime
from app.agent.state import AgentState
from app.tools.mock_tools import crm_tool, payment_tool, ticket_tool, sms_tool
from app.memory.database import memory_db
from app.rag.retriever import knowledge_retriever
from app.monitoring.metrics import track_metric

def greeting_node(state: AgentState) -> AgentState:
    """
    State: Greeting
    Purpose: Welcome the borrower and establish initial contact
    Entry: Start of conversation
    Exit: Proceed to authentication or end if borrower refuses
    Failure: If borrower hangs up or refuses to engage, end conversation
    Recovery: Retry greeting with different approach
    """
    track_metric("state_entry", {"state": "Greeting"})
    
    phone_number = state.get("phone_number", "")
    
    # Check if this is a returning customer
    user_memory = memory_db.get_user_memory(phone_number)
    
    if user_memory:
        greeting = f"Namaste! Welcome back to CredResolve. I hope you're doing well today."
    else:
        greeting = "Namaste! Thank you for calling CredResolve. My name is AI Assistant and I'm here to help you with your account."
    
    state["agent_response"] = greeting
    state["current_state"] = "Greeting"
    state["user_memory"] = user_memory
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "Greeting", "next_state": "Authentication"})
    
    return state

def authentication_node(state: AgentState) -> AgentState:
    """
    State: Authentication
    Purpose: Verify borrower identity
    Entry: From Greeting
    Exit: Proceed to context gathering if authenticated
    Failure: If authentication fails, end conversation
    Recovery: Request alternative verification method
    """
    track_metric("state_entry", {"state": "Authentication"})
    
    phone_number = state.get("phone_number", "")
    
    # Fetch customer data
    customer_data = crm_tool.fetch_customer_data(phone_number)
    
    if customer_data:
        response = f"I see you're calling about your account. For verification, could you please confirm your name?"
        state["customer_data"] = customer_data
        state["agent_response"] = response
        state["current_state"] = "Authentication"
        state["next_state"] = "ContextGathering"
    else:
        response = "I'm unable to locate your account with this phone number. Please verify your number or contact our customer service."
        state["agent_response"] = response
        state["current_state"] = "Authentication"
        state["next_state"] = "EndConversation"
    
    state["timestamp"] = datetime.now().isoformat()
    track_metric("state_exit", {"state": "Authentication", "next_state": state["next_state"]})
    
    return state

def context_gathering_node(state: AgentState) -> AgentState:
    """
    State: ContextGathering
    Purpose: Gather information about borrower's current situation
    Entry: From Authentication
    Exit: Proceed to diagnosis
    Failure: If borrower refuses to provide information, escalate or end
    Recovery: Ask questions in different way
    """
    track_metric("state_entry", {"state": "ContextGathering"})
    
    customer_data = state.get("customer_data", {})
    user_memory = state.get("user_memory", {})
    
    response = f"Thank you for verifying, {customer_data.get('name', 'Sir/Madam')}. "
    response += f"I see you have an outstanding amount of ₹{customer_data.get('due_amount', 0):,.2f} on your {customer_data.get('loan_type', 'loan')}. "
    response += "Could you please tell me about your current situation and when you might be able to make a payment?"
    
    state["agent_response"] = response
    state["current_state"] = "ContextGathering"
    state["next_state"] = "Diagnosis"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "ContextGathering", "next_state": "Diagnosis"})
    
    return state

def diagnosis_node(state: AgentState) -> AgentState:
    """
    State: Diagnosis
    Purpose: Analyze borrower's situation and determine appropriate path
    Entry: From ContextGathering
    Exit: Route to knowledge retrieval, tool execution, negotiation, or escalation
    Failure: If analysis unclear, ask for more information
    Recovery: Re-route to context gathering
    """
    track_metric("state_entry", {"state": "Diagnosis"})
    
    # Analyze the situation based on customer data and conversation
    customer_data = state.get("customer_data", {})
    overdue_days = customer_data.get("overdue_days", 0)
    risk_category = customer_data.get("risk_category", "medium")
    
    # Simple routing logic based on risk and overdue days
    if risk_category == "high" and overdue_days > 60:
        state["next_state"] = "KnowledgeRetrieval"
    elif overdue_days < 30:
        state["next_state"] = "Negotiation"
    else:
        state["next_state"] = "ToolExecution"
    
    response = "I understand your situation. Let me check what options are available for you."
    
    state["agent_response"] = response
    state["current_state"] = "Diagnosis"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "Diagnosis", "next_state": state["next_state"]})
    
    return state

def knowledge_retrieval_node(state: AgentState) -> AgentState:
    """
    State: KnowledgeRetrieval
    Purpose: Retrieve relevant information from knowledge base
    Entry: From Diagnosis
    Exit: Proceed to tool execution or negotiation
    Failure: If retrieval fails, proceed without knowledge
    Recovery: Use fallback responses
    """
    track_metric("state_entry", {"state": "KnowledgeRetrieval"})
    
    customer_data = state.get("customer_data", {})
    query = f"settlement policy for {customer_data.get('risk_category', 'medium')} risk category"
    
    retrieved_docs = knowledge_retriever.retrieve(query, top_k=2)
    
    state["retrieved_knowledge"] = retrieved_docs
    
    if retrieved_docs:
        response = "Based on your situation, I can see some options that might help you. Let me calculate the details."
    else:
        response = "Let me check what payment options are available for you."
    
    state["agent_response"] = response
    state["current_state"] = "KnowledgeRetrieval"
    state["next_state"] = "ToolExecution"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "KnowledgeRetrieval", "next_state": "ToolExecution"})
    
    return state

def tool_execution_node(state: AgentState) -> AgentState:
    """
    State: ToolExecution
    Purpose: Execute relevant tools (payment calculation, SMS, etc.)
    Entry: From Diagnosis or KnowledgeRetrieval
    Exit: Proceed to negotiation, resolution, or escalation
    Failure: If tool fails, log error and continue
    Recovery: Use manual calculation or fallback
    """
    track_metric("state_entry", {"state": "ToolExecution"})
    
    customer_data = state.get("customer_data", {})
    due_amount = customer_data.get("due_amount", 0)
    
    # Calculate settlement options
    settlement = payment_tool.calculate_settlement(due_amount)
    
    tool_calls = [
        {
            "tool": "payment_tool",
            "function": "calculate_settlement",
            "input": {"amount": due_amount},
            "output": settlement
        }
    ]
    
    state["tool_calls"] = tool_calls
    
    response = f"I've calculated your options. You can settle your account by paying ₹{settlement['settlement_amount']:,.2f} instead of the full amount. "
    response += f"This would save you ₹{settlement['savings']:,.2f}. This offer is valid until {settlement['valid_until']}."
    
    state["agent_response"] = response
    state["current_state"] = "ToolExecution"
    state["next_state"] = "Negotiation"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "ToolExecution", "next_state": "Negotiation"})
    track_metric("tool_call", {"tool": "payment_tool", "success": True})
    
    return state

def negotiation_node(state: AgentState) -> AgentState:
    """
    State: Negotiation
    Purpose: Discuss payment terms and reach agreement
    Entry: From ToolExecution or Diagnosis
    Exit: Proceed to resolution, escalation, follow-up, or end
    Failure: If negotiation breaks down, escalate
    Recovery: Offer alternative terms
    """
    track_metric("state_entry", {"state": "Negotiation"})
    
    response = "Would you like to proceed with this settlement option, or would you prefer to discuss other payment arrangements?"
    
    state["agent_response"] = response
    state["current_state"] = "Negotiation"
    state["next_state"] = "Resolution"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "Negotiation", "next_state": "Resolution"})
    
    return state

def escalation_node(state: AgentState) -> AgentState:
    """
    State: Escalation
    Purpose: Handle cases that require human intervention
    Entry: From Diagnosis, ToolExecution, or Negotiation
    Exit: Proceed to resolution, follow-up, or end
    Failure: If escalation fails, end conversation
    Recovery: Schedule callback
    """
    track_metric("state_entry", {"state": "Escalation"})
    
    customer_data = state.get("customer_data", {})
    phone_number = state.get("phone_number", "")
    
    # Create escalation ticket
    ticket = ticket_tool.create_ticket(
        phone_number,
        "Escalation",
        "Case requires human intervention"
    )
    
    tool_calls = state.get("tool_calls", [])
    tool_calls.append({
        "tool": "ticket_tool",
        "function": "create_ticket",
        "input": {"phone_number": phone_number, "issue_type": "Escalation"},
        "output": ticket
    })
    
    state["tool_calls"] = tool_calls
    
    response = "I understand this requires special attention. I've created a ticket for our senior team member who will review your case within 24 hours. They will call you at your preferred time."
    
    state["agent_response"] = response
    state["current_state"] = "Escalation"
    state["next_state"] = "FollowUp"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "Escalation", "next_state": "FollowUp"})
    track_metric("escalation", {"phone_number": phone_number})
    
    return state

def resolution_node(state: AgentState) -> AgentState:
    """
    State: Resolution
    Purpose: Confirm agreement and document resolution
    Entry: From Negotiation or Escalation
    Exit: Proceed to follow-up or end
    Failure: If confirmation fails, re-negotiate
    Recovery: Re-enter negotiation
    """
    track_metric("state_entry", {"state": "Resolution"})
    
    customer_data = state.get("customer_data", {})
    phone_number = state.get("phone_number", "")
    
    # Send confirmation SMS
    sms = sms_tool.send_confirmation(
        phone_number,
        f"Thank you for your commitment. Your payment arrangement has been recorded."
    )
    
    tool_calls = state.get("tool_calls", [])
    tool_calls.append({
        "tool": "sms_tool",
        "function": "send_confirmation",
        "input": {"phone_number": phone_number},
        "output": sms
    })
    
    state["tool_calls"] = tool_calls
    
    response = "Thank you for your cooperation. I've sent you a confirmation SMS with the details. Is there anything else I can help you with today?"
    
    state["agent_response"] = response
    state["current_state"] = "Resolution"
    state["next_state"] = "EndConversation"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "Resolution", "next_state": "EndConversation"})
    track_metric("resolution", {"phone_number": phone_number})
    
    return state

def followup_node(state: AgentState) -> AgentState:
    """
    State: FollowUp
    Purpose: Schedule callback and document next steps
    Entry: From Escalation or Resolution
    Exit: Proceed to end conversation
    Failure: If scheduling fails, log for manual follow-up
    Recovery: Use default callback time
    """
    track_metric("state_entry", {"state": "FollowUp"})
    
    response = "I've scheduled a follow-up for you. Our team will contact you as discussed. Thank you for speaking with CredResolve today. Have a great day!"
    
    state["agent_response"] = response
    state["current_state"] = "FollowUp"
    state["next_state"] = "EndConversation"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "FollowUp", "next_state": "EndConversation"})
    
    return state

def end_conversation_node(state: AgentState) -> AgentState:
    """
    State: EndConversation
    Purpose: Close conversation and save to memory
    Entry: From any state
    Exit: Conversation ends
    Failure: N/A
    Recovery: N/A
    """
    track_metric("state_entry", {"state": "EndConversation"})
    
    phone_number = state.get("phone_number", "")
    current_state = state.get("current_state", "")
    agent_response = state.get("agent_response", "")
    
    # Save conversation to memory
    memory_db.save_conversation(
        phone_number,
        current_state,
        state.get("conversation_history", [{}])[-1].get("message", ""),
        agent_response,
        state.get("metadata", {})
    )
    
    response = "Thank you for calling CredResolve. Have a wonderful day!"
    
    state["agent_response"] = response
    state["current_state"] = "EndConversation"
    state["next_state"] = "END"
    state["timestamp"] = datetime.now().isoformat()
    
    track_metric("state_exit", {"state": "EndConversation", "next_state": "END"})
    track_metric("conversation_end", {"phone_number": phone_number})
    
    return state
