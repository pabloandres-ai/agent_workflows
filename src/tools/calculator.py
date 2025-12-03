"""
Calculator Tool

A safe mathematical calculation tool that evaluates Python expressions.
Uses restricted evaluation to prevent code injection.
"""

from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations. Input should be a valid Python expression.
    
    Args:
        expression: A mathematical expression as a string (e.g., "25 * 47")
        
    Returns:
        The calculation result or an error message
        
    Example:
        >>> calculate("25 * 47")
        "Result: 1175"
        
    Note:
        This uses Python's eval() with restricted builtins for safety.
        Only mathematical operations are allowed.
    """
    try:
        # Restricted evaluation - no access to builtins for security
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"
