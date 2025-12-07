from core.orchestrator import Orchestrator
import pandas as pd

def test_realism():
    # Load a real SKU from the new data
    try:
        df = pd.read_csv("data/inventory_data_real.csv")
    except FileNotFoundError:
        print("Error: data/inventory_data_real.csv not found. Run generate_data.py first.")
        return

    # Pick a Winter item to test seasonality (e.g., Nintendo Switch)
    winter_item = df[df["Product_Name"].str.contains("Nintendo")].iloc[0]
    
    print(f"\n=== TEST: Seasonality (Winter Item) ===")
    print(f"Product: {winter_item['Product_Name']}")
    print(f"Season: {winter_item['Season']}")
    print(f"Current Stock: {winter_item['Current_Stock']}")
    print(f"Forecast: {winter_item['Forecast']}")
    
    orchestrator = Orchestrator()
    result = orchestrator.run(winter_item.to_dict())
    
    print("\n--- Logs ---")
    for log in result["logs"]:
        print(log)

if __name__ == "__main__":
    test_realism()
