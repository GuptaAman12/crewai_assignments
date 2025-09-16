import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set in a .env file.")

groq_model = LiteLlm(model="groq/gemma2-9b-it")

QUESTION_BANK = {
    1: {
        "question": "What is the value of 5 + 7?",
        "answer": "12",
        "explanation": "This is a basic arithmetic addition."
    },
    2: {
        "question": "Who was the first President of India?",
        "answer": "Rajendra Prasad",
        "explanation": "Dr. Rajendra Prasad was the first President of India, in office from 1950 to 1962."
    },
    3: {
        "question": "What is the chemical symbol for water?",
        "answer": "H2O",
        "explanation": "Water is a molecule composed of two hydrogen (H) atoms and one oxygen (O) atom."
    }
}


def question_bank_tool(question_id: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Retrieves a specific question from the question bank using its ID.
    It also stores the question details in the context state for the AnswerCheckerTool.
    """
    print(f"Tool 1 (QuestionBank): Fetching question_id: {question_id}")
    question_data = QUESTION_BANK.get(question_id)

    if not question_data:
        return {"status": "error", "message": "Question not found."}

    tool_context.state["current_question_id"] = question_id
    tool_context.state["current_question_text"] = question_data["question"]
    tool_context.state["current_correct_answer"] = question_data["answer"]
    tool_context.state["current_explanation"] = question_data["explanation"]

    return {"status": "success", "question": question_data["question"]}


def answer_checker_tool(student_answer: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Checks if the student's answer is correct by comparing it to the answer
    stored in the context state.
    """
    print(f"Tool 2 (AnswerChecker): Validating answer: '{student_answer}'")
    correct_answer = tool_context.state.get("current_correct_answer")
    explanation = tool_context.state.get("current_explanation")

    if not correct_answer:
        return {"status": "error", "message": "No question was asked first."}

    is_correct = student_answer.strip().lower() == correct_answer.strip().lower()
    result = "Correct" if is_correct else "Incorrect"
    
    tool_context.state["student_answer"] = student_answer
    tool_context.state["result"] = result

    return {
        "status": "success",
        "result": result,
        "explanation": explanation
    }


def log_interaction_callback(tool: BaseTool, args: Dict, tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    """
    This callback function is triggered after a tool executes.
    It logs the interaction if the tool was the 'answer_checker_tool'.
    """
    if tool.name == "answer_checker_tool":
        print(">>> Callback (log_interaction_callback): Fired after AnswerCheckerTool.")
        
        quiz_log: List[Dict] = tool_context.state.setdefault("quiz_log", [])

        log_entry = {
            "question": tool_context.state.get("current_question_text"),
            "student_response": tool_context.state.get("student_answer"),
            "result": tool_context.state.get("result"),
            "explanation": tool_context.state.get("current_explanation")
        }
        
        quiz_log.append(log_entry)
        print(f">>> Callback: Interaction logged successfully. Total logs: {len(quiz_log)}")

    return None 


quiz_agent = LlmAgent(
    name="quiz_assistant_agent",
    instruction="""
    You are an AI Quiz Assistant. Your goal is to administer a 3-question quiz.
    1.  Start by calling `question_bank_tool` with `question_id` = 1.
    2.  Present the question to the student and wait for their answer.
    3.  When the student provides an answer, call `answer_checker_tool` with their response.
    4.  Briefly state if the answer was correct or incorrect, providing the explanation.
    5.  Repeat this process for `question_id` = 2, and then `question_id` = 3.
    6.  After the third question is answered, state that the quiz is complete.
    7.  Finally, present a summary of the entire quiz by formatting the `quiz_log` from the context.
        The summary format should be a list like:
        Q1: "[Question]" -> Student: "[Answer]" -> [Result] (Correct Answer: [Explanation])
    """,
    model=groq_model,
    tools=[question_bank_tool, answer_checker_tool],
    after_tool_callback=log_interaction_callback, 
)

root_agent = quiz_agent