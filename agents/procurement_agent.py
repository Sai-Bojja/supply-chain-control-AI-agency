from typing import Dict, Any
from .base_agent import Agent

class ProcurementAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.get("status") != "Risk":
            return context
            
        logs = []
        new_forecast = context.get("new_forecast", context["sku_data"]["Forecast"])
        current_stock = int(context["sku_data"]["Current_Stock"])
        lead_time = int(context["sku_data"]["Supplier_Lead_Time"])
        
        # Simple PO calculation
        # Needed = Forecast - (Current_Stock + On_Order)
        on_order = int(context["sku_data"].get("On_Order", 0))
        needed = new_forecast - (current_stock + on_order)
        
        if needed > 0:
            po_qty = needed + int(needed * 0.2) # Safety buffer
            action = f"Create PO for {po_qty} units. Lead time: {lead_time} days. (On Order: {on_order})"
        else:
            action = "No immediate procurement needed."
            
        context["procurement_action"] = action
        logs.append(self.log(f"Procurement Action: {action}"))
        
        context["logs"].extend(logs)
        return context
