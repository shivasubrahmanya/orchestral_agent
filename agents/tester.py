from agents.base import BaseAgent
from schemas import PlannerSpec, TesterOutput
import os

class TesterAgent(BaseAgent):
    def run(self, spec: PlannerSpec) -> TesterOutput:
        # We need to make sure the test imports the right file.
        # Implied assumption: The file will be in the same directory or accessible path.
        # We will assume the orchestrator places them in the same workspace.
        # The module name is the filename without .py
        module_name = spec.filename.replace(".py", "")
        
        system_prompt = (
            "You are a QA Engineer. Write a pytest compatible test file for the given specification.\n"
            "Your test MUST import the function from the specified module.\n"
            "The test should verify the correctness of the logic. Since the implementation might have a bug, successful detection of the bug means the test FAILS.\n"
            "Do NOT assume the code is buggy in your test logic; simply write a CORRECT test case that asserts true behavior.\n"
            "Output JSON with 'test_content'.\n"
            "Example:\n"
            "{\n"
            "  \"test_content\": \"import pytest\\n...\"\n"
            "}"
        )
        
        user_prompt = (
            f"Module to import: {module_name}\n"
            f"Function Name: {spec.function_name}\n"
            f"Expected Behavior: {spec.description}\n"
            f"Logic Steps: {json.dumps(spec.steps)}"
        )
        
        response = self.llm.call_expecting_json(system_prompt, user_prompt)
        return TesterOutput(**response)
import json
