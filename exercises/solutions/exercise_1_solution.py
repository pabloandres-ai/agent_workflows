"""
Solution: Exercise 1 - Create a Custom Tool

This is the complete solution for Exercise 1.
"""

import os
import random
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal
import operator

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool


# ============================================================================
# SOLUTION: Weather Tool
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    
    Args:
        city: The name of the city
        
    Returns:
        A weather report string with temperature, conditions, and wind
    """
    # Validate input
    if not city or not city.strip():
        return "Error: Please provide a valid city name"
    
    # Simulated weather data with some randomness
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Foggy"]
    temp = random.randint(50, 85)
    condition = random.choice(conditions)
    wind = random.randint(5, 25)
    humidity = random.randint(30, 80)
    
    return (
        f"Weather in {city.title()}: "
        f"{temp}°F, {condition}, "
        f"Wind: {wind}mph, "
        f"Humidity: {humidity}%"
    )


# ============================================================================
# Agent Setup
# ============================================================================

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    iteration_count: int


def agent_node(state: AgentState) -> AgentState:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
    
    tools = [get_weather]
    llm_with_tools = llm.bind_tools(tools)
    
    response = llm_with_tools.invoke(state["messages"])
    
    return {
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    last_message = state["messages"][-1]
    
    if state.get("iteration_count", 0) >= 5:
        return "end"
    
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    return "end"


def create_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", agent_node)
    
    tools = [get_weather]
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Solution: Exercise 1 - Create a Custom Tool")
    print("=" * 60)
    
    # Test tool directly
    print("\n🧪 Testing tool directly:")
    print("-" * 60)
    print(get_weather("San Francisco"))
    print(get_weather("New York"))
    print(get_weather(""))  # Test error handling
    
    # Test with agent
    print("\n🤖 Testing with agent:")
    print("-" * 60)
    
    graph = create_graph()
    
    initial_state = {
        "messages": [
            HumanMessage(content="What's the weather like in Tokyo and London?")
        ],
        "iteration_count": 0
    }
    
    result = graph.invoke(initial_state)
    
    final_message = result["messages"][-1]
    if isinstance(final_message, AIMessage):
        print(f"\n💡 Agent's Answer:\n{final_message.content}")
    
    print("\n✅ Solution complete!")
