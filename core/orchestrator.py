from typing import Dict, Any, List
from agents.monitoring_agent import MonitoringAgent
from agents.forecast_agent import ForecastAgent
from agents.root_cause_agent import RootCauseAgent
from agents.inventory_agent import InventoryAgent
from agents.procurement_agent import ProcurementAgent
from agents.communication_agent import CommunicationAgent
from core.llm_service import LLMService
from core.state import AgentState

class Orchestrator:
    def __init__(self, data_file="data/inventory_data_real.csv"):
        self.data_file = data_file
        self.llm_service = LLMService()
        self.agents = [
            MonitoringAgent("Monitoring Agent", self.llm_service),
            ForecastAgent("Forecast Agent", self.llm_service),
            RootCauseAgent("Root Cause Agent", self.llm_service),
            InventoryAgent("Inventory Agent", self.llm_service),
            ProcurementAgent("Procurement Agent", self.llm_service),
            CommunicationAgent("Communication Agent", self.llm_service)
        ]

    def run(self, sku_data: Dict[str, Any]) -> Dict[str, Any]:
        # Initialize State
        state = AgentState.from_dict(sku_data)
        
        print(f"Starting analysis for SKU: {state.sku_id}")
        
        context = state.to_dict()
        
        # Inject Seasonality Context
        # Simulating "December 1st" to trigger holiday logic
        context["current_date"] = "2024-12-01"
        context["current_season"] = "Winter"
        
        # Load full inventory for cross-location analysis
        import pandas as pd
        try:
            full_df = pd.read_csv(self.data_file)
            context["full_inventory"] = full_df.to_dict(orient="records")
        except Exception as e:
            print(f"Warning: Could not load full inventory: {e}")
            context["full_inventory"] = []
        
        for agent in self.agents:
            print(f"Running {agent.name}...")
            context = agent.process(context)
            
        # --- PERSISTENCE LAYER ---
        # Update state from context
        if context.get("new_forecast") is not None:
            state.forecast = context["new_forecast"]
        
        # Parse PO quantity from string (Hack for demo)
        # "Create PO for 138 units..."
        proc_action = context.get("procurement_action") or ""
        if "Create PO" in proc_action:
            try:
                qty = int(proc_action.split("for")[1].split("units")[0].strip())
                state.on_order += qty
            except:
                pass
                
        # Parse Inventory Transfer
        inv_action = context.get("inventory_action") or ""
        transfer_qty = 0
        source_loc = None
        if "Transfer" in inv_action:
             # Format: "Transfer 50 units from FL..."
             try:
                 parts = inv_action.split()
                 transfer_qty = int(parts[1])
                 source_loc = parts[4]
                 # Update state in memory
                 state.current_stock += transfer_qty
             except:
                 pass

        # Write back to CSV with Retry Logic
        import pandas as pd
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                df = pd.read_csv(self.data_file)
                
                # Update Current SKU (Forecast & On Order)
                df.loc[df["SKU_ID"] == state.sku_id, "Forecast"] = state.forecast
                df.loc[df["SKU_ID"] == state.sku_id, "On_Order"] = state.on_order
                
                # Execute Transfer (if any)
                if transfer_qty > 0 and source_loc:
                    # Add to Destination (Current SKU)
                    df.loc[df["SKU_ID"] == state.sku_id, "Current_Stock"] = state.current_stock
                    
                    # Deduct from Source Location
                    product_name = context["sku_data"]["Product_Name"]
                    # Find the row for the same product in the source location
                    source_mask = (df["Product_Name"] == product_name) & (df["Location"] == source_loc)
                    if not df[source_mask].empty:
                        current_source_stock = df.loc[source_mask, "Current_Stock"].values[0]
                        df.loc[source_mask, "Current_Stock"] = current_source_stock - transfer_qty
                        print(f"Executed Transfer: Moved {transfer_qty} units from {source_loc} to {state.sku_id}")

                df.to_csv(self.data_file, index=False)
                print(f"Persisted changes for {state.sku_id}")
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    print(f"File locked, retrying in 1s... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(1)
                else:
                    print(f"Failed to persist data after {max_retries} attempts: File locked.")
            except Exception as e:
                print(f"Failed to persist data: {e}")
                break
            
        return context
