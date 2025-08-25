from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class FileSaverInput(BaseModel):
    content: str = Field(..., description="the text or code content to save into a file.")
    filename: str = Field(..., description="the name of the file where the content should be saved.")

class FileSaverTool(BaseTool):
    name: str = "file_saver"
    description: str = "A tool that saves text or code into a file. Use this tool whenever you need to store code (solution.py) or feedback (review.txt)."
    args_schema: Type[BaseModel] = FileSaverInput

    def _run(self, filename: str, content: str) -> str:
        try:
            os.makedirs("outputs", exist_ok=True)
            filepath = os.path.join("outputs", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"saved to {filepath}"
        except Exception as e:
            return f"failed to save file {filename}: {str(e)}"