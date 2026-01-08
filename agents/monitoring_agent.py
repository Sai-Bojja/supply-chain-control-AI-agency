from .base_agent import Agent

def monitoring_instructions(context_variables):
    return """You are a Monitoring Agent.
Your job is to analyze the inventory levels and forecast to detect risks.

Rules:
- Calculate Coverage = Current_Stock / Forecast (if Forecast > 0, else 0).
- If Coverage < 0.8, flag as "Stock-out Risk".
- If Coverage > 2.0, flag as "Overstock Risk".
- Otherwise, status is "Healthy".

Output a concise analysis of the health status.
"""

monitoring_agent = Agent(
    name="Monitoring Agent",
    model="gpt-4o",
    instructions=monitoring_instructions,
    tools=[]
)
