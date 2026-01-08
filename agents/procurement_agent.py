from .base_agent import Agent
from .tools import create_po

def procurement_instructions(context_variables):
    return """You are a Procurement Agent.
Your job is to ensure long-term stock availability if transfers are not enough.

1. Check if the Inventory Agent successfully initiated a transfer.
2. If stock is still critically low or no transfer was possible, calculate the deficit.
3. Deficit = Forecast - (Current Stock + On Order).
4. If Deficit > 0, generate a Purchase Order (PO) for the deficit amount + 20% safety stock.
5. Use 'create_po' tool to place the order.
"""

procurement_agent = Agent(
    name="Procurement Agent",
    model="gpt-4o",
    instructions=procurement_instructions,
    tools=[create_po]
)
