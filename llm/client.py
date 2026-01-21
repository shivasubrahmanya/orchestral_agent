import os
import json
import time
from dotenv import load_dotenv

load_dotenv(override=True)

class LLMClient:
    def __init__(self):
        self.provider = "openai"
        self.client = None
        self.model = None
        
        # Check for Gemini Key first (since user asked for it)
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        if gemini_key:
            import google.generativeai as genai
            self.provider = "gemini"
            genai.configure(api_key=gemini_key)
            self.client = genai
            # Switching to stable flash model which usually has better quota availability
            self.model = "gemini-flash-latest" 
            print(f"DEBUG: Using Gemini API (Key: {gemini_key[:8]}...)")
            
        elif openai_key:
            from openai import OpenAI
            self.provider = "openai"
            masked_key = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "INVALID_LENGTH"
            print(f"DEBUG: Using OpenAI API (Key: {masked_key})")
            self.client = OpenAI(api_key=openai_key)
            self.model = "gpt-3.5-turbo"
            
        else:
            raise ValueError("No API Key found. Please set GEMINI_API_KEY or OPENAI_API_KEY in .env")

    def call(self, system_prompt: str, user_prompt: str, response_format=None) -> str:
        try:
            if self.provider == "gemini":
                model = self.client.GenerativeModel(self.model)
                # Combine system and user prompt for Gemini as it separates them differently or we can just prepend
                full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
                
                generation_config = {}
                if response_format and response_format.get("type") == "json_object":
                    generation_config["response_mime_type"] = "application/json"
                
                # Retry loop for rate limits
                retries = 3
                for attempt in range(retries):
                    try:
                        response = model.generate_content(
                            full_prompt,
                            generation_config=generation_config
                        )
                        
                        # Check safety/finish reason logic
                        if not response.parts:
                            print(f"DEBUG: Gemini Empty Response. Finish Reason: {response.candidates[0].finish_reason}")
                            print(f"Safety Ratings: {response.candidates[0].safety_ratings}")
                            # If blocked, maybe retry or raise specific error
                            raise ValueError("Gemini returned no content (likely safety filter or empty generation).")

                        return response.text
                    except Exception as e:
                        # Check for 429 or ResourceExhausted
                        if ("429" in str(e) or "ResourceExhausted" in str(e)) and attempt < retries - 1:
                            # Increase wait time to handle standard ~60s resets
                            wait_time = 30 * (attempt + 1) + 10 # 40s, 70s, 100s
                            print(f"DEBUG: Gemini Rate Limit hit. Waiting {wait_time}s before retry {attempt+1}/{retries}...")
                            time.sleep(wait_time)
                        else:
                            raise e
                
            else: # OpenAI
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format=response_format,
                    temperature=0.0
                )
                return completion.choices[0].message.content
                
        except Exception as e:
            if self.provider == "gemini" and "404" in str(e):
                print(f"DEBUG: Model {self.model} not found. Available models:")
                for m in self.client.list_models():
                    if "generateContent" in m.supported_generation_methods:
                        print(f" - {m.name}")
            raise RuntimeError(f"LLM call failed ({self.provider}): {e}")

    def call_expecting_json(self, system_prompt: str, user_prompt: str) -> dict:
        # Append instruction to ensure JSON
        system_prompt += "\n\nIMPORTANT: Output valid JSON only."
        
        content = self.call(system_prompt, user_prompt, response_format={"type": "json_object"})
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback for models that might return markdown fences
            clean_content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_content)

class MockLLMClient:
    def __init__(self):
        self.call_count = 0
        
    def call_expecting_json(self, system_prompt: str, user_prompt: str) -> dict:
        self.call_count += 1
        
        # PLANNER MOCK
        if "Senior Software Architect" in system_prompt:
            return {
                "filename": "math_ops.py",
                "function_name": "factorial",
                "description": "Calculate the factorial of a non-negative integer. Raises ValueError if n < 0.",
                "steps": [
                    "Check if n is less than 0, raise ValueError if so.",
                    "If n is 0, return 1.",
                    "Otherwise return n * factorial(n-1)."
                ]
            }
        
        # CODER MOCK (Buggy)
        if "Senior Python Developer" in system_prompt and "SUBTLE BUG" in system_prompt:
            return {
                "file_content": "def factorial(n):\n    if n < 0:\n        raise ValueError('n must be >= 0')\n    # BUG: Base case returns 0 instead of 1, causing all results to be 0\n    if n == 0:\n        return 0\n    return n * factorial(n - 1)"
            }
            
        # TESTER MOCK
        if "QA Engineer" in system_prompt:
            return {
                "test_content": "import pytest\nfrom math_ops import factorial\n\ndef test_factorial_success():\n    assert factorial(5) == 120\n    assert factorial(0) == 1\n\ndef test_factorial_error():\n    with pytest.raises(ValueError):\n        factorial(-1)"
            }
            
        # JUDGE MOCK
        if "CI/CD Judge" in system_prompt:
            if "failed" in user_prompt or "E " in user_prompt:
                return {"success": False, "reason": "Tests failed with errors."}
            else:
                return {"success": True, "reason": "All tests passed."}

        # FIXER MOCK
        if "FIX a bug" in system_prompt:
             return {
                "file_content": "def factorial(n):\n    if n < 0:\n        raise ValueError('n must be >= 0')\n    # FIXED: Base case returns 1\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)"
            }

        return {}
