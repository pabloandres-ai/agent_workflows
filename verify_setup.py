#!/usr/bin/env python3
"""
Verification script for the workshop demo.
This checks that all components are properly set up.
"""

import sys
import importlib.util
from pathlib import Path

def check_file_exists(path: str) -> bool:
    """Check if a file exists."""
    return Path(path).exists()

def check_import(module_name: str) -> bool:
    """Check if a module can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False

def main():
    print("=" * 60)
    print("Workshop Demo Verification")
    print("=" * 60)
    
    checks = []
    
    # Check directory structure
    print("\n📁 Checking directory structure...")
    dirs = [
        "src",
        "src/tools",
        "src/agents",
        "src/workflows",
        "examples",
        "exercises",
        "exercises/solutions",
        "docs"
    ]
    
    for dir_path in dirs:
        exists = check_file_exists(dir_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_path}")
        checks.append(exists)
    
    # Check key files
    print("\n📄 Checking key files...")
    files = [
        "README.md",
        "requirements.txt",
        "setup.py",
        ".env.example",
        "src/__init__.py",
        "src/tools/__init__.py",
        "src/agents/__init__.py",
        "src/workflows/__init__.py",
        "examples/01_basic_agent.py",
        "examples/02_agent_with_tools.py",
        "examples/03_prefect_orchestration.py",
        "examples/04_batch_processing.py",
        "exercises/exercise_1_custom_tool.py",
        "exercises/exercise_2_new_agent.py",
        "docs/WORKSHOP_GUIDE.md",
        "docs/TROUBLESHOOTING.md"
    ]
    
    for file_path in files:
        exists = check_file_exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        checks.append(exists)
    
    # Check Python modules (if installed)
    print("\n🐍 Checking Python modules...")
    modules = [
        "langchain",
        "langgraph",
        "langchain_anthropic",
        "prefect"
    ]
    
    for module in modules:
        can_import = check_import(module)
        status = "✅" if can_import else "⚠️ "
        print(f"  {status} {module}")
        if not can_import:
            print(f"      → Run: pip install -r requirements.txt")
    
    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All structure checks passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up API key: cp .env.example .env")
        print("3. Run first example: python examples/01_basic_agent.py")
    else:
        print("❌ Some checks failed. Please review the output above.")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
