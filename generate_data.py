import pandas as pd
import random

import pandas as pd
import random

def generate_data():
    # Real-world product catalog with Seasonality
    catalog = [
        {"Category": "Electronics", "Product": "Apple AirPods Pro", "Season": "All Year"},
        {"Category": "Electronics", "Product": "Sony WH-1000XM5 Headphones", "Season": "All Year"},
        {"Category": "Electronics", "Product": "Samsung 65-inch 4K TV", "Season": "Winter"}, # Super Bowl / Holiday
        {"Category": "Electronics", "Product": "Nintendo Switch OLED", "Season": "Winter"},
        {"Category": "Home", "Product": "Dyson V15 Detect Vacuum", "Season": "All Year"},
        {"Category": "Home", "Product": "Instant Pot Duo 7-in-1", "Season": "Winter"},
        {"Category": "Home", "Product": "Weber Spirit II Gas Grill", "Season": "Summer"},
        {"Category": "Clothing", "Product": "Nike Air Force 1 '07", "Season": "All Year"},
        {"Category": "Clothing", "Product": "North Face Nuptse Jacket", "Season": "Winter"},
        {"Category": "Clothing", "Product": "Adidas Ultraboost 22", "Season": "Summer"},
        {"Category": "Toys", "Product": "LEGO Star Wars Millennium Falcon", "Season": "Winter"},
        {"Category": "Toys", "Product": "Barbie Dreamhouse", "Season": "Winter"},
        {"Category": "Personal Care", "Product": "Colgate Total Toothpaste", "Season": "All Year"},
        {"Category": "Personal Care", "Product": "Dove Body Wash", "Season": "All Year"},
        {"Category": "Personal Care", "Product": "Philips Norelco Shaver", "Season": "Winter"}, # Gift item
        {"Category": "Sports", "Product": "Wilson NFL Football", "Season": "Winter"},
        {"Category": "Sports", "Product": "Spalding NBA Basketball", "Season": "Winter"},
        {"Category": "Sports", "Product": "Callaway Golf Set", "Season": "Summer"},
        {"Category": "Office", "Product": "Logitech MX Master 3S Mouse", "Season": "All Year"},
        {"Category": "Office", "Product": "Herman Miller Aeron Chair", "Season": "All Year"}
    ]
    
    locations = ["NJ", "CA", "TX", "NY", "FL"]
    
    data = []
    
    # Generate 100 SKUs (20 Products x 5 Locations)
    for item in catalog:
        product_base_name = item["Product"]
        category = item["Category"]
        season = item["Season"]
        
        for loc in locations:
            sku_id = f"P-{100 + len(data) + 1}"
            lead_time = random.randint(3, 30)
            
            # Randomize scenario per location
            scenario = random.choices(
                ["Normal", "Trending", "Stock-out", "Overstock"],
                weights=[0.6, 0.1, 0.1, 0.2]
            )[0]
            
            if scenario == "Normal":
                forecast = random.randint(50, 200)
                current_stock = int(forecast * random.uniform(0.8, 1.2))
                sales_trend = int(forecast * random.uniform(0.9, 1.1))
            elif scenario == "Trending":
                forecast = random.randint(50, 200)
                current_stock = int(forecast * random.uniform(0.5, 0.8))
                sales_trend = int(forecast * random.uniform(1.3, 2.0))
            elif scenario == "Stock-out":
                forecast = random.randint(50, 200)
                current_stock = int(forecast * random.uniform(0.0, 0.3))
                sales_trend = int(forecast * random.uniform(0.9, 1.1))
            elif scenario == "Overstock":
                forecast = random.randint(50, 200)
                current_stock = int(forecast * random.uniform(2.0, 3.0))
                sales_trend = int(forecast * random.uniform(0.7, 0.9))
                
            data.append({
                "SKU_ID": sku_id,
                "Product_Name": product_base_name,
                "Category": category,
                "Season": season, # New Column
                "Current_Stock": current_stock,
                "Forecast": forecast,
                "Sales_Trend_Last_30_Days": sales_trend,
                "Supplier_Lead_Time": lead_time,
                "Location": loc,
                "On_Order": 0
            })
        
    df = pd.DataFrame(data)
    df.to_csv("data/inventory_data_real.csv", index=False)
    print("Generated 100 SKUs (20 Real Products x 5 Locations) in data/inventory_data_real.csv")

if __name__ == "__main__":
    generate_data()
