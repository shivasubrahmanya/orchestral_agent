from abc import ABC, abstractmethod
from llm.client import LLMClient

class BaseAgent(ABC):
    def __init__(self, use_mock: bool = False):
        if use_mock:
            from llm.client import MockLLMClient
            self.llm = MockLLMClient()
        else:
            self.llm = LLMClient()

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
