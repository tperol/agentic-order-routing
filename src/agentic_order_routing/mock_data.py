"""Mock data stores for the Agentic AI Order Routing POC.

These dictionaries simulate databases and external services for demonstration.
"""

# 1. Mock Customer Relationship Management (CRM) Database
# Stores basic customer data, including their shipping ZIP code and customer tier.
MOCK_CRM_DB = {
    "cust123": {"name": "Alice Wonderland", "zip_code": "10001", "tier": "gold"},
    "cust456": {"name": "Bob The Builder", "zip_code": "90210", "tier": "silver"},
    "cust789": {"name": "Charlie Brown", "zip_code": "60606", "tier": "bronze"},
    "cust101": {"name": "Diana Prince", "zip_code": "30303", "tier": "gold"}, # Atlanta
    "cust112": {"name": "Edward Scissorhands", "zip_code": "90210", "tier": "bronze"}, # West Coast
}

# 2. Mock Inventory Database
# Stores product stock levels at different fulfillment locations (warehouses, stores).
# Format: { "location_id": {"product_id": quantity, ...}, ... }
INVENTORY_DB = {
    "WH_EAST": {"product_A": 10, "product_B": 5, "product_C": 0, "product_D": 20},
    "WH_WEST": {"product_A": 7, "product_B": 12, "product_C": 8, "product_D": 15},
    "STORE_CENTRAL": {"product_A": 3, "product_B": 2, "product_C": 1, "product_D": 5}, # Store acting as micro-fulfillment
    "WH_SOUTH": {"product_A": 15, "product_B": 10, "product_C": 10, "product_D": 10},
}

# 3. Mock Shipping Options Database
# Stores available shipping carriers, costs, ETAs, and CO2 factors per product,
# from a source location to a destination zone.
# Format: { "location_id": { "zone_id": [ (product_id, carrier, cost, days, co2_kg), ... ], ... }, ... }
SHIPPING_OPTIONS_DB = {
    "WH_EAST": {
        "ZONE_1": [ # East Coast Zone
            ("product_A", "CarrierX_Std", 10, 3, 0.5), ("product_A", "CarrierY_Exp", 15, 1, 0.8),
            ("product_B", "CarrierX_Std", 8, 3, 0.4), ("product_B", "CarrierY_Exp", 12, 1, 0.6),
            ("product_D", "CarrierX_Std", 12, 3, 0.6), ("product_D", "CarrierY_Exp", 18, 1, 0.9),
        ],
        "ZONE_2": [ # West Coast Zone (from East WH)
            ("product_A", "CarrierX_Std", 25, 5, 1.2),
            ("product_B", "CarrierX_Std", 20, 5, 1.0),
            ("product_D", "CarrierX_Std", 30, 5, 1.5),
        ],
        "ZONE_3": [ # South Zone (from East WH)
            ("product_A", "CarrierX_Std", 12, 2, 0.6), ("product_A", "CarrierY_Exp", 18, 1, 0.9),
            ("product_B", "CarrierX_Std", 10, 2, 0.5),
            ("product_D", "CarrierX_Std", 15, 2, 0.7),
        ]
    },
    "WH_WEST": {
        "ZONE_1": [ # East Coast Zone (from West WH)
            ("product_A", "CarrierZ_Std", 22, 5, 1.1),
            ("product_B", "CarrierZ_Std", 18, 5, 0.9),
            ("product_D", "CarrierZ_Std", 28, 5, 1.4),
        ],
        "ZONE_2": [ # West Coast Zone
            ("product_A", "CarrierZ_Std", 9, 3, 0.4), ("product_A", "CarrierW_Exp", 14, 1, 0.6),
            ("product_B", "CarrierZ_Std", 7, 3, 0.3), ("product_B", "CarrierW_Exp", 11, 1, 0.5),
            ("product_D", "CarrierZ_Std", 11, 3, 0.5), ("product_D", "CarrierW_Exp", 16, 1, 0.7),
        ],
        "ZONE_3": [ # South Zone (from West WH)
            ("product_A", "CarrierZ_Std", 18, 4, 0.9),
            ("product_B", "CarrierZ_Std", 15, 4, 0.7),
            ("product_D", "CarrierZ_Std", 22, 4, 1.1),
        ]
    },
    "STORE_CENTRAL": { # Limited, often more expensive/slower options for store fulfillment
        "ZONE_1": [
            ("product_A", "LocalCourier_Std", 20, 2, 0.2), ("product_A", "LocalCourier_Exp", 25, 1, 0.3),
            ("product_D", "LocalCourier_Std", 22, 2, 0.25),
        ],
        "ZONE_2": [
            ("product_A", "LocalCourier_Std", 20, 2, 0.2), ("product_A", "LocalCourier_Exp", 25, 1, 0.3),
        ],
        "ZONE_3": [
             ("product_A", "LocalCourier_Std", 15, 1, 0.15), # Store might be close to a part of ZONE_3
        ]
    },
    "WH_SOUTH": {
        "ZONE_1": [ # East Coast Zone (from South WH)
            ("product_A", "CarrierS_Std", 14, 3, 0.7), ("product_A", "CarrierS_Exp", 20, 2, 1.0),
            ("product_B", "CarrierS_Std", 12, 3, 0.6),
            ("product_D", "CarrierS_Std", 18, 3, 0.8),
        ],
        "ZONE_2": [ # West Coast Zone (from South WH)
            ("product_A", "CarrierS_Std", 20, 4, 1.0),
            ("product_B", "CarrierS_Std", 17, 4, 0.8),
            ("product_D", "CarrierS_Std", 25, 4, 1.2),
        ],
        "ZONE_3": [ # South Zone
            ("product_A", "CarrierS_Std", 8, 2, 0.3), ("product_A", "CarrierS_Exp", 12, 1, 0.4),
            ("product_B", "CarrierS_Std", 6, 2, 0.2), ("product_B", "CarrierS_Exp", 10, 1, 0.3),
            ("product_D", "CarrierS_Std", 10, 2, 0.4), ("product_D", "CarrierS_Exp", 15, 1, 0.5),
        ]
    }
}

# 4. Mock ZIP Code to Shipping Zone Mapping
# Simplifies determining a customer's region for shipping calculations.
ZIP_TO_ZONE_DB = {
    "10001": "ZONE_1", # NYC (East Coast)
    "02101": "ZONE_1", # Boston (East Coast)
    "90210": "ZONE_2", # Beverly Hills (West Coast)
    "94101": "ZONE_2", # San Francisco (West Coast)
    "60606": "ZONE_1", # Chicago (Central, but often grouped with East for national models)
    "75201": "ZONE_3", # Dallas (South)
    "30303": "ZONE_3", # Atlanta (South)
    "UNKNOWN_ZIP_DEFAULT": "ZONE_1" # A default if a ZIP isn't specifically mapped
}

# 5. Mock Product Weight Database
# Stores product weights in kilograms (kg).
# This can be used for more detailed CO2 calculations if the shipping options
# provide CO2 per kg-mile or similar, though it's simplified in the current POC.
PRODUCT_WEIGHT_DB = {
    "product_A": 2.0,   # kg
    "product_B": 1.5,   # kg
    "product_C": 3.0,   # kg
    "product_D": 0.5    # kg (new light product)
}

if __name__ == "__main__":
    # This block allows you to quickly test if the data structures are accessible
    # by running `python mock_data.py` from your terminal.
    print("--- MOCK_CRM_DB ---")
    for cust_id, details in MOCK_CRM_DB.items():
        print(f"{cust_id}: {details}")
    
    print("\n--- INVENTORY_DB ---")
    for loc, stock in INVENTORY_DB.items():
        print(f"{loc}: {stock}")

    print("\n--- SHIPPING_OPTIONS_DB (Example: WH_EAST to ZONE_1) ---")
    if "WH_EAST" in SHIPPING_OPTIONS_DB and "ZONE_1" in SHIPPING_OPTIONS_DB["WH_EAST"]:
        for option in SHIPPING_OPTIONS_DB["WH_EAST"]["ZONE_1"]:
            print(option)
            
    print("\n--- ZIP_TO_ZONE_DB ---")
    for zip_code, zone in ZIP_TO_ZONE_DB.items():
        print(f"{zip_code} -> {zone}")

    print("\n--- PRODUCT_WEIGHT_DB ---")
    for product, weight in PRODUCT_WEIGHT_DB.items():
        print(f"{product}: {weight} kg")
