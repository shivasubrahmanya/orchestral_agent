import json
from agents.base import BaseAgent
from schemas import PlannerSpec

class PlannerAgent(BaseAgent):
    def run(self, user_goal: str) -> PlannerSpec:
        system_prompt = (
            "You are a Senior Software Architect. Your job is to break down a user request into a precise "
            "single-file Python module specification.\n"
            "You must define:\n"
            "1. The filename (always end in .py)\n"
            "2. The main function name\n"
            "3. A description of what it does\n"
            "4. A list of step-by-step logic commands for the coder.\n\n"
            "Output MUST be a strict JSON object with these EXACT keys:\n"
            "{\n"
            "  \"filename\": \"example.py\",\n"
            "  \"function_name\": \"my_function\",\n"
            "  \"description\": \"Brief summary...\",\n"
            "  \"steps\": [\"Step 1\", \"Step 2\"]\n"
            "}"
        )
        
        user_prompt = f"Goal: {user_goal}"
        
        # We use the LLM to get the dict, then validate with Pydantic
        response_dict = self.llm.call_expecting_json(system_prompt, user_prompt)
        
        # Basic validation and type conversion
        return PlannerSpec(**response_dict)
