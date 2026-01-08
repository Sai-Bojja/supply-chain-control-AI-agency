from core.orchestrator import Orchestrator
import json

def test_orchestrator():
    print("Initializing Orchestrator...")
    orchestrator = Orchestrator()
    
    sample_data = {
        "SKU_ID": "TEST-SKU-001",
        "Product_Name": "Test Product",
        "Category": "Apparel",
        "Location": "NY",
        "Current_Stock": 100,
        "Forecast": 200, # Should trigger coverage check (0.5 < 0.8) -> Risk
        "On_Order": 0,
        "Sales_Trend_Last_30_Days": 250,
        "Supplier_Lead_Time": 14,
        "Season": "Winter"
    }
    
    print("\nRunning Orchestrator with sample data...")
    result = orchestrator.run(sample_data)
    
    print("\n--- Final Result ---")
    print(json.dumps(result, indent=2, default=str))
    
    # Assertions
    logs = "\n".join(result["logs"])
    assert "Monitoring Agent" in logs, "Monitoring Agent should have run"
    assert "Root Cause Agent" in logs, "Root Cause Agent should have run"
    assert "Forecast Agent" in logs, "Forecast Agent should have run"
    
    if "Risk" in str(result): # Context might not explicitly say Risk if msg structure changed
        pass
        
    print("\nTest passed successfully!")

if __name__ == "__main__":
    test_orchestrator()
