from pydantic import BaseModel
from typing import List, Optional

class PlannerSpec(BaseModel):
    filename: str
    function_name: str
    description: str
    steps: List[str]

class CoderOutput(BaseModel):
    file_content: str

class TesterOutput(BaseModel):
    test_content: str

class FixerOutput(BaseModel):
    file_content: str

class JudgeOutput(BaseModel):
    success: bool
    reason: str
