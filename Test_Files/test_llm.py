from core.llm_service import LLMService
import os

def test_llm():
    print(f"Checking API Key: {'Found' if os.environ.get('OPENAI_API_KEY') else 'Not Found'}")
    
    llm = LLMService()
    prompt = "Explain the concept of safety stock in one sentence."
    print(f"\nPrompt: {prompt}")
    
    response = llm.generate_response(prompt)
    print(f"\nResponse: {response}")
    
    if "safety stock" in response.lower() or "inventory" in response.lower():
        print("\n✅ LLM Service is working (Real or Simulated).")
    else:
        print("\n❌ Unexpected response.")

if __name__ == "__main__":
    test_llm()
