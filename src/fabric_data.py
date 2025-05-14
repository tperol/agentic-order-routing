import random

# Helper lists for generating varied data
PRODUCT_CATEGORIES = ["Bookcase", "Sideboard", "Shelf", "Coffee Table", "Sofa", "Office Chair", "Desk", "Floor Lamp", "Loveseat", "Dining Table", "Area Rug", "Accent Mirror", "Bed Frame", "Nightstand", "Dresser", "TV Stand", "Ottoman", "Bar Stool", "Patio Chair", "Planter"]
PRODUCT_MATERIALS = ["Oak", "Pine", "Walnut", "Metal", "Glass", "Linen", "Velvet", "Leather", "Mesh", "Plastic", "Ceramic", "Concrete"]
PRODUCT_COLORS = ["Grey", "Oak", "Brown", "White", "Black", "Red", "Blue", "Green", "Brass", "Gold", "Silver", "Natural", "Charcoal"]
PRODUCT_STYLES = ["Small", "Large", "Tall", "Minimalist", "Industrial", "Modern", "Classic", "Rustic", "Kids", "Outdoor"]

LOCATIONS = ["Warehouse East", "Warehouse West", "Showroom Central", "Warehouse North", "Warehouse South", "Retail Hub Metro", "Online Fulfillment Center"]
CHANNELS = ["Online Store", "Retail Outlet A", "Retail Outlet B", "Marketplace Hub", "Mobile App", "Partner Site"]
STATUSES = ["Available", "Low stock", "Backorder", "Preorder", "Discontinued"]

FABRIC_INVENTORY_DATA = [
    {
        "skuCode": "100084-000012-2",
        "productName": "3-Shelf Bookcase / Grey / Small",
        "location": "Warehouse East",
        "channel": "Online Store",
        "status": "Low stock",
        "availToPurchase": 130,
        "availToBackorder": 18,
        "availToPreorder": 15
    },
    {
        "skuCode": "150085-000019-9",
        "productName": "Oceanside Sideboard / Oak / Large",
        "location": "Warehouse West",
        "channel": "Retail Outlet A",
        "status": "Low stock",
        "availToPurchase": 540,
        "availToBackorder": 56,
        "availToPreorder": 54
    },
    {
        "skuCode": "540083-000017-7",
        "productName": "Stairway Ladder Shelf / Brown / Tall",
        "location": "Showroom Central",
        "channel": "Online Store",
        "status": "Available",
        "availToPurchase": 536,
        "availToBackorder": 82,
        "availToPreorder": 13
    },
    {
        "skuCode": "760083-000015-2",
        "productName": "Minimalist Coffee Table / Oak / Small",
        "location": "Warehouse East",
        "channel": "Retail Outlet B",
        "status": "Backorder",
        "availToPurchase": 274, # Still available for purchase despite backorder status
        "availToBackorder": 15,
        "availToPreorder": 12
    },
    {
        "skuCode": "420081-000015-2",
        "productName": "Oceanside Sectional Sofa / White Linen",
        "location": "Warehouse West",
        "channel": "Online Store",
        "status": "Preorder",
        "availToPurchase": 0, # Not available for immediate purchase
        "availToBackorder": 0,
        "availToPreorder": 135,
        "eta": "2025-08-15"
    },
    {
        "skuCode": "B001-CHAIR-RED",
        "productName": "Ergonomic Office Chair / Red Mesh",
        "location": "Showroom Central",
        "channel": "Retail Outlet A",
        "status": "Available",
        "availToPurchase": 75,
        "availToBackorder": 5,
        "availToPreorder": 0
    },
    {
        "skuCode": "D003-DESK-BLK",
        "productName": "Standing Desk Converter / Black",
        "location": "Warehouse East",
        "channel": "Online Store",
        "status": "Available",
        "availToPurchase": 210,
        "availToBackorder": 20,
        "availToPreorder": 5
    },
    {
        "skuCode": "L005-LAMP-BRS",
        "productName": "Industrial Floor Lamp / Brass Finish",
        "location": "Warehouse West",
        "channel": "Retail Outlet B",
        "status": "Low stock",
        "availToPurchase": 45,
        "availToBackorder": 10,
        "availToPreorder": 0
    },
    {
        "skuCode": "S007-SOFA-GRN",
        "productName": "Velvet Loveseat / Emerald Green",
        "location": "Showroom Central",
        "channel": "Online Store",
        "status": "Backorder",
        "availToPurchase": 30,
        "availToBackorder": 50,
        "availToPreorder": 25,
        "eta": "2025-07-28"
    },
    {
        "skuCode": "T009-TABLE-WHT",
        "productName": "Dining Table Extendable / White Gloss",
        "location": "Warehouse East",
        "channel": "Retail Outlet A",
        "status": "Preorder",
        "availToPurchase": 0,
        "availToBackorder": 0,
        "availToPreorder": 90 
    },
    {
        "skuCode": "R011-RUG-BLU",
        "productName": "Abstract Area Rug / Blue & Grey / 8x10",
        "location": "Warehouse West",
        "channel": "Online Store",
        "status": "Available",
        "availToPurchase": 150,
        "availToBackorder": 0,
        "availToPreorder": 0
    },
    {
        "skuCode": "M013-MIRROR-GLD",
        "productName": "Round Accent Mirror / Gold Frame",
        "location": "Showroom Central",
        "channel": "Retail Outlet B",
        "status": "Available",
        "availToPurchase": 60,
        "availToBackorder": 5,
        "availToPreorder": 10
    }
]

# Generate additional items to reach at least 100 total
num_existing_items = len(FABRIC_INVENTORY_DATA)
num_to_generate = 100 - num_existing_items

for i in range(num_to_generate):
    cat = random.choice(PRODUCT_CATEGORIES)
    mat = random.choice(PRODUCT_MATERIALS)
    col = random.choice(PRODUCT_COLORS)
    sty = random.choice(PRODUCT_STYLES)
    
    product_name = f"{cat} / {mat} / {col} / {sty}"
    # Simplified SKU generation for uniqueness in this mock set
    sku_code = f"GEN{i+1:03d}-{cat[:3].upper()}-{random.randint(1000,9999)}"
    
    location = random.choice(LOCATIONS)
    channel = random.choice(CHANNELS)
    status = random.choice(STATUSES)
    
    avail_purchase = random.randint(0, 500) if status != "Preorder" else 0
    avail_backorder = random.randint(0, 100) if status in ["Low stock", "Backorder", "Available"] else 0
    avail_preorder = random.randint(0, 200) if status in ["Preorder", "Backorder"] else 0
    
    if status == "Discontinued":
        avail_purchase = 0
        avail_backorder = 0
        avail_preorder = 0
        
    FABRIC_INVENTORY_DATA.append({
        "skuCode": sku_code,
        "productName": product_name,
        "location": location,
        "channel": channel,
        "status": status,
        "availToPurchase": avail_purchase,
        "availToBackorder": avail_backorder,
        "availToPreorder": avail_preorder
    })

# --- Data moved from mock_data.py and order_agent_tools.py ---

# 1. Mock Customer Relationship Management (CRM) Database (Revised with emails)
MOCK_CRM_DB = {
    "cust001": {"name": "Savannah Nguyen", "email": "savannah.n@example.com", "zip_code": "90210", "tier": "gold"},
    "cust002": {"name": "Wade Warren", "email": "wade.warren@example.net", "zip_code": "10001", "tier": "silver"},
    "cust003": {"name": "Arlene McCoy", "email": "arlene.m@example.org", "zip_code": "60606", "tier": "bronze"},
    "cust004": {"name": "Floyd Miles", "email": "floyd.m@example.com", "zip_code": "75201", "tier": "gold"},
    "cust005": {"name": "Darrell Steward", "email": "darrell.s@example.net", "zip_code": "30303", "tier": "silver"},
    "cust006": {"name": "Eleanor Pena", "email": "eleanor.p@example.com", "zip_code": "94107", "tier": "gold"},
    "cust007": {"name": "Cameron Williamson", "email": "cameron.w@example.org", "zip_code": "02110", "tier": "bronze"},
    "cust008": {"name": "Brooklyn Simmons", "email": "brooklyn.s@example.com", "zip_code": "33101", "tier": "silver"},
    "cust009": {"name": "Esther Howard", "email": "esther.h@example.net", "zip_code": "77002", "tier": "gold"},
    "cust010": {"name": "Jacob Jones", "email": "jacob.j@example.org", "zip_code": "80202", "tier": "standard"},
    "cust123": {"name": "Alice Wonderland", "email": "alice.w@example.com", "zip_code": "10001", "tier": "gold"},
    "cust456": {"name": "Bob The Builder", "email": "bob.b@example.net", "zip_code": "90210", "tier": "silver"},
    "cust789": {"name": "Charlie Brown", "email": "charlie.b@example.org", "zip_code": "60606", "tier": "bronze"},
    "cust101": {"name": "Diana Prince", "email": "diana.p@example.com", "zip_code": "30303", "tier": "gold"},
    "cust112": {"name": "Edward Scissorhands", "email": "edward.s@example.net", "zip_code": "90210", "tier": "bronze"}
}

# 2. Original Mock Inventory Database (for existing Order Routing workflow if needed)
INVENTORY_DB = {
    "WH_EAST": {"product_A": 10, "product_B": 5, "product_C": 0, "product_D": 20},
    "WH_WEST": {"product_A": 7, "product_B": 12, "product_C": 8, "product_D": 15},
    "STORE_CENTRAL": {"product_A": 3, "product_B": 2, "product_C": 1, "product_D": 5},
    "WH_SOUTH": {"product_A": 15, "product_B": 10, "product_C": 10, "product_D": 10}
}

# 3. Mock Shipping Options Database
SHIPPING_OPTIONS_DB = {
    "WH_EAST": {
        "ZONE_1": [ 
            ("product_A", "CarrierX_Std", 10, 3, 0.5), ("product_A", "CarrierY_Exp", 15, 1, 0.8),
            ("product_B", "CarrierX_Std", 8, 3, 0.4), ("product_B", "CarrierY_Exp", 12, 1, 0.6),
            ("product_D", "CarrierX_Std", 12, 3, 0.6), ("product_D", "CarrierY_Exp", 18, 1, 0.9)
        ],
        "ZONE_2": [ 
            ("product_A", "CarrierX_Std", 25, 5, 1.2),
            ("product_B", "CarrierX_Std", 20, 5, 1.0),
            ("product_D", "CarrierX_Std", 30, 5, 1.5)
        ],
        "ZONE_3": [ 
            ("product_A", "CarrierX_Std", 12, 2, 0.6), ("product_A", "CarrierY_Exp", 18, 1, 0.9),
            ("product_B", "CarrierX_Std", 10, 2, 0.5),
            ("product_D", "CarrierX_Std", 15, 2, 0.7)
        ]
    },
    "WH_WEST": {
        "ZONE_1": [ 
            ("product_A", "CarrierZ_Std", 22, 5, 1.1),
            ("product_B", "CarrierZ_Std", 18, 5, 0.9),
            ("product_D", "CarrierZ_Std", 28, 5, 1.4)
        ],
        "ZONE_2": [ 
            ("product_A", "CarrierZ_Std", 9, 3, 0.4), ("product_A", "CarrierW_Exp", 14, 1, 0.6),
            ("product_B", "CarrierZ_Std", 7, 3, 0.3), ("product_B", "CarrierW_Exp", 11, 1, 0.5),
            ("product_D", "CarrierZ_Std", 11, 3, 0.5), ("product_D", "CarrierW_Exp", 16, 1, 0.7)
        ],
        "ZONE_3": [ 
            ("product_A", "CarrierZ_Std", 18, 4, 0.9),
            ("product_B", "CarrierZ_Std", 15, 4, 0.7),
            ("product_D", "CarrierZ_Std", 22, 4, 1.1)
        ]
    },
    "STORE_CENTRAL": {
        "ZONE_1": [
            ("product_A", "LocalCourier_Std", 20, 2, 0.2), ("product_A", "LocalCourier_Exp", 25, 1, 0.3),
            ("product_D", "LocalCourier_Std", 22, 2, 0.25)
        ],
        "ZONE_2": [
            ("product_A", "LocalCourier_Std", 20, 2, 0.2), ("product_A", "LocalCourier_Exp", 25, 1, 0.3)
        ],
        "ZONE_3": [
             ("product_A", "LocalCourier_Std", 15, 1, 0.15)
        ]
    },
    "WH_SOUTH": {
        "ZONE_1": [ 
            ("product_A", "CarrierS_Std", 14, 3, 0.7), ("product_A", "CarrierS_Exp", 20, 2, 1.0),
            ("product_B", "CarrierS_Std", 12, 3, 0.6),
            ("product_D", "CarrierS_Std", 18, 3, 0.8)
        ],
        "ZONE_2": [ 
            ("product_A", "CarrierS_Std", 20, 4, 1.0),
            ("product_B", "CarrierS_Std", 17, 4, 0.8),
            ("product_D", "CarrierS_Std", 25, 4, 1.2)
        ],
        "ZONE_3": [ 
            ("product_A", "CarrierS_Std", 8, 2, 0.3), ("product_A", "CarrierS_Exp", 12, 1, 0.4),
            ("product_B", "CarrierS_Std", 6, 2, 0.2), ("product_B", "CarrierS_Exp", 10, 1, 0.3),
            ("product_D", "CarrierS_Std", 10, 2, 0.4), ("product_D", "CarrierS_Exp", 15, 1, 0.5)
        ]
    }
}

# 4. Mock ZIP Code to Shipping Zone Mapping
ZIP_TO_ZONE_DB = {
    "10001": "ZONE_1", "02101": "ZONE_1", "90210": "ZONE_2", "94101": "ZONE_2",
    "60606": "ZONE_1", "75201": "ZONE_3", "30303": "ZONE_3",
    "UNKNOWN_ZIP_DEFAULT": "ZONE_1"
}

# 5. Mock Product Weight Database
PRODUCT_WEIGHT_DB = {
    "product_A": 2.0, "product_B": 1.5, "product_C": 3.0, "product_D": 0.5
}

# 6. Mock Orders Database (Expanded for Detail View & Main Table - Corrected Order IDs)
FABRIC_ORDERS_DATA = {
    "6110822858950": { 
        "orderId": "6110822858950",
        "displayOrderId": "#6110822858950", 
        "status": "Ready for processing",
        "paymentStatus": "Paid",
        "orderType": "WEB",
        "dateCreated": "Mar 13, 2025, 1:22 PM",
        "internalOrderId": "67d314438fc5cd1f8f8c58f3",
        "customerName": "Michelle M",
        "customerEmail": "michelle.m@example.com",
        "customerId": "cust001",
        "orderSummary": {
            "subtotal": "150.00",
            "discount": "0.00",
            "shipping": "0.00",
            "fees": "0.00",
            "adjustments": "0.00",
            "taxes": "12.00",
            "total": "162.00",
            "currency": "USD"
        },
        "shippingGroups": [
            {
                "groupTitle": "Shipment Group 1",
                "type": "Delivery",
                "deliveryAddress": "123 Main St, Anytown, USA 90210",
                "lineItems": [
                    {
                        "sku": "product_A",
                        "productName": "Standard Product A",
                        "imageUrl": "https://via.placeholder.com/60x80/cccccc/000000?text=ProdA",
                        "quantity": 1,
                        "itemTotal": "150.00",
                        "currency": "USD",
                        "statusProgress": ["Created"] 
                    }
                ]
            }
        ]
    },
    "7201122334455": {
        "orderId": "7201122334455",
        "displayOrderId": "#7201122334455",
        "customerName": "Alice Wonderland",
        "customerEmail": "alice.w@example.com",
        "status": "Shipped", 
        "paymentStatus": "Paid", 
        "orderType": "ONLINE",
        "dateCreated": "Jul 15, 2024, 10:30 AM",
        "internalOrderId": "aabbccddeeff001122334455",
        "trackingNumber": "TN123456789", 
        "estimatedDelivery": "2024-07-30",
        "orderSummary": { "subtotal": "250.00", "discount": "10.00", "shipping": "15.00", "fees": "0.00", "adjustments": "0.00", "taxes": "20.00", "total": "275.00", "currency": "USD" },
        "shippingGroups": [
            {
                "groupTitle": "Shipment 1",
                "type": "Delivery",
                "deliveryAddress": "123 Wonderland Ave, Fantasy, FL 33000",
                "lineItems": [
                    {
                        "sku": "product_A", "productName": "3-Shelf Bookcase / Grey / Small", 
                        "imageUrl": "https://via.placeholder.com/60x80/cccccc/000000?text=BookcaseA",
                        "quantity": 1, "itemTotal": "150.00", "currency": "USD",
                        "statusProgress": ["Created", "Allocated", "Shipped"]
                    },
                    {
                        "sku": "product_B", "productName": "Minimalist Coffee Table / Oak / Small", 
                        "imageUrl": "https://via.placeholder.com/60x80/deb887/000000?text=TableB",
                        "quantity": 1, "itemTotal": "100.00", "currency": "USD",
                        "statusProgress": ["Created", "Allocated", "Shipped"]
                    }
                ]
            }
        ]
    },
    "8302233445566": {
        "orderId": "8302233445566",
        "displayOrderId": "#8302233445566",
        "customerName": "Bob The Builder",
        "customerEmail": "bob.b@example.net", 
        "status": "Processing", 
        "paymentStatus": "Authorized",
        "orderType": "PHONE",
        "dateCreated": "Jul 20, 2024, 02:15 PM",
        "internalOrderId": "ffeeddccbbaa112233445566",
        "trackingNumber": None, 
        "estimatedDelivery": "2024-08-02",
        "orderSummary": { "subtotal": "75.00", "discount": "0.00", "shipping": "5.00", "fees": "1.00",  "adjustments": "0.00", "taxes": "6.00", "total": "87.00", "currency": "USD" },
        "shippingGroups": [
            {
                "groupTitle": "Shipment 1",
                "type": "Delivery",
                "deliveryAddress": "456 Construct Rd, Builderville, CA 90210",
                "lineItems": [
                    {
                        "sku": "product_D", "productName": "Standing Desk Converter / Black", 
                        "imageUrl": "https://via.placeholder.com/60x80/a9a9a9/000000?text=DeskD", 
                        "quantity": 1, "itemTotal": "75.00", "currency": "USD",
                        "statusProgress": ["Created"]
                    }
                ]
            }
        ]
    },
    "9403344556677": {
        "orderId": "9403344556677", 
        "displayOrderId": "#9403344556677", 
        "customerName": "Charlie Brown", 
        "customerEmail": "charlie.b@example.org", 
        "status": "Delivered", 
        "paymentStatus": "Paid", 
        "orderType": "STORE", 
        "dateCreated": "Jul 10, 2024, 09:00 AM", 
        "internalOrderId": "112233445566778899aabb", 
        "trackingNumber": "TN987654321", 
        "estimatedDelivery": "2024-07-25", 
        "orderSummary": {"subtotal": "50.00", "discount":"5.00", "shipping":"0.00", "fees":"0.00", "adjustments":"0.00", "taxes":"4.00", "total":"49.00", "currency":"USD"}, 
        "shippingGroups":[]
    },
    "1054455667788": {
        "orderId": "1054455667788", 
        "displayOrderId": "#1054455667788", 
        "customerName": "Diana Prince", 
        "customerEmail": "diana.p@example.com", 
        "status": "Pending Payment", 
        "paymentStatus": "Pending", 
        "orderType": "WEB", 
        "dateCreated": "Jul 22, 2024, 05:00 PM", 
        "internalOrderId": "ccddeeff11223344556677", 
        "trackingNumber": None, 
        "estimatedDelivery": "2024-08-05", 
        "orderSummary": {"subtotal": "120.00", "discount":"0.00", "shipping":"10.00", "fees":"0.00", "adjustments":"0.00", "taxes":"9.60", "total":"139.60", "currency":"USD"}, 
        "shippingGroups":[]
    }
} 