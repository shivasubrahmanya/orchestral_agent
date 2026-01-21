from agents.base import BaseAgent
from schemas import JudgeOutput

class JudgeAgent(BaseAgent):
    def run(self, test_output: str) -> JudgeOutput:
        system_prompt = (
            "You are a CI/CD Judge. Analyze the pytest output to determine if the tests PASSED or FAILED.\n"
            "Success = All tests passed, no errors.\n"
            "Output JSON with 'success' (bool) and 'reason' (string).\n"
            "Example:\n"
            "{\n"
            "  \"success\": true,\n"
            "  \"reason\": \"All 3 tests passed.\"\n"
            "}"
        )
        
        user_prompt = f"Pytest Output:\n{test_output}"
        
        response = self.llm.call_expecting_json(system_prompt, user_prompt)
        return JudgeOutput(**response)
