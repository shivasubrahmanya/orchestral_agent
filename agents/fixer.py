from agents.base import BaseAgent
from schemas import PlannerSpec, FixerOutput
import json

class FixerAgent(BaseAgent):
    def run(self, spec: PlannerSpec, current_code: str, test_output: str) -> FixerOutput:
        system_prompt = (
            "You are a Senior Python Developer. Your task is to FIX a bug in the provided code.\n"
            "You have the original specification, the current buggy code, and the test failure output.\n"
            "YOU MUST NOT CHANGE the function signature (name, arguments) or the file name.\n"
            "Analyze the test failure to understand the logic error.\n"
            "Output JSON with 'file_content' containing the FIXED python code.\n"
            "Example:\n"
            "{\n"
            "  \"file_content\": \"def foo():\\n    # fixed logic...\"\n"
            "}"
        )
        
        user_prompt = (
            f"Spec: {spec.description}\n"
            f"Function: {spec.function_name}\n"
            f"Logic: {json.dumps(spec.steps)}\n\n"
            f"Current Code:\n```python\n{current_code}\n```\n\n"
            f"Test Output:\n{test_output}"
        )
        
        response = self.llm.call_expecting_json(system_prompt, user_prompt)
        return FixerOutput(**response)
