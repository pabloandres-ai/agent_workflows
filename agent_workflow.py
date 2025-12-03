"""
LangGraph + Prefect Agent Workflow Demo

⚠️  NOTE: This is the original all-in-one demo file.
    For the workshop, please use the modular structure:
    - Examples: examples/01_basic_agent.py through 04_batch_processing.py
    - Exercises: exercises/exercise_1_custom_tool.py and exercise_2_new_agent.py
    - Modular code: src/tools/, src/agents/, src/workflows/
    
    This file is kept for reference and as a standalone demo.

This demo shows how to build an AI agent using LangGraph and orchestrate it with Prefect.
The agent can search the web, analyze data, and make decisions based on the results.

Requirements:
pip install langchain langgraph langchain-google-genai prefect httpx
"""

import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal
from datetime import datetime
import operator

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

from prefect import flow, task
from prefect.logging import get_run_logger


# ============================================================================
# TOOLS - Define what the agent can do
# ============================================================================

@tool
def web_search(query: str) -> str:
    """Search the web for information. Use this when you need current information."""
    # Simulated web search - in production, integrate with real search API
    return f"Search results for '{query}': Found 5 relevant articles about this topic. Key findings include recent developments and expert opinions."


@tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations. Input should be a valid Python expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"


@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of text. Returns positive, negative, or neutral."""
    # Simple sentiment analysis simulation
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
    negative_words = ['bad', 'terrible', 'awful', 'poor', 'horrible']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Sentiment: Positive"
    elif neg_count > pos_count:
        return "Sentiment: Negative"
    else:
        return "Sentiment: Neutral"


# ============================================================================
# AGENT STATE - Define what information flows through the graph
# ============================================================================

class AgentState(TypedDict):
    """State of the agent workflow"""
    messages: Annotated[list, operator.add]
    next_step: str
    iteration_count: int
    final_answer: str


# ============================================================================
# LANGGRAPH NODES - Define agent behavior
# ============================================================================

def agent_node(state: AgentState) -> AgentState:
    """Main agent reasoning node - decides what to do next"""
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
    """Decide whether to continue or end the workflow"""
    last_message = state["messages"][-1]
    
    # Check if we've hit iteration limit
    if state.get("iteration_count", 0) >= 5:
        return "end"
    
    # If the last message has tool calls, continue to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we're done
    return "end"


def finalize_response(state: AgentState) -> AgentState:
    """Extract the final answer from the conversation"""
    last_message = state["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        final_answer = last_message.content
    else:
        final_answer = "No response generated"
    
    return {"final_answer": final_answer}


# ============================================================================
# BUILD LANGGRAPH WORKFLOW
# ============================================================================

def create_agent_graph():
    """Build the LangGraph agent workflow"""
    
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


# ============================================================================
# PREFECT TASKS - Orchestrate the workflow
# ============================================================================

@task(name="Initialize Agent", retries=2)
def initialize_agent_task():
    """Initialize the LangGraph agent"""
    logger = get_run_logger()
    logger.info("🤖 Initializing LangGraph agent...")
    
    agent = create_agent_graph()
    logger.info("✅ Agent initialized successfully")
    return agent


@task(name="Run Agent Query", retries=2)
def run_agent_query_task(agent, query: str):
    """Execute a query through the agent"""
    logger = get_run_logger()
    logger.info(f"🔍 Processing query: {query}")
    
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "iteration_count": 0,
        "final_answer": ""
    }
    
    # Run the agent
    start_time = datetime.now()
    result = agent.invoke(initial_state)
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"✅ Query completed in {duration:.2f}s")
    logger.info(f"📊 Iterations: {result.get('iteration_count', 0)}")
    
    return result


@task(name="Process Results")
def process_results_task(result):
    """Process and format the agent's results"""
    logger = get_run_logger()
    logger.info("📋 Processing agent results...")
    
    final_answer = result.get("final_answer", "No answer generated")
    iteration_count = result.get("iteration_count", 0)
    message_count = len(result.get("messages", []))
    
    summary = {
        "final_answer": final_answer,
        "iterations": iteration_count,
        "total_messages": message_count,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"✅ Processing complete: {iteration_count} iterations, {message_count} messages")
    return summary


# ============================================================================
# PREFECT FLOW - Main orchestration
# ============================================================================

@flow(name="LangGraph Agent Workflow", log_prints=True)
def agent_workflow(query: str = "What is 25 * 47? Also search for information about AI agents."):
    """
    Main Prefect flow that orchestrates the LangGraph agent workflow.
    
    Args:
        query: The question or task for the agent to process
    """
    logger = get_run_logger()
    logger.info("=" * 60)
    logger.info("🚀 Starting LangGraph + Prefect Agent Workflow")
    logger.info("=" * 60)
    
    # Step 1: Initialize the agent
    agent = initialize_agent_task()
    
    # Step 2: Run the query through the agent
    result = run_agent_query_task(agent, query)
    
    # Step 3: Process and format results
    summary = process_results_task(result)
    
    # Print final summary
    logger.info("=" * 60)
    logger.info("📊 WORKFLOW SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Query: {query}")
    logger.info(f"Iterations: {summary['iterations']}")
    logger.info(f"Total Messages: {summary['total_messages']}")
    logger.info(f"\n💡 Final Answer:\n{summary['final_answer']}")
    logger.info("=" * 60)
    
    return summary


# ============================================================================
# EXAMPLE: Multiple Queries Workflow
# ============================================================================

@flow(name="Batch Agent Workflow")
def batch_agent_workflow(queries: list[str]):
    """Process multiple queries through the agent workflow"""
    logger = get_run_logger()
    logger.info(f"🔄 Processing {len(queries)} queries in batch...")
    
    results = []
    for i, query in enumerate(queries, 1):
        logger.info(f"\n📝 Query {i}/{len(queries)}")
        result = agent_workflow(query)
        results.append(result)
    
    logger.info(f"✅ Batch processing complete: {len(results)} queries processed")
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example 1: Single query
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Single Query Workflow")
    print("=" * 60)
    
    result = agent_workflow(
        query="Calculate 156 * 89, then analyze the sentiment of this text: 'This is an amazing product!'"
    )
    
    # Example 2: Batch queries
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Query Workflow")
    print("=" * 60)
    
    queries = [
        "What is 42 * 13?",
        "Search for information about machine learning",
        "Analyze sentiment: 'This was a terrible experience'"
    ]
    
    batch_results = batch_agent_workflow(queries)
    
    print("\n✅ All workflows completed successfully!")