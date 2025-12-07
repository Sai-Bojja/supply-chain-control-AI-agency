from core.orchestrator import Orchestrator

def test_transfer():
    # Data matching the candidate found
    sku_data = {
        "SKU_ID": "P-101",
        "Product_Name": "Electronics Item 1", # Critical: Must match CSV
        "Current_Stock": 100,
        "Forecast": 165,
        "Sales_Trend_Last_30_Days": 180, # High trend to trigger risk
        "Supplier_Lead_Time": 14,
        "Location": "NJ",
        "On_Order": 0
    }
    
    orchestrator = Orchestrator()
    result = orchestrator.run(sku_data)
    
    print("\n--- Inventory Action ---")
    print(result.get("inventory_action"))

if __name__ == "__main__":
    test_transfer()
