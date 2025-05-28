"""
Configuration settings for the LLM Chatbot.
This module contains the configuration class and default settings.
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Config:
    """Configuration settings for the chatbot."""
    
    # Model settings
    model_name: str = "gpt2"  # Default model
    max_response_length: int = 100  # Maximum length of generated responses
    temperature: float = 0.7  # Temperature for text generation
    
    # Conversation settings
    max_history_length: int = 10  # Maximum number of exchanges to keep in context
    save_conversations: bool = True  # Whether to save conversations
    conversation_dir: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "conversations")
    
    # Web interface settings
    web_host: str = "0.0.0.0"  # Host for web interface
    web_port: int = 8000  # Port for web interface
    
    # Debug settings
    debug: bool = False  # Debug mode
    
    def __post_init__(self):
        """Ensure directories exist after initialization."""
        os.makedirs(self.conversation_dir, exist_ok=True)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "model_name": self.model_name,
            "max_response_length": self.max_response_length,
            "temperature": self.temperature,
            "max_history_length": self.max_history_length,
            "save_conversations": self.save_conversations,
            "conversation_dir": self.conversation_dir,
            "web_host": self.web_host,
            "web_port": self.web_port,
            "debug": self.debug
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create config from dictionary."""
        return cls(**config_dict)
    
    def save(self, filepath: str) -> None:
        """Save config to JSON file."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'Config':
        """Load config from JSON file."""
        import json
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
