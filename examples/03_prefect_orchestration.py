"""
Example 3: Prefect Orchestration

This example wraps the agent workflow in Prefect tasks and flows.
Prefect adds orchestration capabilities like logging, retries, and monitoring.

Learning objectives:
- Understand Prefect tasks and flows
- See how to add retry logic
- Learn about workflow logging and observability

Run this example:
    python examples/03_prefect_orchestration.py
"""

from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from prefect import flow, task
from prefect.logging import get_run_logger

# Import our modular components
from src.agents import create_agent_graph


# ============================================================================
# STEP 1: Define Prefect Tasks
# ============================================================================

@task(name="Initialize Agent", retries=2)
def initialize_agent():
    """Initialize the agent with retry logic.
    
    The @task decorator makes this a Prefect task.
    - retries=2 means it will retry up to 2 times on failure
    - Prefect automatically logs task execution
    """
    logger = get_run_logger()
    logger.info("🤖 Initializing agent...")
    
    agent = create_agent_graph()
    
    logger.info("✅ Agent initialized")
    return agent


@task(name="Run Query", retries=2)
def run_query(agent, query: str):
    """Run a query through the agent.
    
    This task:
    - Tracks execution time
    - Logs progress
    - Returns the result
    """
    logger = get_run_logger()
    logger.info(f"🔍 Processing: {query}")
    
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "iteration_count": 0,
        "final_answer": ""
    }
    
    # Run and time the execution
    start_time = datetime.now()
    result = agent.invoke(initial_state)
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"✅ Completed in {duration:.2f}s")
    logger.info(f"📊 Iterations: {result.get('iteration_count', 0)}")
    
    return result


@task(name="Format Results")
def format_results(result):
    """Format the agent's results into a summary.
    
    This task extracts key information and creates a clean summary.
    """
    logger = get_run_logger()
    logger.info("📋 Formatting results...")
    
    summary = {
        "final_answer": result.get("final_answer", "No answer"),
        "iterations": result.get("iteration_count", 0),
        "message_count": len(result.get("messages", [])),
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info("✅ Results formatted")
    return summary


# ============================================================================
# STEP 2: Define Prefect Flow
# ============================================================================

@flow(name="Agent Workflow with Prefect", log_prints=True)
def agent_workflow_with_prefect(query: str):
    """Main workflow that orchestrates the agent.
    
    The @flow decorator makes this a Prefect flow.
    - Flows orchestrate tasks
    - log_prints=True means print statements are logged
    - Prefect tracks the entire workflow execution
    
    Args:
        query: The question for the agent
        
    Returns:
        Summary of the execution
    """
    logger = get_run_logger()
    
    logger.info("=" * 60)
    logger.info("🚀 Starting Prefect-Orchestrated Agent Workflow")
    logger.info("=" * 60)
    
    # Execute tasks in sequence
    agent = initialize_agent()
    result = run_query(agent, query)
    summary = format_results(result)
    
    # Log summary
    logger.info("=" * 60)
    logger.info("📊 WORKFLOW SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Query: {query}")
    logger.info(f"Iterations: {summary['iterations']}")
    logger.info(f"Messages: {summary['message_count']}")
    logger.info(f"\n💡 Final Answer:\n{summary['final_answer']}")
    logger.info("=" * 60)
    
    return summary


# ============================================================================
# STEP 3: Run the Flow
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Example 3: Prefect Orchestration")
    print("=" * 60)
    print("\nThis example shows how Prefect adds:")
    print("- ✅ Automatic logging")
    print("- ✅ Retry logic")
    print("- ✅ Task tracking")
    print("- ✅ Workflow observability")
    print()
    
    # Run the flow
    result = agent_workflow_with_prefect(
        query="Calculate 42 * 13, then search for information about Prefect."
    )
    
    print("\n✅ Example complete!")
    print("\nKey takeaways:")
    print("- @task decorator creates reusable, retriable tasks")
    print("- @flow decorator orchestrates tasks into workflows")
    print("- Prefect automatically provides logging and observability")
    print("- Tasks can have retry logic for resilience")
    print("\nNext: Try examples/04_batch_processing.py for advanced patterns!")
