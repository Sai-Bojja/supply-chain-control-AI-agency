import os
import random
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self, provider="openai"):
        self.provider = provider
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generates a response from the LLM.
        If no API key is present, returns a simulated response based on keywords in the prompt.
        """
        if not self.api_key:
            return self._simulate_response(prompt)
            
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Fast and cost-effective
                messages=[
                    {"role": "system", "content": system_prompt or "You are a supply chain expert agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM Error: {e}. Falling back to simulation.")
            return self._simulate_response(prompt)

    def _simulate_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "root cause" in prompt_lower:
            reasons = [
                "Viral social media trend on TikTok driving unexpected demand.",
                "Competitor stock-out caused customers to switch to our product.",
                "Seasonal spike due to early holiday shopping.",
                "Supplier delay caused by raw material shortage."
            ]
            return random.choice(reasons)
        elif "recommendation" in prompt_lower or "inventory" in prompt_lower:
            return "Transfer 20 units from NJ warehouse to meet immediate demand. Increase safety stock by 10%."
        elif "procurement" in prompt_lower:
            return "Generate Purchase Order for 100 units. Expedite shipping if possible."
        elif "communication" in prompt_lower:
            return "Alert: Stock-out risk detected for this SKU. Root cause identified as viral demand. Action taken: Transfer initiated and PO generated."
        
        return "Analysis complete. Proceeding to next step."
