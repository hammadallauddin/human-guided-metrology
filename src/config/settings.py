"""
Configuration management for the human-guided meteorology agent.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Google Gemini Configuration
        self.google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
        self.google_model: Optional[str] = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
        
        # LangSmith Configuration
        self.langsmith_api_key: Optional[str] = os.getenv("LANGSMITH_API_KEY")
        self.langsmith_project: Optional[str] = os.getenv("LANGSMITH_PROJECT", "human-guided-metrology")
        self.langsmith_tracing: bool = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
        
        # Tavily Configuration
        self.tavily_api_key: Optional[str] = os.getenv("TAVILY_API_KEY")
        
    def validate(self) -> None:
        """Validate that all required settings are present."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        if not self.tavily_api_key:
            raise ValueError("TAVILY_API_KEY environment variable is required")
        if not self.langsmith_api_key:
            raise ValueError("LANGSMITH_API_KEY environment variable is required")
    
    @property
    def gemini_model(self) -> str:
        """Get the Gemini model to use."""
        return self.google_model or "gemini-2.5-flash"


# Global settings instance
settings = Settings()
