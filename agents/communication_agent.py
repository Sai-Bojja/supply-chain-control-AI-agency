from typing import Dict, Any
from .base_agent import Agent

class CommunicationAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        logs = []
        sku_id = context["sku_data"]["SKU_ID"]
        
        if context.get("status") == "Risk":
            summary = (
                f"**Alert for SKU {sku_id}**\n"
                f"- **Issue**: {context.get('risk_type')}\n"
                f"- **Root Cause**: {context.get('root_cause')}\n"
                f"- **Inventory Action**: {context.get('inventory_action')}\n"
                f"- **Procurement Action**: {context.get('procurement_action')}"
            )
        else:
            summary = f"SKU {sku_id} is healthy. No actions required."
            
        context["final_summary"] = summary
        logs.append(self.log("Final report generated."))
        
        context["logs"].extend(logs)
        return context
