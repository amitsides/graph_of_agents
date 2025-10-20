from typing import Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Import necessary classes from base_agent
class AgentState(Enum):
    """Lifecycle states for agents."""
    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Represents a message between agents or for internal processing."""
    message_id: str
    sender_id: str
    recipient_id: str
    content: dict
    message_type: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = None

class LlmAgent(BaseAgent):
    """
    LLM-powered agent that extends BaseAgent with LLM capabilities.
    Can process natural language inputs and generate responses using language models.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        description: str = "",
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: str = None
    ):
        """Initialize the LLM agent."""
        super().__init__(agent_id, name, description)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt or f"You are {name}, {description}"
        self._llm_conversation_history = []
    
    def execute(self, task: Any) -> dict:
        """Execute a task using LLM capabilities."""
        if self.state != AgentState.RUNNING:
            raise RuntimeError(f"Cannot execute task when agent is in state: {self.state}")
        
        # Convert task to prompt
        if isinstance(task, str):
            _llm_prompt = task
        elif isinstance(task, dict):
            _llm_prompt = task.get("prompt", str(task))
        else:
            _llm_prompt = str(task)
        
        # Simulate LLM processing
        _llm_exec_result = self._call_llm(_llm_prompt)
        
        print(f"LlmAgent '{self.name}' executed task")
        return _llm_exec_result
    
    def _call_llm(self, prompt: str) -> dict:
        """Simulate calling an LLM."""
        # Add to conversation history
        self._llm_conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Simulate LLM response
        _llm_simulated_response = f"[LLM Response] Processed prompt: '{prompt[:50]}...'"
        
        self._llm_conversation_history.append({
            "role": "assistant",
            "content": _llm_simulated_response
        })
        
        return {
            "success": True,
            "prompt": prompt,
            "response": _llm_simulated_response,
            "model": self.model_name,
            "temperature": self.temperature,
            "conversation_length": len(self._llm_conversation_history)
        }
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._llm_conversation_history.clear()
        print(f"LlmAgent '{self.name}' conversation history cleared")
    
    def get_history(self) -> list:
        """Get the conversation history."""
        return self._llm_conversation_history.copy()
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt."""
        self.system_prompt = prompt
        print(f"LlmAgent '{self.name}' system prompt updated")
    
    def _on_reset(self) -> None:
        """Hook called during reset."""
        super()._on_reset()
        self._llm_conversation_history.clear()
    
    def get_status(self) -> dict:
        """Get the current status including LLM-specific info."""
        _llm_status_dict = super().get_status()
        _llm_status_dict.update({
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "conversation_length": len(self._llm_conversation_history)
        })
        return _llm_status_dict
    
    def __repr__(self) -> str:
        return f"LlmAgent(id={self.agent_id}, name={self.name}, model={self.model_name}, state={self.state.value})"

print("LlmAgent class created successfully")
print(f"  - Extends BaseAgent with LLM capabilities")
print(f"  - Model: {LlmAgent.__init__.__defaults__[1]}")
print(f"  - Methods: execute(), clear_history(), get_history(), set_system_prompt()")
print(f"  - Maintains conversation history for context")
