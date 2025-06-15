from typing import Dict, Any
import json
from openai import OpenAI
from ..schemas.prompt import PromptParseResult

class PromptParsingAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        
    def parse_prompt(self, prompt: str) -> PromptParseResult:
        """Parse a natural language prompt into structured furniture requirements."""
        
        # Define the function schema for GPT-3.5
        function_schema = {
            "name": "parse_furniture_prompt",
            "description": "Parse a natural language furniture description into structured data",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The main category of furniture (e.g., 'sofa', 'chair', 'table')"
                    },
                    "dimensions": {
                        "type": "object",
                        "properties": {
                            "width": {"type": "number", "description": "Width in inches"},
                            "height": {"type": "number", "description": "Height in inches"},
                            "depth": {"type": "number", "description": "Depth in inches"}
                        }
                    },
                    "material": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of materials mentioned"
                    },
                    "style_keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of style-related keywords"
                    },
                    "hard_requirements": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of non-negotiable requirements"
                    }
                },
                "required": ["category"]
            }
        }

        # Call GPT-3.5 with function calling
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a furniture expert that parses natural language descriptions into structured data."},
                {"role": "user", "content": prompt}
            ],
            functions=[function_schema],
            function_call={"name": "parse_furniture_prompt"}
        )

        # Extract the function call result
        function_call = response.choices[0].message.function_call
        if not function_call:
            raise ValueError("Failed to parse prompt")

        # Parse the result into our schema
        result = json.loads(function_call.arguments)
        return PromptParseResult(**result) 