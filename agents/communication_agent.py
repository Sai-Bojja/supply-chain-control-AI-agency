from .base_agent import Agent

def communication_instructions(context_variables):
    return """You are a Communication Agent.
Your job is to summarize the entire chain of actions taken by the other agents for the user.

1. Review the conversation history (which is implicit in your context).
2. Summarize:
   - The initial status (Healthy/Risk).
   - Any Root Cause identified.
   - Actions taken (Forecast updates, Transfers, POs).
3. Provide a 'Final Summary' paragraph that is business-friendly and reassuring.
"""

communication_agent = Agent(
    name="Communication Agent",
    model="gpt-4o",
    instructions=communication_instructions,
    tools=[]
)
