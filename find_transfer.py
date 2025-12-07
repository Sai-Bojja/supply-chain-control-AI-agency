import pandas as pd

def find_candidate():
    df = pd.read_csv("data/inventory_data_.csv")
    
    # Group by Product Name
    products = df["Product_Name"].unique()
    
    for prod in products:
        subset = df[df["Product_Name"] == prod]
        
        # Find a location with Stock < Forecast (Need)
        needs = subset[subset["Current_Stock"] < subset["Forecast"]]
        
        # Find a location with Stock > Forecast + 10 (Surplus)
        surpluses = subset[subset["Current_Stock"] > subset["Forecast"] + 10]
        
        if not needs.empty and not surpluses.empty:
            need_loc = needs.iloc[0]
            surplus_loc = surpluses.iloc[0]
            
            print(f"FOUND CANDIDATE: {prod}")
            print(f"Need at {need_loc['Location']} (SKU: {need_loc['SKU_ID']}): Stock={need_loc['Current_Stock']}, Forecast={need_loc['Forecast']}")
            print(f"Surplus at {surplus_loc['Location']} (SKU: {surplus_loc['SKU_ID']}): Stock={surplus_loc['Current_Stock']}, Forecast={surplus_loc['Forecast']}")
            return

    print("No suitable transfer candidate found.")

if __name__ == "__main__":
    find_candidate()
