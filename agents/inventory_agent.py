from .base_agent import Agent
from .tools import transfer_inventory

def inventory_instructions(context_variables):
    current_stock = context_variables.get("Current_Stock", 0)
    forecast = context_variables.get("Forecast", 0)
    full_inventory = context_variables.get("full_inventory", [])
    product_name = context_variables.get("Product_Name", "Product")
    
    return f"""You are an Inventory Agent.
Your goal is to resolve stock-out risks by checking if other locations have excess stock of the same product.

Context: 
- Product: {product_name}
- Current Stock: {current_stock}
- Forecast: {forecast}
- Full Inventory List: {str(full_inventory)[:1000]}... (truncated)

1. If the current stock is sufficient (e.g., > 50% of forecast), do nothing.
2. If there is a risk, check 'Full Inventory List' for other locations with high stock of '{product_name}'.
3. If a location has excess stock (e.g., more than double their own forecast or > 100 units surplus), recommend a transfer.
4. Use 'transfer_inventory' tool to initiate the transfer.
"""

inventory_agent = Agent(
    name="Inventory Agent",
    model="gpt-4o",
    instructions=inventory_instructions,
    tools=[transfer_inventory]
)
