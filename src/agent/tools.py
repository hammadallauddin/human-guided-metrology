"""
Tools for the human-guided meteorology agent.
"""

from typing import Any, Dict, Optional
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from src.config.settings import settings


@tool
def search(location: str) -> Dict[str, Any]:
    """
    Search for weather information at a specific location.
    
    Args:
        location: The location to search for weather information
        
    Returns:
        Search response containing weather information
    """
    query = f"weather in {location}"
    print(f'Performing Web Search for: {query}')
    
    # Use Tavily API key from environment
    web_search_tool = TavilySearch(
        max_results=1, 
        include_answer=True,
        tavily_api_key=settings.tavily_api_key
    )
    search_response = web_search_tool.invoke({"query": query})
    
    return search_response


@tool
def ask_human(question: str) -> str:
    """
    Ask the human a question and get their response.
    
    Args:
        question: The question to ask the human
        
    Returns:
        Human response to the question
    """
    print('Asking human...')
    # Note: This would integrate with langgraph's interrupt functionality
    # For now, we'll return a placeholder
    return question
