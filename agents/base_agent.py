from abc import ABC, abstractmethod
from typing import Dict, Any

class Agent(ABC):
    def __init__(self, name: str, llm_service=None):
        self.name = name
        self.llm_service = llm_service

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the context and return the updated context.
        """
        pass

    def log(self, message: str):
        print(f"[{self.name}] {message}")
        return f"[{self.name}] {message}"
