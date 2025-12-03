"""
Example 1: Basic Agent (No Tools)

This is the simplest possible LangGraph agent.
It demonstrates the core agent loop without any tool calling.

Learning objectives:
- Understand LangGraph state management
- See how messages flow through the graph
- Learn the basic agent node pattern

Run this example:
    python examples/01_basic_agent.py
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import operator

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage


# ============================================================================
# STEP 1: Define the State
# ============================================================================

class AgentState(TypedDict):
    """The state that flows through our graph.
    
    The 'Annotated[list, operator.add]' means that when we return
    {"messages": [new_message]}, it will be ADDED to the existing messages
    rather than replacing them.
    """
    messages: Annotated[list, operator.add]


# ============================================================================
# STEP 2: Define the Agent Node
# ============================================================================

def simple_agent(state: AgentState) -> AgentState:
    """A simple agent that just responds to messages.
    
    This node:
    1. Takes the current state (with messages)
    2. Sends messages to the LLM
    3. Returns the LLM's response
    """
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
    
    # Get the LLM's response
    response = llm.invoke(state["messages"])
    
    # Return the response (it will be added to messages)
    return {"messages": [response]}


# ============================================================================
# STEP 3: Build the Graph
# ============================================================================

def create_simple_graph():
    """Build a simple graph with just one node."""
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add our agent node
    workflow.add_node("agent", simple_agent)
    
    # Set the entry point
    workflow.set_entry_point("agent")
    
    # After the agent runs, end the workflow
    workflow.add_edge("agent", END)
    
    return workflow.compile()


# ============================================================================
# STEP 4: Run the Agent
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Example 1: Basic Agent (No Tools)")
    print("=" * 60)
    
    # Create the graph
    graph = create_simple_graph()
    
    # Create initial state with a user message
    initial_state = {
        "messages": [HumanMessage(content="Hello! Tell me a short joke about programming.")]
    }
    
    # Run the graph
    print("\n🤖 Running agent...\n")
    result = graph.invoke(initial_state)
    
    # Print the conversation
    print("Conversation:")
    print("-" * 60)
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"👤 Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"🤖 Agent: {msg.content}")
    print("-" * 60)
    
    print("\n✅ Example complete!")
    print("\nKey takeaways:")
    print("- LangGraph uses a state dictionary that flows through nodes")
    print("- Nodes are functions that take state and return updated state")
    print("- The graph defines how nodes connect and when to end")
    print("\nNext: Try examples/02_agent_with_tools.py to add tool calling!")
