from typing import Dict, Any
from .base_agent import Agent

class ForecastAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.get("status") != "Risk":
            return context
            
        sku_data = context.get("sku_data")
        logs = []
        
        sales_trend = int(sku_data["Sales_Trend_Last_30_Days"])
        current_forecast = int(sku_data["Forecast"])
        
        logs.append(self.log(f"Analyzing demand trends. Sales Trend (30d): {sales_trend} vs Forecast: {current_forecast}"))
        
        # Enhanced Prompt with Seasonality
        season = context.get("sku_data", {}).get("Season", "All Year")
        current_date = context.get("current_date", "Unknown")
        current_season = context.get("current_season", "Unknown")
        
        prompt = (
            f"Forecast demand for {sku_data['SKU_ID']} ({sku_data['Product_Name']}). "
            f"Current Stock: {sku_data['Current_Stock']}, Sales Trend (Past 30 Days): {sku_data['Sales_Trend_Last_30_Days']}. "
            f"Current Forecast: {current_forecast}. "
            f"Product Seasonality: {season}. Current Date: {current_date} ({current_season}). "
            "Task: Update the forecast based on the Sales Trend and Seasonality.\n"
            "Rules:\n"
            "1. If Sales Trend is significantly LOWER than Forecast, DECREASE the forecast (unless it's the start of peak season).\n"
            "2. If Sales Trend is HIGHER, INCREASE the forecast.\n"
            "3. Do not increase forecast just because of seasonality if the recent sales trend is poor.\n"
            "Return ONLY the new forecast number as an integer."
        )
        
        # Use LLM for reasoning
        try:
            new_forecast_str = self.llm_service.generate_response(prompt)
            # Extract number from response
            import re
            numbers = re.findall(r'\d+', new_forecast_str)
            if numbers:
                new_forecast = int(numbers[0])
                # Sanity check
                if new_forecast < 0: new_forecast = current_forecast
            else:
                new_forecast = current_forecast
        except:
            new_forecast = current_forecast

        # Fallback logic if LLM fails or returns same
        if new_forecast == current_forecast:
             if sales_trend > current_forecast * 1.1:
                 new_forecast = int(sales_trend * 1.1)
             elif sales_trend < current_forecast * 0.9:
                 new_forecast = int(sales_trend * 1.05) # Decrease to match trend (with slight buffer)

        if new_forecast != current_forecast:
            context["new_forecast"] = new_forecast
            if new_forecast < current_forecast:
                 logs.append(self.log(f"📉 Decreasing forecast to {new_forecast} units (Trend: {sales_trend} < Forecast: {current_forecast})."))
            else:
                 logs.append(self.log(f"📈 Increasing forecast to {new_forecast} units (Trend: {sales_trend} > Forecast: {current_forecast})."))
        else:
            context["new_forecast"] = current_forecast
            logs.append(self.log("Forecast remains unchanged (Aligned with trend)."))
            
        context["logs"].extend(logs)
        return context
