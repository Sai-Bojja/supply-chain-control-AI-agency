from typing import Dict, Any, List
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.base_agent import Agent
from agents.monitoring_agent import monitoring_agent
from agents.forecast_agent import forecast_agent
from agents.root_cause_agent import root_cause_agent
from agents.inventory_agent import inventory_agent
from agents.procurement_agent import procurement_agent
from agents.communication_agent import communication_agent
from core.state import AgentState

class Orchestrator:
    def __init__(self, data_file="data/inventory_data_real.csv"):
        self.data_file = data_file
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agents = [
            monitoring_agent,
            forecast_agent,
            root_cause_agent,
            inventory_agent,
            procurement_agent,
            communication_agent
        ]

    def run(self, sku_data: Dict[str, Any]) -> Dict[str, Any]:
        # Initialize Context/State
        state = AgentState.from_dict(sku_data)
        context_variables = sku_data.copy()
        
        # Add broader context
        context_variables["current_date"] = "2024-12-01"
        context_variables["current_season"] = "Winter"
        
        # Load full inventory for cross-location context
        import pandas as pd
        try:
            full_df = pd.read_csv(self.data_file)
            context_variables["full_inventory"] = full_df.to_dict(orient="records")
        except:
            context_variables["full_inventory"] = []

        print(f"Starting analysis for SKU: {state.sku_id}")
        
        messages = []
        logs = []
        
        # Starting with a system prompt to set the stage or just the first agent?
        # In this Agents SDK style, we often iterate through agents. 
        # Since we don't have the official 'handoff' function in standard API yet, 
        # we will simulate the handoff by running agents sequentially using the chat history.
        
        # Kickoff Message
        system_context = f"""
        Analyze the supply chain status for:
        Product: {sku_data['Product_Name']} (SKU: {sku_data['SKU_ID']})
        Stats: Stock={sku_data['Current_Stock']}, Forecast={sku_data['Forecast']}, On Order={sku_data['On_Order']}
        """
        
        messages.append({"role": "user", "content": system_context})
        
        final_context = context_variables.copy() # To return to UI
        
        
        # Helper to generate tool schemas
        def function_to_schema(func) -> Dict[str, Any]:
            # Simplified schema generator for demo
            # in a real app, use pydantic or similar introspection
            return {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": func.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            # Hardcoding props for known tools to save complex introspection code in this demo
                            "query": {"type": "string"},
                            "sku_id": {"type": "string"},
                            "new_forecast": {"type": "integer"},
                            "quantity": {"type": "integer"},
                            "source_location": {"type": "string"},
                            "product_name": {"type": "string"}
                        },
                        "required": ["query"] if func.__name__ == "search_web" else []
                    }
                }
            }

        for agent in self.agents:
            print(f"--- Handoff to {agent.name} ---")
            
            # 1. Prepare Instructions
            if callable(agent.instructions):
                instructions = agent.instructions(context_variables)
            else:
                instructions = agent.instructions
                
            # 2. Run Agent (Responses API / Chat Completions)
            current_messages = [{"role": "system", "content": instructions}] + messages
            
            try:
                # Generate schemas
                tool_schemas = [function_to_schema(t) for t in agent.tools] if agent.tools else None
                
                response = self.client.chat.completions.create(
                    model=agent.model,
                    messages=current_messages,
                    tools=tool_schemas,
                )
                
                msg = response.choices[0].message
                # Convert to dict for safety in message history if strictly using dicts, 
                # but SDK objects work if consistently used. Let's cast to dict to be safe with our manual appends.
                msg_dict = msg.model_dump() if hasattr(msg, "model_dump") else msg.dict()
                messages.append(msg_dict)
                
                content = msg.content or ""
                logs.append(f"[{agent.name}] {content[:100]}...")
                
                # Handle Tool Calls
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        func_name = tc.function.name
                        import json
                        args = json.loads(tc.function.arguments)
                        
                        # Find the tool function
                        tool_func = next((t for t in agent.tools if t.__name__ == func_name), None)
                        if tool_func:
                            try:
                                result = tool_func(**args)
                            except Exception as e:
                                result = str(e)
                            
                            # Add tool output to messages
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": str(result)
                            })
                            logs.append(f"[{agent.name}] Tool {func_name}: {result}")
                            
                            # Update local context if needed
                            if "Forecast updated" in str(result):
                                final_context["new_forecast"] = args.get("new_forecast")
                            if "Transfer" in str(result):
                                final_context["inventory_action"] = str(result)
                                final_context["transfer_qty"] = args.get("quantity")
                            if "PO created" in str(result):
                                final_context["procurement_action"] = str(result)
                                final_context["po_qty"] = args.get("quantity")
                                
                    # Follow-up call
                    followup = self.client.chat.completions.create(
                        model=agent.model,
                        messages=[{"role": "system", "content": instructions}] + messages
                    )
                    followup_msg = followup.choices[0].message
                    followup_dict = followup_msg.model_dump() if hasattr(followup_msg, "model_dump") else followup_msg.dict()
                    messages.append(followup_dict)
                    logs.append(f"[{agent.name}] {followup_msg.content}")

            except Exception as e:
                print(f"Error running {agent.name}: {e}")
                logs.append(f"[{agent.name}] Error: {e}")

        final_context["logs"] = logs
        
        last_msg = messages[-1].get("content", "")
        final_context["final_summary"] = last_msg
        
        return final_context

    def run_agent_ad_hoc(self, agent: Agent, context: Dict[str, Any]) -> str:
        """
        Run a single agent with a specific context. Useful for on-demand tasks like Email.
        """
        print(f"--- Ad-hoc Run: {agent.name} ---")
        
        # 1. Prepare Instructions
        if callable(agent.instructions):
            instructions = agent.instructions(context)
        else:
            instructions = agent.instructions
            
        # 2. Prepare Messages
        messages = [{"role": "system", "content": instructions}]
        
        # Helper for schemas (duplicated for now, could actulaly move to util)
        def function_to_schema(func) -> Dict[str, Any]:
            return {
                "type": "function",
                "function": {
                    "name": func.__name__,
                    "description": func.__doc__ or "",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to_email": {"type": "string"},
                            "subject": {"type": "string"},
                            "body": {"type": "string"},
                        },
                        "required": ["to_email", "subject", "body"] if func.__name__ == "send_email" else []
                    }
                }
            }

        try:
            tool_schemas = [function_to_schema(t) for t in agent.tools] if agent.tools else None
            
            response = self.client.chat.completions.create(
                model=agent.model,
                messages=messages,
                tools=tool_schemas,
            )
            
            msg = response.choices[0].message
            content = msg.content or ""
            
            # execute tools if any
            if msg.tool_calls:
                 for tc in msg.tool_calls:
                    func_name = tc.function.name
                    import json
                    args = json.loads(tc.function.arguments)
                    tool_func = next((t for t in agent.tools if t.__name__ == func_name), None)
                    if tool_func:
                        try:
                            result = tool_func(**args)
                        except Exception as e:
                            result = str(e)
                        return f"Action Taken: {result}"
            
            return content
            
        except Exception as e:
            return f"Error: {e}"

    def persist_changes(self, sku_id: str, changes: Dict[str, Any]) -> str:
        """
        Actually write changes to the CSV file after user approval.
        """
        import pandas as pd
        import pandas as pd
        # Don't print the whole dict, it contains full_inventory and logs!
        print(f"Persisting changes for {sku_id}...")
        
        try:
            df = pd.read_csv(self.data_file)
            mask = df["SKU_ID"] == sku_id
            
            if not mask.any():
                return "Error: SKU not found in database."
            
            updated = False
            
            # Apply Forecast Update
            if "new_forecast" in changes and changes["new_forecast"]:
                df.loc[mask, "Forecast"] = int(changes["new_forecast"])
                updated = True
                
            # Apply PO (Simple logic: increase On_Order)
            if "po_qty" in changes and changes["po_qty"]:
                current_on_order = df.loc[mask, "On_Order"].values[0]
                # Handle NaN
                if pd.isna(current_on_order): current_on_order = 0
                df.loc[mask, "On_Order"] = current_on_order + int(changes["po_qty"])
                updated = True
                
            # Apply Transfer (Increase Current Stock immediately for demo simplicity? Or On_Order?)
            # Let's say transfer assumes immediate arrival or In-Transit. 
            # We'll add to "On_Order" for consistency in this simple schema.
            if "transfer_qty" in changes and changes["transfer_qty"]:
                current_on_order = df.loc[mask, "On_Order"].values[0]
                if pd.isna(current_on_order): current_on_order = 0
                df.loc[mask, "On_Order"] = current_on_order + int(changes["transfer_qty"])
                updated = True

            if updated:
                df.to_csv(self.data_file, index=False)
                return "✅ Database successfully updated."
            else:
                return "No changes required."
                
        except Exception as e:
            return f"Database Error: {e}"
