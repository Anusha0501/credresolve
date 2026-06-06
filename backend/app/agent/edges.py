from typing import Literal
from app.agent.state import AgentState

def route_from_greeting(state: AgentState) -> Literal["Authentication", "EndConversation"]:
    """Route from Greeting state"""
    # In a real implementation, this would check if borrower is willing to proceed
    return "Authentication"

def route_from_authentication(state: AgentState) -> Literal["ContextGathering", "EndConversation"]:
    """Route from Authentication state"""
    customer_data = state.get("customer_data")
    if customer_data:
        return "ContextGathering"
    return "EndConversation"

def route_from_context(state: AgentState) -> Literal["Diagnosis", "EndConversation"]:
    """Route from ContextGathering state"""
    # In a real implementation, this would check if borrower provided information
    return "Diagnosis"

def route_from_diagnosis(state: AgentState) -> Literal["KnowledgeRetrieval", "ToolExecution", "Negotiation", "Escalation", "EndConversation"]:
    """Route from Diagnosis state"""
    next_state = state.get("next_state", "ToolExecution")
    if next_state in ["KnowledgeRetrieval", "ToolExecution", "Negotiation", "Escalation", "EndConversation"]:
        return next_state
    return "ToolExecution"

def route_from_knowledge(state: AgentState) -> Literal["ToolExecution", "Negotiation"]:
    """Route from KnowledgeRetrieval state"""
    next_state = state.get("next_state", "ToolExecution")
    return next_state if next_state in ["ToolExecution", "Negotiation"] else "ToolExecution"

def route_from_tool(state: AgentState) -> Literal["Negotiation", "Resolution", "Escalation"]:
    """Route from ToolExecution state"""
    next_state = state.get("next_state", "Negotiation")
    return next_state if next_state in ["Negotiation", "Resolution", "Escalation"] else "Negotiation"

def route_from_negotiation(state: AgentState) -> Literal["Resolution", "Escalation", "FollowUp", "EndConversation"]:
    """Route from Negotiation state"""
    next_state = state.get("next_state", "Resolution")
    return next_state if next_state in ["Resolution", "Escalation", "FollowUp", "EndConversation"] else "Resolution"

def route_from_escalation(state: AgentState) -> Literal["Resolution", "FollowUp", "EndConversation"]:
    """Route from Escalation state"""
    next_state = state.get("next_state", "FollowUp")
    return next_state if next_state in ["Resolution", "FollowUp", "EndConversation"] else "FollowUp"

def route_from_resolution(state: AgentState) -> Literal["FollowUp", "EndConversation"]:
    """Route from Resolution state"""
    next_state = state.get("next_state", "EndConversation")
    return next_state if next_state in ["FollowUp", "EndConversation"] else "EndConversation"
