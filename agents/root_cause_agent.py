from typing import Dict, Any
from .base_agent import Agent
from duckduckgo_search import DDGS

class RootCauseAgent(Agent):
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if context.get("status") != "Risk":
            return context
            
        sku_data = context.get("sku_data")
        logs = []
        product_name = sku_data['Product_Name']
        
        logs.append(self.log(f"Initiating investigation for {product_name}..."))
        
        # Real-world search
        search_query = f"{product_name} supply chain issues news {sku_data.get('Location', '')}"
        logs.append(self.log(f"Searching web for: '{search_query}'"))
        
        search_results = []
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(search_query, max_results=3))
                for r in results:
                    snippet = f"- {r['title']}: {r['body']}"
                    search_results.append(snippet)
                    logs.append(self.log(f"🌍 Found live news: {r['title']}"))
        except Exception as e:
            logs.append(self.log(f"Search connection failed ({e}). Switching to simulation mode."))

        # Fallback if no results found (for demo stability)
        if not search_results:
            import random
            fallback_news = [
                f"Global shortage of components impacting {product_name} production.",
                f"Unexpected demand spike for {product_name} due to viral social media trend.",
                f"Logistics delays at {sku_data.get('Location', 'local')} port affecting deliveries.",
                f"Competitor recall driving customers to {product_name}."
            ]
            simulated_news = random.choice(fallback_news)
            search_results.append(f"- (Simulated Live Feed) {simulated_news}")
            logs.append(self.log(f"📰 [DEMO] Found news context: {simulated_news}"))
            
        search_context = "\n".join(search_results)
        
        season = context.get("sku_data", {}).get("Season", "All Year")
        current_date = context.get("current_date", "Unknown")
        
        prompt = (
            f"Analyze the root cause for SKU {sku_data['SKU_ID']} ({product_name}). "
            f"Sales Trend: {sku_data['Sales_Trend_Last_30_Days']}, Forecast: {sku_data['Forecast']}. "
            f"Product Seasonality: {season}. Current Date: {current_date}. "
            f"Recent News/Context:\n{search_context}\n"
            "Based on this, what is the likely root cause? Be specific and professional."
        )
        
        logs.append(self.log("Synthesizing findings with LLM..."))
        reason = self.llm_service.generate_response(prompt)
        
        context["root_cause"] = reason
        logs.append(self.log(f"Root Cause Identified: {reason}"))
        
        context["logs"].extend(logs)
        return context
