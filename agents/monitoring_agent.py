from typing import Dict, Any
from .base_agent import Agent

class MonitoringAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        sku_data = context.get("sku_data")
        logs = []
        
        current_stock = int(sku_data["Current_Stock"])
        forecast = int(sku_data["Forecast"])
        
        # Simple logic: Check for stockout risk (e.g., less than 50% of forecast coverage)
        coverage = current_stock / forecast if forecast > 0 else 0
        
        log_msg = f"Checking SKU {sku_data['SKU_ID']}: Stock={current_stock}, Forecast={forecast}, Coverage={coverage:.2f}"
        logs.append(self.log(log_msg))
        
        if coverage < 0.8: # Threshold for demo
            context["status"] = "Risk"
            context["risk_type"] = "Stock-out Risk"
            logs.append(self.log(f"ALERT: Stock-out risk detected for {sku_data['SKU_ID']}"))
        elif coverage > 2.0:
            context["status"] = "Risk"
            context["risk_type"] = "Overstock Risk"
            logs.append(self.log(f"ALERT: Overstock risk detected for {sku_data['SKU_ID']}"))
        else:
            context["status"] = "Healthy"
            logs.append(self.log(f"SKU {sku_data['SKU_ID']} is healthy."))
            
        context["logs"].extend(logs)
        return context
