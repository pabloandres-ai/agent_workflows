# Agent Workflows: LangGraph + Prefect Workshop

A hands-on workshop demonstrating how to build AI agents with **LangGraph** and orchestrate them with **Prefect**.

## 🎯 What You'll Learn

- **LangGraph Fundamentals**: Build stateful AI agents with conditional routing
- **Tool Integration**: Give agents capabilities like web search and calculations
- **Prefect Orchestration**: Add retry logic, logging, and workflow management
- **Production Patterns**: Batch processing, error handling, and observability

## 🏗️ Project Structure

```
agent_workflows/
├── src/                    # Modular, reusable components
│   ├── tools/             # Agent tools (web search, calculator, etc.)
│   ├── agents/            # Agent implementations
│   └── workflows/         # Prefect flows and tasks
├── examples/              # Progressive learning examples
│   ├── 01_basic_agent.py
│   ├── 02_agent_with_tools.py
│   ├── 03_prefect_orchestration.py
│   └── 04_batch_processing.py
├── exercises/             # Hands-on exercises
│   ├── exercise_1_custom_tool.py
│   ├── exercise_2_new_agent.py
│   └── solutions/
└── docs/                  # Additional documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google API key ([get one here](https://aistudio.google.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent_workflows
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Verify Setup**
   ```bash
   python verify_setup.py
   ```

5. **Install the package (optional, for easier imports)**
   ```bash
   pip install -e .
   ```

### Run Your First Example

```bash
python examples/01_basic_agent.py
```

## 📚 Learning Path

### Level 1: Basic Agent
**File**: `examples/01_basic_agent.py`

Learn the fundamentals of LangGraph:
- State management
- Agent nodes
- Message flow

```bash
python examples/01_basic_agent.py
```

### Level 2: Agent with Tools
**File**: `examples/02_agent_with_tools.py`

Add tool-calling capabilities:
- Tool binding
- Conditional routing
- Agent-tool loop

```bash
python examples/02_agent_with_tools.py
```

### Level 3: Prefect Orchestration
**File**: `examples/03_prefect_orchestration.py`

Add production-grade orchestration:
- Prefect tasks and flows
- Retry logic
- Logging and observability

```bash
python examples/03_prefect_orchestration.py
```

### Level 4: Batch Processing
**File**: `examples/04_batch_processing.py`

Handle multiple queries:
- Flow composition
- Result aggregation
- Parallel execution patterns

```bash
python examples/04_batch_processing.py
```

## 🎓 Exercises

### Exercise 1: Create a Custom Tool
**Difficulty**: ⭐ Beginner

Create a weather tool and integrate it with the agent.

```bash
python exercises/exercise_1_custom_tool.py
```

### Exercise 2: Build a Specialized Agent
**Difficulty**: ⭐⭐ Intermediate

Build a data analysis agent with custom routing logic.

```bash
python exercises/exercise_2_new_agent.py
```

**Solutions** are available in `exercises/solutions/`

## 🔧 Using the Modular Components

The `src/` directory contains reusable components:

```python
# Import tools
from src.tools import web_search, calculate, analyze_sentiment

# Import agent builder
from src.agents import create_agent_graph

# Import workflows
from src.workflows import agent_workflow, batch_agent_workflow

# Use in your code
agent = create_agent_graph()
result = agent_workflow("Your query here")
```

## 📖 Architecture Overview

### LangGraph Agent Flow

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Agent    │ ◄──┐
│   (LLM)     │    │
└──────┬──────┘    │
       │           │
       ▼           │
   Need tools?     │
       │           │
   ┌───┴───┐       │
   │  Yes  │       │
   └───┬───┘       │
       │           │
       ▼           │
┌─────────────┐    │
│    Tools    │────┘
└─────────────┘
       │
   ┌───┴───┐
   │  No   │
   └───┬───┘
       │
       ▼
┌─────────────┐
│  Finalize   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     End     │
└─────────────┘
```

### Prefect Orchestration

```
Flow: agent_workflow
├── Task: initialize_agent (retries=2)
├── Task: run_agent_query (retries=2)
└── Task: process_results
```

## 🛠️ Advanced Usage

### Running with Prefect UI

1. Start Prefect server:
   ```bash
   prefect server start
   ```

2. Run a flow:
   ```bash
   python examples/03_prefect_orchestration.py
   ```

3. View in UI: http://localhost:4200

### Creating Custom Tools

```python
from langchain_core.tools import tool

@tool
def my_custom_tool(input: str) -> str:
    """Description for the LLM."""
    # Your implementation
    return result
```

### Building Custom Agents

```python
from langgraph.graph import StateGraph, END
from src.agents import AgentState

def create_custom_agent():
    workflow = StateGraph(AgentState)
    workflow.add_node("my_node", my_node_function)
    workflow.set_entry_point("my_node")
    workflow.add_edge("my_node", END)
    return workflow.compile()
```

## 📚 Additional Resources

- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Prefect Documentation**: https://docs.prefect.io/
- **Google AI Studio**: https://aistudio.google.com/

## 🤝 Workshop Tips

### For Instructors

- Start with `examples/01_basic_agent.py` to explain core concepts
- Use `examples/02_agent_with_tools.py` to show tool integration
- Demonstrate Prefect benefits with `examples/03_prefect_orchestration.py`
- Show real-world patterns with `examples/04_batch_processing.py`
- Allocate time for exercises - they reinforce learning

### For Participants

- Follow the examples in order (01 → 04)
- Read the code comments carefully
- Try modifying examples before moving to exercises
- Don't skip the exercises - they solidify understanding
- Check solutions if stuck, but try first!

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -e .
```

### "API key not found"
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Or add to .env file
```

### Import errors
Make sure you're running from the project root:
```bash
cd agent_workflows
python examples/01_basic_agent.py
```

## 📝 License

MIT License - See LICENSE file for details

## 🙋 Questions?

- Check `docs/TROUBLESHOOTING.md`
- Review example code comments
- Look at exercise solutions

---

**Ready to build AI agents?** Start with `examples/01_basic_agent.py`! 🚀