from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    greeting_node,
    authentication_node,
    context_gathering_node,
    diagnosis_node,
    knowledge_retrieval_node,
    tool_execution_node,
    negotiation_node,
    escalation_node,
    resolution_node,
    followup_node,
    end_conversation_node
)
from app.agent.edges import (
    route_from_greeting,
    route_from_authentication,
    route_from_context,
    route_from_diagnosis,
    route_from_knowledge,
    route_from_tool,
    route_from_negotiation,
    route_from_escalation,
    route_from_resolution
)

def create_agent_graph() -> StateGraph:
    """Create the LangGraph state machine for debt collection agent"""
    
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("Greeting", greeting_node)
    workflow.add_node("Authentication", authentication_node)
    workflow.add_node("ContextGathering", context_gathering_node)
    workflow.add_node("Diagnosis", diagnosis_node)
    workflow.add_node("KnowledgeRetrieval", knowledge_retrieval_node)
    workflow.add_node("ToolExecution", tool_execution_node)
    workflow.add_node("Negotiation", negotiation_node)
    workflow.add_node("Escalation", escalation_node)
    workflow.add_node("Resolution", resolution_node)
    workflow.add_node("FollowUp", followup_node)
    workflow.add_node("EndConversation", end_conversation_node)
    
    # Set entry point
    workflow.set_entry_point("Greeting")
    
    # Add edges
    workflow.add_conditional_edges(
        "Greeting",
        route_from_greeting,
        {
            "Authentication": "Authentication",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "Authentication",
        route_from_authentication,
        {
            "ContextGathering": "ContextGathering",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "ContextGathering",
        route_from_context,
        {
            "Diagnosis": "Diagnosis",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "Diagnosis",
        route_from_diagnosis,
        {
            "KnowledgeRetrieval": "KnowledgeRetrieval",
            "ToolExecution": "ToolExecution",
            "Negotiation": "Negotiation",
            "Escalation": "Escalation",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "KnowledgeRetrieval",
        route_from_knowledge,
        {
            "ToolExecution": "ToolExecution",
            "Negotiation": "Negotiation"
        }
    )
    
    workflow.add_conditional_edges(
        "ToolExecution",
        route_from_tool,
        {
            "Negotiation": "Negotiation",
            "Resolution": "Resolution",
            "Escalation": "Escalation"
        }
    )
    
    workflow.add_conditional_edges(
        "Negotiation",
        route_from_negotiation,
        {
            "Resolution": "Resolution",
            "Escalation": "Escalation",
            "FollowUp": "FollowUp",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "Escalation",
        route_from_escalation,
        {
            "Resolution": "Resolution",
            "FollowUp": "FollowUp",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_conditional_edges(
        "Resolution",
        route_from_resolution,
        {
            "FollowUp": "FollowUp",
            "EndConversation": "EndConversation"
        }
    )
    
    workflow.add_edge("FollowUp", "EndConversation")
    workflow.add_edge("EndConversation", END)
    
    return workflow.compile()
