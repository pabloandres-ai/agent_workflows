"""
Agent Workflow - Prefect Orchestration

This module defines Prefect flows and tasks for orchestrating the LangGraph agent.
Prefect provides:
- Task retry logic
- Logging and observability
- Workflow scheduling
- Parallel execution
"""

from datetime import datetime
from langchain_core.messages import HumanMessage
from prefect import flow, task
from prefect.logging import get_run_logger

from src.agents import create_agent_graph


# ============================================================================
# PREFECT TASKS
# ============================================================================

@task(name="Initialize Agent", retries=2)
def initialize_agent_task():
    """Initialize the LangGraph agent.
    
    This task creates and compiles the agent graph.
    It has retry logic in case of initialization failures.
    
    Returns:
        Compiled LangGraph agent ready to execute
    """
    logger = get_run_logger()
    logger.info("🤖 Initializing LangGraph agent...")
    
    agent = create_agent_graph()
    logger.info("✅ Agent initialized successfully")
    return agent


@task(name="Run Agent Query", retries=2)
def run_agent_query_task(agent, query: str):
    """Execute a query through the agent.
    
    This task runs the agent with a given query and tracks execution time.
    
    Args:
        agent: The compiled LangGraph agent
        query: The question or task for the agent
        
    Returns:
        The agent's execution result including final answer and metadata
    """
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
    """Process and format the agent's results.
    
    This task extracts key information from the agent's execution
    and formats it into a summary.
    
    Args:
        result: The raw agent execution result
        
    Returns:
        A formatted summary dictionary
    """
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
# PREFECT FLOWS
# ============================================================================

@flow(name="LangGraph Agent Workflow", log_prints=True)
def agent_workflow(query: str = "What is 25 * 47? Also search for information about AI agents."):
    """Main Prefect flow that orchestrates the LangGraph agent workflow.
    
    This flow:
    1. Initializes the agent
    2. Runs the query through the agent
    3. Processes and formats the results
    
    Args:
        query: The question or task for the agent to process
        
    Returns:
        A summary of the agent's execution and final answer
        
    Example:
        >>> result = agent_workflow("Calculate 156 * 89")
        >>> print(result["final_answer"])
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


@flow(name="Batch Agent Workflow")
def batch_agent_workflow(queries: list[str]):
    """Process multiple queries through the agent workflow.
    
    This flow demonstrates how to process multiple queries,
    either sequentially or in parallel.
    
    Args:
        queries: List of questions or tasks for the agent
        
    Returns:
        List of summaries for each query
        
    Example:
        >>> queries = ["What is 42 * 13?", "Search for AI news"]
        >>> results = batch_agent_workflow(queries)
    """
    logger = get_run_logger()
    logger.info(f"🔄 Processing {len(queries)} queries in batch...")
    
    results = []
    for i, query in enumerate(queries, 1):
        logger.info(f"\n📝 Query {i}/{len(queries)}")
        result = agent_workflow(query)
        results.append(result)
    
    logger.info(f"✅ Batch processing complete: {len(results)} queries processed")
    return results
