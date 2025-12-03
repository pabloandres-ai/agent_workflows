"""
Base Agent Implementation

This module defines the core agent workflow using LangGraph.
The agent can reason, use tools, and make decisions based on the results.
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
from langchain_core.messages import AIMessage

from src.tools import web_search, calculate, analyze_sentiment


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(TypedDict):
    """State of the agent workflow.
    
    Attributes:
        messages: List of messages in the conversation (accumulated)
        next_step: The next step to take in the workflow
        iteration_count: Number of iterations the agent has performed
        final_answer: The final answer from the agent
    """
    messages: Annotated[list, operator.add]
    next_step: str
    iteration_count: int
    final_answer: str


# ============================================================================
# AGENT NODES
# ============================================================================

def agent_node(state: AgentState) -> AgentState:
    """Main agent reasoning node - decides what to do next.
    
    This node:
    1. Takes the current conversation state
    2. Passes it to the LLM with tools
    3. Gets back either a tool call or a final response
    4. Updates the state with the response
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with the agent's response
    """
    # Initialize the LLM with tools
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
    
    tools = [web_search, calculate, analyze_sentiment]
    llm_with_tools = llm.bind_tools(tools)
    
    # Get the agent's response
    response = llm_with_tools.invoke(state["messages"])
    
    # Update state
    return {
        "messages": [response],
        "iteration_count": state.get("iteration_count", 0) + 1
    }


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Decide whether to continue or end the workflow.
    
    This is a conditional edge that determines the next step:
    - If the agent wants to use tools, route to "tools"
    - If the agent has a final answer or hit iteration limit, route to "end"
    
    Args:
        state: Current agent state
        
    Returns:
        "tools" to continue with tool execution, "end" to finish
    """
    last_message = state["messages"][-1]
    
    # Check if we've hit iteration limit (safety measure)
    if state.get("iteration_count", 0) >= 5:
        return "end"
    
    # If the last message has tool calls, continue to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we're done
    return "end"


def finalize_response(state: AgentState) -> AgentState:
    """Extract the final answer from the conversation.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with the final answer extracted
    """
    last_message = state["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        final_answer = last_message.content
    else:
        final_answer = "No response generated"
    
    return {"final_answer": final_answer}


# ============================================================================
# GRAPH BUILDER
# ============================================================================

def create_agent_graph():
    """Build the LangGraph agent workflow.
    
    The workflow follows this pattern:
    1. Start at the agent node
    2. Agent decides what to do (conditional edge)
    3. If tools needed: execute tools -> back to agent
    4. If done: finalize response -> end
    
    Returns:
        Compiled LangGraph workflow ready to execute
        
    Example:
        >>> graph = create_agent_graph()
        >>> result = graph.invoke({"messages": [HumanMessage(content="Hello")]})
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    
    # Create tool node with all tools
    tools = [web_search, calculate, analyze_sentiment]
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    
    workflow.add_node("finalize", finalize_response)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": "finalize"
        }
    )
    
    # After using tools, go back to agent
    workflow.add_edge("tools", "agent")
    
    # After finalizing, end
    workflow.add_edge("finalize", END)
    
    return workflow.compile()
