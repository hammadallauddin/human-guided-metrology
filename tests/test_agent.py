"""
Tests for the agent core functionality.
"""

import pytest
from unittest.mock import Mock, patch
from src.agent.core import Agent
from src.config.settings import settings


class TestAgent:
    """Test cases for the Agent class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Mock the settings validation
        self.original_validate = settings.validate
        settings.validate = Mock()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        settings.validate = self.original_validate
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai')
    def test_agent_initialization(self, mock_genai, mock_model):
        """Test that agent initializes correctly."""
        # Arrange
        mock_genai.configure = Mock()
        mock_model_instance = Mock()
        mock_model.return_value = mock_model_instance
        
        # Act
        agent = Agent()
        
        # Assert
        assert agent.model is not None  # Just check that model was created
        mock_genai.configure.assert_called_once()
        mock_model.assert_called_once_with(settings.gemini_model)
    
    @patch('google.generativeai.GenerativeModel')
    def test_agent_run_basic_query(self, mock_model):
        """Test running the agent with a basic query."""
        # Arrange
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_part.text = "This is a test response"
        
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        agent = Agent()
        
        # Act
        result = agent.run("Test query")
        
        # Assert
        assert result['agent_response'] == "This is a test response"
        assert result['web_search_response'] is None
        mock_model_instance.generate_content.assert_called_once_with("Test query")
    
    @patch('google.generativeai.GenerativeModel')
    @patch('src.agent.tools.search')
    def test_agent_run_with_human_interaction(self, mock_search, mock_model):
        """Test running the agent with human interaction simulation."""
        # Arrange
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_part.text = "Okay! To get started, where are you located right now?"
        
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        # Mock the search tool
        mock_search.invoke.return_value = {
            "answer": "Sunny, 75°F in Karachi",
            "query": "weather in Karachi, Pakistan"
        }
        
        agent = Agent()
        
        # Act
        result = agent.run("Ask the user where they are, then look up the weather there")
        
        # Assert
        assert result['agent_response'] is None
        assert result['web_search_response'] is not None
        assert "Karachi" in result['web_search_response']['query']
        mock_model_instance.generate_content.assert_called_once()
        mock_search.invoke.assert_called_once()
    
    @patch('google.generativeai.GenerativeModel')
    @patch('src.agent.tools.search')
    @patch('src.agent.tools.ask_human')
    def test_agent_run_with_tool_call(self, mock_ask_human, mock_search, mock_model):
        """Test running the agent with a tool call."""
        # Arrange
        mock_response = Mock()
        mock_candidate = Mock()
        mock_content = Mock()
        mock_part = Mock()
        mock_part.text = "ask_human What is your location?"
        
        mock_content.parts = [mock_part]
        mock_candidate.content = mock_content
        mock_response.candidates = [mock_candidate]
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        # Mock the tools
        mock_ask_human.invoke.return_value = "Karachi"
        mock_search.invoke.return_value = {"answer": "Sunny, 75°F"}
        
        agent = Agent()
        
        # Act
        result = agent.run("Test query with tool call")
        
        # Assert
        assert result['agent_response'] is None
        assert result['web_search_response'] is not None
        mock_model_instance.generate_content.assert_called_once_with("Test query with tool call")
        mock_ask_human.invoke.assert_called_once_with("What is your location?")
        mock_search.invoke.assert_called_once_with({"location": "Karachi"})
