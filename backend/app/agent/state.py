from typing import TypedDict, Optional, List, Dict
from datetime import datetime

class AgentState(TypedDict):
    phone_number: str
    current_state: str
    customer_data: Optional[Dict]
    conversation_history: List[Dict]
    user_memory: Optional[Dict]
    retrieved_knowledge: List[Dict]
    tool_calls: List[Dict]
    agent_response: str
    next_state: str
    metadata: Dict
    timestamp: str
