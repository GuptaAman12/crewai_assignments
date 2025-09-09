# Assignment 1: Math Assistant Agent
# Demonstrates how to build an LlmAgent that routes math queries to a Calculator Tool.

import re
from dotenv import load_dotenv
import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set.")

groq_model = LiteLlm(model="groq/gemma2-9b-it")

def calculator_tool(expression: str) -> dict:
    """
    Evaluate a basic math expression (supports +, -, *, /).
    Args:
        expression (str): Math expression (e.g., "12 * 15").
    Returns:
        dict: {status: str, result or error_message}
    """
    try:
        if not re.match(r"^[0-9+\-*/().\s]+$", expression):
            return {"status": "error", "error_message": "Invalid characters in expression."}

        result = eval(expression, {"__builtins__": None}, {})
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

root_agent = LlmAgent(
    name="math_assistant_agent",
    model=groq_model,
    description="An agent that solves basic math problems using a Calculator Tool.",
    instruction=(
        "You are a helpful Math Assistant. "
        "If the user asks a math question, extract the expression and call calculator_tool. "
        "For non-math queries, politely say you can only help with math problems for now."
    ),
    tools=[calculator_tool],
)
