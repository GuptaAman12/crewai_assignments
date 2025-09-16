from typing import Dict, Any, Optional
from dotenv import load_dotenv
import os

from google.adk.agents import LlmAgent
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool

from google.adk.models.lite_llm import LiteLlm

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set.")

groq_model = LiteLlm(model="groq/gemma2-9b-it")

def symptom_lookup_tool(symptom_text: str, tool_context: ToolContext) -> Dict[str, Any]:
    text = symptom_text.lower().strip()
    condition = "Unknown"

    if "fever" in text and "sore throat" in text:
        condition = "Flu"
    elif "runny nose" in text and "sneezing" in text:
        condition = "Allergic rhinitis"
    elif "abdominal pain" in text and "diarrhea" in text:
        condition = "Gastroenteritis"

    tool_context.state["condition"] = condition
    tool_context.state["symptom_text"] = symptom_text

    print(f"Tool1: Detected condition '{condition}' from symptoms '{symptom_text}'")

    return {"status": "success", "condition": condition}


def medication_suggestion_tool(condition: str, tool_context: ToolContext) -> Dict[str, Any]:
    cond = (condition or "").lower()
    suggestions = []

    if "flu" in cond:
        suggestions = ["Rest", "Hydration (fluids)", "Paracetamol"]
    elif "allergic" in cond:
        suggestions = ["Antihistamines (cetirizine)", "Nasal saline rinse"]
    elif "gastroenteritis" in cond:
        suggestions = ["ORS (oral rehydration solution)", "Light meals (BRAT diet)"]
    else:
        suggestions = ["General rest", "Consult a doctor if symptoms persist"]

    print(f"Tool2: Suggested care for '{condition}' → {suggestions}")

    return {"status": "success", "suggestions": suggestions}


def after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    if tool.name == "symptom_lookup_tool":
        condition = tool_context.state.get("condition")
        if condition:
            print("Callback: Passing condition to Medication Suggestion Tool...")
            return medication_suggestion_tool(condition, tool_context)
    return None

my_agent = LlmAgent(
    name="symptom_checker_agent",
    instruction="""You are a helpful health assistant. 
    When user describes symptoms, call symptom_lookup_tool to detect condition. 
    Then (via callback) pass the detected condition into medication_suggestion_tool. 
    Finally summarize: Symptom → Condition → Care.""",
    model=groq_model,
    tools=[symptom_lookup_tool, medication_suggestion_tool],
    after_tool_callback=after_tool_callback
)

root_agent = my_agent
