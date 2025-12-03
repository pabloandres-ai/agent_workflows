# Workshop Guide: LangGraph + Prefect Agent Workflows

## Workshop Overview

**Duration**: 2-3 hours  
**Level**: Intermediate Python developers  
**Prerequisites**: Basic Python, familiarity with APIs

## Learning Objectives

By the end of this workshop, participants will be able to:
1. Build stateful AI agents using LangGraph
2. Integrate tools to extend agent capabilities
3. Orchestrate agent workflows with Prefect
4. Implement production-ready patterns

## Session Outline

### Part 1: Introduction (15 minutes)

**Topics**:
- What are AI agents?
- Why LangGraph + Prefect?
- Architecture overview

**Activities**:
- Show the final demo
- Explain the tech stack
- Review project structure

**Key Points**:
- Agents are LLMs that can use tools and make decisions
- LangGraph provides the agent framework
- Prefect adds orchestration and observability

---

### Part 2: Basic Agent (30 minutes)

**File**: `examples/01_basic_agent.py`

**Topics**:
- LangGraph state management
- Agent nodes and edges
- Message flow

**Teaching Points**:
1. **State is a TypedDict**: Explain how state flows through the graph
2. **Nodes are functions**: Each node takes state and returns updates
3. **Edges define flow**: Show how to connect nodes

**Live Coding**:
```python
# Show how to modify the agent's behavior
# Change the prompt, add logging, etc.
```

**Common Questions**:
- Q: "Why use a graph instead of a simple function?"
- A: Graphs allow complex routing, loops, and conditional logic

---

### Part 3: Tools and Routing (45 minutes)

**File**: `examples/02_agent_with_tools.py`

**Topics**:
- Tool binding
- Conditional edges
- Agent-tool loop

**Teaching Points**:
1. **Tools extend capabilities**: Show how tools give agents new abilities
2. **Conditional routing**: Explain `should_continue` logic
3. **The agent loop**: Walk through a complete execution

**Live Coding**:
```python
# Add a new tool
@tool
def get_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%H:%M:%S")

# Show how the agent automatically uses it
```

**Common Questions**:
- Q: "How does the LLM know when to use tools?"
- A: The tool docstring tells the LLM what the tool does

**Exercise Time** (15 minutes):
- Have participants work on Exercise 1
- Walk around and help
- Review solutions together

---

### Part 4: Prefect Orchestration (30 minutes)

**File**: `examples/03_prefect_orchestration.py`

**Topics**:
- Tasks vs Flows
- Retry logic
- Logging and observability

**Teaching Points**:
1. **Tasks are units of work**: Explain `@task` decorator
2. **Flows orchestrate tasks**: Explain `@flow` decorator
3. **Built-in features**: Show retries, logging, UI

**Live Demo**:
1. Start Prefect server: `prefect server start`
2. Run the example
3. Show the Prefect UI at localhost:4200
4. Point out task status, logs, retry attempts

**Common Questions**:
- Q: "When should I use Prefect vs just Python?"
- A: Prefect adds value for production: retries, monitoring, scheduling

---

### Part 5: Advanced Patterns (30 minutes)

**File**: `examples/04_batch_processing.py`

**Topics**:
- Flow composition
- Batch processing
- Result aggregation

**Teaching Points**:
1. **Flows can call flows**: Show composition pattern
2. **Batch processing**: Explain when and why
3. **Parallel execution**: Discuss task runners

**Live Coding**:
```python
# Show how to modify for parallel execution
# Discuss trade-offs
```

**Exercise Time** (15 minutes):
- Have participants work on Exercise 2
- This is more challenging - encourage collaboration
- Review key concepts from the solution

---

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

4. **Install the package (optional, for easier imports)**
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
- **Google AI Studio**: https://aistudio.google.com/)

### Example Projects
- LangGraph examples repo
- Prefect recipes
- This workshop repo

---

### Part 6: Wrap-up (15 minutes)

**Topics**:
- Review key concepts
- Production considerations
- Next steps

**Discussion Points**:
- What would you build with this?
- What challenges do you foresee?
- What additional features would you need?

**Resources**:
- Share documentation links
- Provide example repos
- Suggest next learning steps

---

## Facilitation Tips

### Before the Workshop

- [ ] Test all examples on a clean environment
- [ ] Prepare API keys for participants (or have them bring their own)
- [ ] Set up Prefect server in advance
- [ ] Have backup internet connection

### During the Workshop

- **Pace yourself**: Check in frequently - "Is everyone following?"
- **Use the REPL**: Show live Python interpreter for quick tests
- **Encourage questions**: "This is complex - what's unclear?"
- **Share your screen**: Make sure code is visible

### Common Issues

**Import errors**:
```bash
# Solution: Install in editable mode
pip install -e .
```

**API rate limits**:
- Use simulated tools for exercises
- Share API keys carefully

**Prefect server issues**:
- Have screenshots ready as backup
- Can run without UI if needed

---

## Extension Ideas

For workshops with extra time:

1. **Add a real API integration**
   - Integrate Tavily for real web search
   - Use OpenAI for comparison

2. **Deploy to production**
   - Show Prefect Cloud
   - Discuss deployment strategies

3. **Add persistence**
   - Save agent conversations
   - Implement memory

4. **Build a specific use case**
   - Customer support agent
   - Data analysis assistant
   - Research helper

---

## Assessment

### Knowledge Check Questions

1. What is the purpose of the `AgentState` TypedDict?
2. How does the agent decide whether to use a tool?
3. What's the difference between a Prefect task and flow?
4. When would you use conditional edges in LangGraph?

### Practical Assessment

Have participants build a simple agent that:
- Takes a user query
- Uses at least one custom tool
- Is wrapped in a Prefect flow
- Handles errors gracefully

---

## Feedback Collection

Ask participants:
1. What was the most valuable thing you learned?
2. What was most confusing?
3. What would you like to learn more about?
4. How would you rate the pace? (too slow / just right / too fast)

---

## Additional Resources

### Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Prefect Docs](https://docs.prefect.io/)
- [Anthropic Claude Docs](https://docs.anthropic.com/)

### Example Projects
- LangGraph examples repo
- Prefect recipes
- This workshop repo

### Community
- LangChain Discord
- Prefect Slack
- AI Engineering communities
