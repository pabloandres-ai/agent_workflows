"""
Agent Workflows - LangGraph + Prefect Demo Package

This package provides a modular implementation of AI agents using LangGraph
and orchestrated with Prefect, designed for workshop demonstrations.
"""

__version__ = "1.0.0"

from src.tools import web_search, calculate, analyze_sentiment
from src.agents import create_agent_graph
from src.workflows import agent_workflow, batch_agent_workflow

__all__ = [
    "web_search",
    "calculate",
    "analyze_sentiment",
    "create_agent_graph",
    "agent_workflow",
    "batch_agent_workflow",
]
