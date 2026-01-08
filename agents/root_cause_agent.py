from .base_agent import Agent
from .tools import search_web, get_market_news

def root_cause_instructions(context_variables):
    product_name = context_variables.get("Product_Name", "Product")
    sku_id = context_variables.get("SKU_ID", "Unknown SKU")
    
    return f"""You are a Root Cause Analysis Agent. 
Your goal is to investigate supply chain issues for SKU {sku_id} ({product_name}).

1. Use the 'search_web' tool to find real-time news about supply chain disruptions, component shortages, or logistics issues related to this product or its category.
2. If no clear news is found, use 'get_market_news' to get market context.
3. Analyze the provided context (Sales Trend, Forecast, Seasonality) alongside the news.
4. Conclude with a specific, professional root cause for any risk status.

Context:
- Sales Trend: {context_variables.get('Sales_Trend_Last_30_Days')}
- Forecast: {context_variables.get('Forecast')}
- Season: {context_variables.get('Season')}
"""

root_cause_agent = Agent(
    name="Root Cause Agent",
    model="gpt-4o",
    instructions=root_cause_instructions,
    tools=[search_web, get_market_news]
)
