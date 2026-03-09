"""
Core agent implementation for the human-guided meteorology agent.
"""

from typing import Dict, Any, Optional
import google.generativeai as genai
from src.config.settings import settings
from src.agent.tools import search, ask_human


class Agent:
    """Main agent class that handles Gemini model interactions."""
    
    def __init__(self):
        """Initialize the agent with configuration."""
        settings.validate()
        self._configure_gemini()
        self.model = self._create_model()
    
    def _configure_gemini(self) -> None:
        """Configure the Gemini API with the provided API key."""
        genai.configure(api_key=settings.google_api_key)
    
    def _create_model(self) -> genai.GenerativeModel:
        """Create and return a Gemini model instance."""
        return genai.GenerativeModel(settings.gemini_model)
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the agent with the given query.
        
        Args:
            query: The user's query
            
        Returns:
            Dictionary containing agent response and any search results
        """
        print('Running agent...')
        
        # Generate content with Gemini
        response = self.model.generate_content(query)
        
        result = {
            'agent_response': None,
            'web_search_response': None
        }
        
        # Check if response contains tool calls (simplified check)
        if hasattr(response, 'candidates') and response.candidates:
            content = response.candidates[0].content
            
            # Check if the response is asking for human input
            response_text = content.parts[0].text.lower()
            if any(keyword in response_text for keyword in ['where are you', 'what is your location', 'where are you located', 'ask the user where']):
                # This is a human interaction request - simulate human response
                print('Detected human interaction request, simulating location response...')
                human_response = "Karachi, Pakistan"  # Simulated human response
                search_response = search.invoke({"location": human_response})
                
                # Format the weather response in a pretty way
                formatted_response = self._format_weather_response(search_response, human_response)
                result['web_search_response'] = formatted_response
            else:
                result['agent_response'] = content.parts[0].text
        else:
            result['agent_response'] = response.text
        
        return result
    
    def _format_weather_response(self, search_response: Dict[str, Any], location: str) -> Dict[str, Any]:
        """
        Format the weather response in a pretty, user-friendly way.
        
        Args:
            search_response: Raw search response from Tavily
            location: The location for which weather was searched
            
        Returns:
            Formatted weather response
        """
        try:
            # Extract weather information from the search response
            if 'answer' in search_response:
                raw_answer = search_response['answer']
                
                # Create a pretty formatted response
                formatted_response = {
                    'location': location,
                    'weather_summary': self._extract_weather_summary(raw_answer),
                    'temperature': self._extract_temperature(raw_answer),
                    'conditions': self._extract_conditions(raw_answer),
                    'humidity': self._extract_humidity(raw_answer),
                    'wind': self._extract_wind_info(raw_answer),
                    'raw_data': search_response,
                    'formatted_display': self._create_pretty_display(raw_answer, location)
                }
                
                return formatted_response
            else:
                return {
                    'location': location,
                    'error': 'No weather data found',
                    'raw_data': search_response
                }
        except Exception as e:
            return {
                'location': location,
                'error': f'Error formatting weather data: {str(e)}',
                'raw_data': search_response
            }
    
    def _extract_weather_summary(self, raw_answer: str) -> str:
        """Extract weather summary from raw answer."""
        # Simple extraction - in a real implementation, you'd use more sophisticated parsing
        if 'mist' in raw_answer.lower():
            return "Mist"
        elif 'sunny' in raw_answer.lower():
            return "Sunny"
        elif 'rain' in raw_answer.lower():
            return "Rainy"
        elif 'cloud' in raw_answer.lower():
            return "Cloudy"
        else:
            return "Clear"
    
    def _extract_temperature(self, raw_answer: str) -> str:
        """Extract temperature from raw answer."""
        import re
        # Look for temperature patterns like "23.2°C" or "73.8°F"
        temp_match = re.search(r'(\d+\.?\d*)°[CF]', raw_answer)
        if temp_match:
            return temp_match.group(0)
        return "N/A"
    
    def _extract_conditions(self, raw_answer: str) -> str:
        """Extract weather conditions from raw answer."""
        # Look for condition keywords
        conditions = []
        if 'mist' in raw_answer.lower():
            conditions.append("Mist")
        if 'wind' in raw_answer.lower() or 'wnw' in raw_answer.lower():
            conditions.append("Windy")
        if 'humidity' in raw_answer.lower():
            conditions.append("Humid")
        
        return ", ".join(conditions) if conditions else "Clear"
    
    def _extract_humidity(self, raw_answer: str) -> str:
        """Extract humidity from raw answer."""
        import re
        # Look for humidity patterns like "humidity is 89%"
        humidity_match = re.search(r'humidity.*?(\d+)%', raw_answer, re.IGNORECASE)
        if humidity_match:
            return f"{humidity_match.group(1)}%"
        return "N/A"
    
    def _extract_wind_info(self, raw_answer: str) -> str:
        """Extract wind information from raw answer."""
        import re
        # Look for wind patterns like "9.6 mph" or "15.5 kph"
        wind_match = re.search(r'(\d+\.?\d*)\s*(mph|kph|kph)', raw_answer, re.IGNORECASE)
        if wind_match:
            return f"{wind_match.group(1)} {wind_match.group(2)}"
        return "N/A"
    
    def _create_pretty_display(self, raw_answer: str, location: str) -> str:
        """Create a pretty display string for the weather."""
        temp = self._extract_temperature(raw_answer)
        conditions = self._extract_conditions(raw_answer)
        humidity = self._extract_humidity(raw_answer)
        wind = self._extract_wind_info(raw_answer)
        
        pretty_display = f"""
🌤️  WEATHER REPORT FOR {location.upper()}
{'='*50}
🌡️  Temperature: {temp}
☁️  Conditions: {conditions}
💧 Humidity: {humidity}
💨 Wind: {wind}
{'='*50}
{raw_answer}
"""
        return pretty_display
