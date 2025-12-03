"""
Example 4: Batch Processing

This example shows advanced patterns for processing multiple queries.
It demonstrates parallel execution and result aggregation.

Learning objectives:
- Process multiple queries efficiently
- Understand flow composition
- Learn result aggregation patterns

Run this example:
    python examples/04_batch_processing.py
"""

from prefect import flow
from prefect.logging import get_run_logger

# Import the single query workflow
from src.workflows import agent_workflow


# ============================================================================
# STEP 1: Batch Processing Flow
# ============================================================================

@flow(name="Batch Agent Workflow")
def batch_workflow(queries: list[str]):
    """Process multiple queries through the agent.
    
    This flow demonstrates:
    - Calling other flows (flow composition)
    - Processing multiple items
    - Aggregating results
    
    Args:
        queries: List of questions to process
        
    Returns:
        List of results for each query
    """
    logger = get_run_logger()
    logger.info(f"🔄 Processing {len(queries)} queries in batch")
    
    results = []
    for i, query in enumerate(queries, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"📝 Query {i}/{len(queries)}: {query}")
        logger.info(f"{'='*60}")
        
        # Call the single query workflow
        result = agent_workflow(query)
        results.append(result)
    
    # Aggregate statistics
    total_iterations = sum(r["iterations"] for r in results)
    avg_iterations = total_iterations / len(results)
    
    logger.info(f"\n{'='*60}")
    logger.info("📊 BATCH SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total queries: {len(queries)}")
    logger.info(f"Total iterations: {total_iterations}")
    logger.info(f"Average iterations per query: {avg_iterations:.1f}")
    logger.info(f"{'='*60}")
    
    return results


# ============================================================================
# STEP 2: Parallel Processing (Advanced)
# ============================================================================

@flow(name="Parallel Batch Workflow")
def parallel_batch_workflow(queries: list[str]):
    """Process queries in parallel using Prefect's task runners.
    
    Note: This is an advanced pattern. For true parallel execution,
    you would configure a Prefect task runner (e.g., DaskTaskRunner).
    
    This example shows the pattern, but runs sequentially by default.
    """
    logger = get_run_logger()
    logger.info(f"🚀 Processing {len(queries)} queries (parallel pattern)")
    
    # In a real parallel setup, these would run concurrently
    # You would use: from prefect_dask import DaskTaskRunner
    # And configure: @flow(task_runner=DaskTaskRunner())
    
    results = []
    for query in queries:
        result = agent_workflow(query)
        results.append(result)
    
    logger.info(f"✅ Parallel batch complete: {len(results)} results")
    return results


# ============================================================================
# STEP 3: Run Examples
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Example 4: Batch Processing")
    print("=" * 60)
    
    # Example queries
    queries = [
        "What is 25 * 47?",
        "Search for information about artificial intelligence",
        "Analyze sentiment: 'This is an amazing product!'",
        "Calculate 100 + 200 + 300"
    ]
    
    print(f"\n📋 Processing {len(queries)} queries:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    print()
    
    # Run batch workflow
    results = batch_workflow(queries)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    for i, (query, result) in enumerate(zip(queries, results), 1):
        print(f"\nQuery {i}: {query}")
        print(f"Answer: {result['final_answer'][:100]}...")
        print(f"Iterations: {result['iterations']}")
    print("=" * 60)
    
    print("\n✅ Example complete!")
    print("\nKey takeaways:")
    print("- Flows can call other flows (flow composition)")
    print("- Batch processing allows handling multiple items")
    print("- Results can be aggregated for analytics")
    print("- Prefect supports parallel execution with task runners")
    print("\nNext steps:")
    print("- Try the exercises in exercises/")
    print("- Explore the modular code in src/")
    print("- Check out the workshop guide in docs/")
