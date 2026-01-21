from agents.base import BaseAgent
from schemas import PlannerSpec, CoderOutput

class CoderAgent(BaseAgent):
    def run(self, spec: PlannerSpec) -> CoderOutput:
        system_prompt = (
            "You are a Senior Python Developer. Your task is to write a Python file based EXACTLY on the provided specification.\n"
            "HOWEVER, you must introduce a SUBTLE BUG in the logic. The bug should not be a syntax error, but a logic error "
            "(e.g., off-by-one, inverted condition, wrong variable usage).\n"
            "The code must otherwise be clean, runnable, and use the exact function name and inputs from the spec.\n"
            "Output JSON with a single key 'file_content' containing the Python code.\n"
            "Example:\n"
            "{\n"
            "  \"file_content\": \"def foo():\\n    pass\"\n"
            "}"
        )
        
        user_prompt = (
            f"Filename: {spec.filename}\n"
            f"Function Name: {spec.function_name}\n"
            f"Description: {spec.description}\n"
            f"Steps: {json.dumps(spec.steps)}"
        )
        
        response = self.llm.call_expecting_json(system_prompt, user_prompt)
        return CoderOutput(**response)

import json
