from core.orchestrator import Orchestrator

def test_orchestrator():
    print("\n=== TEST 1: RISK SCENARIO ===")
    sku_data_risk = {
        "SKU_ID": "P-101",
        "Product_Name": "Sony Headphones",
        "Current_Stock": 50,
        "Forecast": 100,
        "Sales_Trend_Last_30_Days": 150,
        "Supplier_Lead_Time": 14,
        "Location": "NJ"
    }
    
    orchestrator = Orchestrator()
    result = orchestrator.run(sku_data_risk)
    print(f"Status: {result.get('status')}")

    print("\n=== TEST 2: HEALTHY SCENARIO ===")
    sku_data_healthy = {
        "SKU_ID": "P-102",
        "Product_Name": "Samsung TV",
        "Current_Stock": 200,
        "Forecast": 100,
        "Sales_Trend_Last_30_Days": 100,
        "Supplier_Lead_Time": 14,
        "Location": "CA"
    }
    
    result = orchestrator.run(sku_data_healthy)
    print(f"Status: {result.get('status')}")

if __name__ == "__main__":
    test_orchestrator()
