"""
Example 2: Agent with Tools

This example adds tool calling capabilities to the agent.
The agent can now use tools to perform tasks like calculations and web searches.

Learning objectives:
- Understand how to bind tools to an LLM
- Learn conditional routing based on tool calls
- See the agent-tool loop in action

Run this example:
    python examples/02_agent_with_tools.py
"""

import os
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
# STEP 1: Define Tools
# ============================================================================

@tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return f"Search results for '{query}': Found relevant information about this topic."


# ============================================================================
# STEP 2: Define State
# ============================================================================

class AgentState(TypedDict):
    """State with messages and iteration tracking."""
    messages: Annotated[list, operator.add]
    iteration_count: int


# ============================================================================
# STEP 3: Define Agent Node
# ============================================================================

def agent_with_tools(state: AgentState) -> AgentState:
    """Agent that can decide to use tools.
    
    The LLM will either:
    1. Return a tool call (to use a tool)
    2. Return a regular response (final answer)
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
    
    # Bind tools to the LLM
    tools = [calculate, web_search]
    llm_with_tools = llm.bind_tools(tools)
    
    # Get response
    response = llm_with_tools.invoke(state["messages"])
    
    return {
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


# ============================================================================
# STEP 4: Define Conditional Logic
# ============================================================================

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Decide whether to use tools or end.
    
    This is the key to the agent loop:
    - If the agent wants to use a tool, route to "tools"
    - If the agent has a final answer, route to "end"
    """
    last_message = state["messages"][-1]
    
    # Safety: limit iterations
    if state.get("iteration_count", 0) >= 5:
        print("⚠️  Max iterations reached")
        return "end"
    
    # Check if there are tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        print(f"🔧 Agent wants to use tool: {last_message.tool_calls[0]['name']}")
        return "tools"
    
    print("✅ Agent has final answer")
    return "end"


# ============================================================================
# STEP 5: Build the Graph
# ============================================================================

def create_agent_with_tools_graph():
    """Build a graph with agent and tools nodes."""
    
    workflow = StateGraph(AgentState)
    
    # Add agent node
    workflow.add_node("agent", agent_with_tools)
    
    # Add tools node (LangGraph provides this!)
    tools = [calculate, web_search]
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edge from agent
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",  # If tools needed, go to tools
            "end": END         # If done, end
        }
    )
    
    # After using tools, go back to agent
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


# ============================================================================
# STEP 6: Run the Agent
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Example 2: Agent with Tools")
    print("=" * 60)
    
    # Create the graph
    graph = create_agent_with_tools_graph()
    
    # Create initial state
    initial_state = {
        "messages": [
            HumanMessage(content="What is 156 * 89? Also search for information about LangGraph.")
        ],
        "iteration_count": 0
    }
    
    # Run the graph
    print("\n🤖 Running agent with tools...\n")
    result = graph.invoke(initial_state)
    
    # Print results
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"Total iterations: {result['iteration_count']}")
    print(f"Total messages: {len(result['messages'])}")
    
    # Print final answer
    final_message = result["messages"][-1]
    if isinstance(final_message, AIMessage):
        print(f"\n💡 Final Answer:\n{final_message.content}")
    
    print("\n✅ Example complete!")
    print("\nKey takeaways:")
    print("- Tools are bound to the LLM with .bind_tools()")
    print("- Conditional edges route based on whether tools are needed")
    print("- The agent-tool loop continues until a final answer is reached")
    print("\nNext: Try examples/03_prefect_orchestration.py to add Prefect!")
