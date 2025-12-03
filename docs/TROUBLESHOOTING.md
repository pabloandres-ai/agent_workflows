# Troubleshooting Guide

Common issues and solutions for the Agent Workflows workshop.

## Installation Issues

### "Module not found" errors

**Problem**: Import errors when running examples
```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Install the package in editable mode
```bash
pip install -e .
```

Or run from the project root:
```bash
cd /path/to/agent_workflows
python examples/01_basic_agent.py
```

---

### Dependency conflicts

**Problem**: Version conflicts during installation

**Solution**: Use a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## API Key Issues

### "API key not found"

**Problem**: 
```
Error: ANTHROPIC_API_KEY not set
```

**Solution**: Set the environment variable
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your key
```

---

### "Invalid API key"

**Problem**: Authentication error

**Solutions**:
1. Check your key at https://console.anthropic.com/
2. Make sure there are no extra spaces
3. Verify the key is active and has credits

---

## Runtime Errors

### "Tool execution failed"

**Problem**: Tool returns an error

**Debug steps**:
1. Test the tool directly:
   ```python
   from src.tools import calculate
   print(calculate("2 + 2"))
   ```

2. Check the tool's docstring - the LLM uses this
3. Add error handling to your tool

---

### "Max iterations reached"

**Problem**: Agent hits iteration limit

**Explanation**: This is a safety feature to prevent infinite loops

**Solutions**:
1. Increase the limit in `should_continue`:
   ```python
   if state.get("iteration_count", 0) >= 10:  # Increased from 5
       return "end"
   ```

2. Simplify the query
3. Check if tools are working correctly

---

### "Graph execution failed"

**Problem**: LangGraph raises an error

**Debug steps**:
1. Check your state definition matches node returns
2. Verify all edges are properly defined
3. Ensure entry point is set
4. Add logging to see where it fails:
   ```python
   def my_node(state):
       print(f"Node state: {state}")
       # ... rest of code
   ```

---

## Prefect Issues

### "Prefect server not found"

**Problem**: Can't connect to Prefect UI

**Solution**: Start the Prefect server
```bash
prefect server start
```

Then access at http://localhost:4200

---

### "Flow not appearing in UI"

**Problem**: Flow runs but doesn't show in Prefect UI

**Solution**: Make sure you're running with Prefect:
```python
# This will show in UI
from prefect import flow

@flow
def my_flow():
    pass

if __name__ == "__main__":
    my_flow()  # Run it!
```

---

### "Task retry not working"

**Problem**: Task doesn't retry on failure

**Check**:
1. Is `retries` set in the decorator?
   ```python
   @task(retries=2)
   def my_task():
       pass
   ```

2. Is the error retriable? Some errors won't retry
3. Check Prefect logs for retry attempts

---

## Performance Issues

### "Agent is too slow"

**Causes**:
- Large context (many messages)
- Complex tools
- Network latency

**Solutions**:
1. Limit message history:
   ```python
   # Only keep last 10 messages
   state["messages"] = state["messages"][-10:]
   ```

2. Use faster model (if available)
3. Optimize tool execution
4. Cache tool results

---

### "High API costs"

**Solutions**:
1. Use simulated tools for development
2. Limit iterations
3. Cache responses
4. Use smaller/cheaper models for testing

---

## Exercise-Specific Issues

### Exercise 1: Custom Tool

**"Tool not being called"**

Check:
1. Tool has a clear docstring
2. Tool is in the tools list:
   ```python
   tools = [get_weather]  # Your tool here
   ```
3. Query actually needs the tool

---

### Exercise 2: Specialized Agent

**"Routing not working"**

Check:
1. Conditional edge is properly defined
2. Routing function returns correct values
3. All routes have corresponding nodes

---

## Environment Issues

### Python version

**Minimum**: Python 3.9

**Check your version**:
```bash
python --version
```

**Upgrade if needed**:
```bash
# Using pyenv
pyenv install 3.11
pyenv local 3.11
```

---

### PATH issues

**Problem**: Commands not found

**Solution**: Ensure virtual environment is activated
```bash
which python  # Should point to venv
source venv/bin/activate
```

---

## Getting Help

If you're still stuck:

1. **Check the code comments**: Examples have detailed explanations
2. **Review solutions**: Look at `exercises/solutions/`
3. **Enable debug logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
4. **Simplify**: Start with the simplest example that works
5. **Ask for help**: Share the error message and what you've tried

---

## Common Gotchas

### State updates

**Wrong**:
```python
def my_node(state):
    state["messages"].append(new_message)  # Mutating state
    return state
```

**Right**:
```python
def my_node(state):
    return {"messages": [new_message]}  # Return updates
```

---

### Tool docstrings

**Wrong**:
```python
@tool
def my_tool(x):
    return x  # No docstring!
```

**Right**:
```python
@tool
def my_tool(x: str) -> str:
    """Clear description of what this tool does."""
    return x
```

---

### Conditional edges

**Wrong**:
```python
def should_continue(state):
    return True  # Should return string!
```

**Right**:
```python
def should_continue(state) -> Literal["tools", "end"]:
    return "tools"  # Return route name
```

---

## Still Having Issues?

Create a minimal reproduction:

```python
# minimal_example.py
import os
from langchain_anthropic import ChatAnthropic

# Test basic LLM call
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

response = llm.invoke("Hello!")
print(response.content)
```

If this works, the issue is in your agent code.  
If this fails, it's an environment/API issue.
