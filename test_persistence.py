from core.orchestrator import Orchestrator
import pandas as pd
import shutil
import os

def test_persistence():
    TEST_FILE = "data/test_inventory_persistence.csv"
    
    # 1. Setup: Create a test file from real data
    shutil.copy("data/inventory_data_real.csv", TEST_FILE)
    
    try:
        # 2. Load a target SKU
        df = pd.read_csv(TEST_FILE)
        target_sku = df.iloc[0]["SKU_ID"]
        initial_forecast = df.iloc[0]["Forecast"]
        initial_on_order = df.iloc[0]["On_Order"]
        
        print(f"Testing Persistence for SKU: {target_sku}")
        print(f"Initial State -> Forecast: {initial_forecast}, On Order: {initial_on_order}")
        
        # 3. Run Orchestrator with TEST FILE
        orchestrator = Orchestrator(data_file=TEST_FILE)
        sku_data = df.iloc[0].to_dict()
        
        # Force a scenario where Forecast SHOULD change (e.g. High Sales Trend)
        sku_data["Sales_Trend_Last_30_Days"] = int(initial_forecast * 1.5) # High trend
        sku_data["Current_Stock"] = 0 # Force Stock-out Risk so agents run
        
        result = orchestrator.run(sku_data)
        
        # 4. Verify File Change
        df_new = pd.read_csv(TEST_FILE)
        new_forecast = df_new[df_new["SKU_ID"] == target_sku].iloc[0]["Forecast"]
        new_on_order = df_new[df_new["SKU_ID"] == target_sku].iloc[0]["On_Order"]
        
        print(f"Final State -> Forecast: {new_forecast}, On Order: {new_on_order}")
        
        if new_forecast != initial_forecast:
            print("✅ Forecast updated in CSV.")
        else:
            print("❌ Forecast NOT updated in CSV.")
            
        if new_on_order != initial_on_order:
             print("✅ On Order updated in CSV.")
        else:
             print("⚠️ On Order not updated (might not have triggered PO).")

    finally:
        # Cleanup
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

if __name__ == "__main__":
    test_persistence()
