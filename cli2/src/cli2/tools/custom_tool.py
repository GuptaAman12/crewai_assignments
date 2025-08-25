from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class FileSaverInput(BaseModel):
    content: str = Field(..., description="The text content to save into a file.")
    filename: str = Field(..., description="The name of the file where the content should be saved.")

class FileSaverTool(BaseTool):
    name: str = "file_saver"
    description: str = "A tool that saves text content into a file. Use this to save the final trip plan."
    args_schema: Type[BaseModel] = FileSaverInput

    def _run(self, filename: str, content: str) -> str:
        try:
            os.makedirs("outputs", exist_ok=True)
            filepath = os.path.join("outputs", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully saved trip plan to {filepath}"
        except Exception as e:
            return f"Failed to save file {filename}: {str(e)}"