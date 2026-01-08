from .base_agent import Agent
from .tools import update_forecast

def forecast_instructions(context_variables):
    return """You are a Forecast Agent.
Your goal is to predict future demand based on sales trends and seasonality.

1. Analyze the 'Sales_Trend_Last_30_Days' and 'Season'.
2. If the product is "In Season" (e.g., Winter for Coats), expect higher demand.
3. Compare the current 'Forecast' with recent sales.
4. If the Forecast seems too low (e.g., < Sales Trend), recommend an increase.
5. Use the 'update_forecast' tool to propose a new forecast number if needed.
"""

forecast_agent = Agent(
    name="Forecast Agent",
    model="gpt-4o",
    instructions=forecast_instructions,
    tools=[update_forecast]
)
