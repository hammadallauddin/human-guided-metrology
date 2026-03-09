"""
Main entry point for the human-guided meteorology agent.
"""

from src.agent.workflow import AgentWorkflow


def main():
    """Main function to run the agent."""
    print("Initializing Human-Guided Meteorology Agent...")
    
    # Create the workflow
    workflow = AgentWorkflow()
    
    # Example usage
    print("\n=== Example 1: Basic Query ===")
    response = workflow.invoke("Ask the user where they are, then look up the weather there")
    print(f"Response: {response}")
    
    print("\n=== Example 2: Resume with Location ===")
    response = workflow.resume("Karachi")
    web_search_response = response.get('web_search_response', {})
    
    if 'formatted_display' in web_search_response:
        print("🌤️  PRETTY WEATHER REPORT:")
        print(web_search_response['formatted_display'])
    elif 'answer' in web_search_response:
        print(f"Agent Response: {web_search_response['answer']}")
    else:
        print("No weather data found")
    
    print("\nAgent execution completed!")


if __name__ == "__main__":
    main()