"""
Workflow management for the human-guided meteorology agent.
"""

from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import InMemorySaver
from src.agent.core import Agent


class HumanInLoopState(TypedDict):
    """State for the human in loop workflow."""
    query: str
    agent_response: Any
    web_search_response: Dict[str, Any]


class AgentWorkflow:
    """Manages the agent workflow using langgraph."""
    
    def __init__(self):
        """Initialize the workflow."""
        self.agent = Agent()
        self.workflow = self._build_workflow()
        self.memory = InMemorySaver()
        self.app = self.workflow.compile(checkpointer=self.memory)
    
    def _build_workflow(self) -> StateGraph:
        """Build the agent workflow graph."""
        workflow = StateGraph(HumanInLoopState)
        
        workflow.add_node("run_agent", self._run_agent)
        workflow.add_edge(START, "run_agent")
        workflow.add_edge("run_agent", END)
        
        return workflow
    
    def _run_agent(self, state: HumanInLoopState) -> HumanInLoopState:
        """Run the agent and update the state."""
        result = self.agent.run(state['query'])
        
        if result['web_search_response']:
            state['web_search_response'] = result['web_search_response']
        else:
            state['agent_response'] = result['agent_response']
        
        return state
    
    def invoke(self, query: str, thread_id: str = "1") -> Dict[str, Any]:
        """
        Invoke the workflow with a query.
        
        Args:
            query: The user's query
            thread_id: The thread ID for conversation state
            
        Returns:
            Workflow response
        """
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.invoke({"query": query}, config=config)
    
    def resume(self, response: str, thread_id: str = "1") -> Dict[str, Any]:
        """
        Resume the workflow with a human response.
        
        Args:
            response: The human's response
            thread_id: The thread ID for conversation state
            
        Returns:
            Workflow response
        """
        from langgraph.types import Command
        
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.invoke(Command(resume=response), config=config)