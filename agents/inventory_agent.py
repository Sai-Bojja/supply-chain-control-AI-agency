from typing import Dict, Any
from .base_agent import Agent

class InventoryAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.get("status") != "Risk":
            return context
            
        logs = []
        
        # Real Inventory Optimization
        product_name = context["sku_data"]["Product_Name"]
        current_loc = context["sku_data"]["Location"]
        full_inv = context.get("full_inventory", [])
        
        logs.append(self.log(f"Checking network inventory for '{product_name}'..."))
        
        transfer_option = None
        for item in full_inv:
            # Find same product in different location
            if item["Product_Name"] == product_name and item["Location"] != current_loc:
                # Check for surplus (Stock > Forecast)
                surplus = int(item["Current_Stock"]) - int(item["Forecast"])
                if surplus > 10: # Minimum transfer quantity
                    transfer_option = item
                    break
        
        if transfer_option:
            qty_to_transfer = min(50, int(transfer_option["Current_Stock"]) - int(transfer_option["Forecast"]))
            recommendation = f"Transfer {qty_to_transfer} units from {transfer_option['Location']} (Surplus: {int(transfer_option['Current_Stock']) - int(transfer_option['Forecast'])}). Avoids PO."
        else:
            recommendation = "No surplus inventory found in network. Procurement required."
            
        context["inventory_action"] = recommendation
        logs.append(self.log(f"Inventory Action Proposed: {recommendation}"))
        
        context["logs"].extend(logs)
        return context
