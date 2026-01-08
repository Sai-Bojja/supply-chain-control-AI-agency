from typing import List, Callable, Optional, Union

class Agent:
    def __init__(self, 
                 name: str, 
                 model: str = "gpt-4o", 
                 instructions: Union[str, Callable[[], str]] = "You are a helpful agent.", 
                 tools: List[Callable] = None):
        self.name = name
        self.model = model
        self.instructions = instructions
        self.tools = tools or []
