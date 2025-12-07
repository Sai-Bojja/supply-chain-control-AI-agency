from core.orchestrator import Orchestrator
import pandas as pd

def test_overstock_logic():
    # Create a mock Overstock scenario
    # Trend (50) is much lower than Forecast (100) -> Should DECREASE forecast
    sku_data = {
        "SKU_ID": "TEST-OVERSTOCK",
        "Product_Name": "Test Overstock Item",
        "Category": "Test",
        "Season": "All Year",
        "Current_Stock": 250, # Way overstocked (Coverage 2.5)
        "Forecast": 100,
        "Sales_Trend_Last_30_Days": 50, # Poor sales
        "Supplier_Lead_Time": 14,
        "Location": "NJ",
        "On_Order": 0
    }
    
    print("\n=== TEST: Overstock Forecast Logic ===")
    print(f"Forecast: {sku_data['Forecast']}")
    print(f"Sales Trend: {sku_data['Sales_Trend_Last_30_Days']}")
    print("EXPECTATION: Forecast should DECREASE.")
    
    orchestrator = Orchestrator()
    result = orchestrator.run(sku_data)
    
    print("\n--- Logs ---")
    for log in result["logs"]:
        if "Forecast" in log:
            print(log)

if __name__ == "__main__":
    test_overstock_logic()
