from setuptools import setup, find_packages

setup(
    name="agent_workflows",
    version="1.0.0",
    description="LangGraph + Prefect Agent Workflow Demo for Workshops",
    author="Workshop Instructor",
    packages=find_packages(),
    install_requires=[
        "langchain>=0.1.0",
        "langgraph>=0.0.40",
        "langchain-google-genai>=0.0.1",
        "langchain-core>=0.1.0",
        "prefect>=2.14.0",
        "httpx>=0.25.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
