"""
Exercise 2: Build a Specialized Agent

Your task: Create a specialized agent with custom routing logic.

DIFFICULTY: ⭐⭐ Intermediate

INSTRUCTIONS:
1. Create an agent that specializes in data analysis
2. Add a custom node that validates queries before processing
3. Implement routing logic that rejects non-data-related queries
4. Add a summary node that formats results nicely

WORKFLOW:
    validate_query -> agent -> tools -> agent -> summarize -> END
                 \                                          /
                  \-> reject (if not data-related) --------/

HINTS:
- Create multiple nodes for different purposes
- Use conditional edges to route based on query content
- Think about what makes a query "data-related"
- The summary node can extract key insights

BONUS CHALLENGES:
- Add a node that suggests follow-up questions
- Implement a feedback loop for query refinement
- Track which tools are used most frequently
"""

import os
from typing import TypedDict, Annotated, Literal
import operator

from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool


# ============================================================================
# Tools for Data Analysis
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
def analyze_data(data: str) -> str:
    """Analyze a dataset and return statistics."""
    # Simulated data analysis
    return f"Analysis of '{data}': Mean=42, Median=40, StdDev=5.2, Count=100"


# ============================================================================
# TODO: DEFINE YOUR STATE
# ============================================================================

class DataAgentState(TypedDict):
    """State for the data analysis agent.
    
    TODO: Add fields you need:
    - messages
    - is_data_query (bool to track if query is data-related)
    - iteration_count
    - summary (final formatted summary)
    """
    messages: Annotated[list, operator.add]
    # TODO: Add more fields here
    pass


# ============================================================================
# TODO: IMPLEMENT VALIDATION NODE
# ============================================================================

def validate_query(state: DataAgentState) -> DataAgentState:
    """Validate if the query is data-related.
    
    TODO: Implement logic to check if the query is about:
    - Calculations
    - Data analysis
    - Statistics
    - Numbers
    
    Set state["is_data_query"] = True/False
    """
    # YOUR CODE HERE
    pass


def should_process(state: DataAgentState) -> Literal["agent", "reject"]:
    """Route based on validation.
    
    TODO: Return "agent" if is_data_query is True, else "reject"
    """
    # YOUR CODE HERE
    pass


# ============================================================================
# TODO: IMPLEMENT AGENT NODE
# ============================================================================

def data_agent(state: DataAgentState) -> DataAgentState:
    """Agent specialized in data analysis.
    
    TODO: Implement the agent with tools
    - Use calculate and analyze_data tools
    - Add a system message that emphasizes data analysis
    """
    # YOUR CODE HERE
    pass


# ============================================================================
# TODO: IMPLEMENT SUMMARY NODE
# ============================================================================

def summarize_results(state: DataAgentState) -> DataAgentState:
    """Create a formatted summary of results.
    
    TODO: Extract the final answer and format it nicely
    - Include what tools were used
    - Highlight key numbers
    - Make it easy to read
    """
    # YOUR CODE HERE
    pass


# ============================================================================
# TODO: IMPLEMENT REJECT NODE
# ============================================================================

def reject_query(state: DataAgentState) -> DataAgentState:
    """Handle non-data-related queries.
    
    TODO: Return a polite message explaining this agent only handles data queries
    """
    # YOUR CODE HERE
    pass


# ============================================================================
# TODO: BUILD THE GRAPH
# ============================================================================

def create_data_agent_graph():
    """Build the specialized data agent graph.
    
    TODO: Implement the workflow:
    1. Start with validate_query
    2. Conditional edge: if valid -> agent, if not -> reject
    3. Agent can use tools (add tools node and conditional edge)
    4. After agent is done, go to summarize
    5. End after summarize or reject
    """
    workflow = StateGraph(DataAgentState)
    
    # TODO: Add all your nodes
    # workflow.add_node("validate", validate_query)
    # ... add more nodes
    
    # TODO: Set entry point
    # workflow.set_entry_point("validate")
    
    # TODO: Add edges
    # workflow.add_conditional_edges(...)
    
    # return workflow.compile()
    pass


# ============================================================================
# Test Your Agent
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 2: Build a Specialized Agent")
    print("=" * 60)
    
    # TODO: Uncomment and test when you've implemented the graph
    
    # graph = create_data_agent_graph()
    
    # Test 1: Valid data query
    # print("\n🧪 Test 1: Valid data query")
    # print("-" * 60)
    # result1 = graph.invoke({
    #     "messages": [HumanMessage(content="Calculate 156 * 89 and analyze the result")],
    #     "is_data_query": False,
    #     "iteration_count": 0,
    #     "summary": ""
    # })
    # print(f"Summary: {result1.get('summary', 'No summary')}")
    
    # Test 2: Invalid query
    # print("\n🧪 Test 2: Non-data query")
    # print("-" * 60)
    # result2 = graph.invoke({
    #     "messages": [HumanMessage(content="Tell me a joke")],
    #     "is_data_query": False,
    #     "iteration_count": 0,
    #     "summary": ""
    # })
    # print(f"Response: {result2['messages'][-1].content}")
    
    print("\n✅ Exercise template ready!")
    print("\nImplementation checklist:")
    print("- [ ] Define complete state with all fields")
    print("- [ ] Implement validate_query node")
    print("- [ ] Implement data_agent node with tools")
    print("- [ ] Implement summarize_results node")
    print("- [ ] Implement reject_query node")
    print("- [ ] Build the complete graph with all edges")
    print("- [ ] Test with both valid and invalid queries")
    print("\nSee exercises/solutions/ for the complete solution!")
