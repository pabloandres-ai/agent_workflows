"""
Exercise 1: Create a Custom Tool

Your task: Create a new tool and integrate it with the agent.

DIFFICULTY: ⭐ Beginner

INSTRUCTIONS:
1. Create a new tool called 'get_weather' that simulates weather information
2. The tool should take a city name as input
3. Return a simulated weather report (temperature, conditions, etc.)
4. Add the tool to the agent and test it

HINTS:
- Use the @tool decorator from langchain_core.tools
- Look at src/tools/web_search.py for an example
- Tools should have a clear docstring (the LLM uses this!)
- Test your tool before adding it to the agent

BONUS CHALLENGES:
- Add error handling for invalid city names
- Include multiple weather attributes (temp, humidity, wind)
- Make the weather data more realistic with random variations
"""

import os
from typing import TypedDict, Annotated, Literal
import operator

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool


# ============================================================================
# TODO: CREATE YOUR WEATHER TOOL HERE
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    
    TODO: Implement this function!
    
    Args:
        city: The name of the city
        
    Returns:
        A weather report string
    """
    # YOUR CODE HERE
    # Example return: "Weather in San Francisco: 65°F, Sunny, Wind: 10mph"
    pass


# ============================================================================
# Agent Setup (Already implemented for you)
# ============================================================================

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    iteration_count: int


def agent_node(state: AgentState) -> AgentState:
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=os.getenv("ANTHROPIC_API_KEY", "")
    )
    
    # TODO: Add your weather tool to this list
    tools = [get_weather]  # Add more tools if you want!
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
    
    tools = [get_weather]  # TODO: Make sure this matches your tools list above
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
# Test Your Tool
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1: Create a Custom Tool")
    print("=" * 60)
    
    # Test your tool directly first
    print("\n🧪 Testing tool directly:")
    print("-" * 60)
    try:
        result = get_weather("San Francisco")
        print(f"✅ Tool result: {result}")
    except Exception as e:
        print(f"❌ Tool error: {e}")
        print("Fix your tool implementation before testing with the agent!")
        exit(1)
    
    # Test with the agent
    print("\n🤖 Testing with agent:")
    print("-" * 60)
    
    graph = create_graph()
    
    initial_state = {
        "messages": [
            HumanMessage(content="What's the weather like in New York?")
        ],
        "iteration_count": 0
    }
    
    result = graph.invoke(initial_state)
    
    final_message = result["messages"][-1]
    if isinstance(final_message, AIMessage):
        print(f"\n💡 Agent's Answer:\n{final_message.content}")
    
    print("\n✅ Exercise complete!")
    print("\nCheck your implementation:")
    print("- Does the tool return realistic weather data?")
    print("- Does the agent successfully use your tool?")
    print("- Did you add a clear docstring?")
    print("\nNext: Try exercise_2_new_agent.py!")
