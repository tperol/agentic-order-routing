# This file defines the Python functions that act as "tools" for the OrderRoutingDecisionAgent.
# These tools fetch data from the mock data stores, simulating API calls or queries
# to specialized services or other agents' knowledge bases.

import json
import logging
from agents import function_tool
from fabric_data import (
    INVENTORY_DB,
    SHIPPING_OPTIONS_DB,
    ZIP_TO_ZONE_DB,
    PRODUCT_WEIGHT_DB # Though not directly used in CO2 calc yet, it's available
)

logger = logging.getLogger("agent_workflow")

@function_tool
def get_customer_zone(customer_zip_code: str) -> str:
    """Determines the shipping zone for a given customer ZIP code."""
    logger.info(f"TOOL_CALL: get_customer_zone with zip: {customer_zip_code}")
    zone = ZIP_TO_ZONE_DB.get(customer_zip_code, ZIP_TO_ZONE_DB.get("UNKNOWN_ZIP_DEFAULT"))
    logger.info(f"TOOL_RESULT: Zone for {customer_zip_code} is {zone}")
    return json.dumps({"zip_code": customer_zip_code, "zone": zone})

@function_tool
def get_inventory(location_id: str = None, product_id: str = None) -> str:
    """Fetches inventory stock levels. Can be filtered by location_id and/or product_id."""
    logger.info(f"TOOL_CALL: get_inventory with location: {location_id}, product: {product_id}")
    # This tool should ideally use the more detailed FABRIC_INVENTORY_DATA and adapt its logic.
    # For now, it will use the simpler INVENTORY_DB for compatibility with original agent.
    if location_id and product_id:
        stock = INVENTORY_DB.get(location_id, {}).get(product_id)
        result = {location_id: {product_id: stock if stock is not None else "product_not_found_at_location"}}
    elif location_id:
        result = {location_id: INVENTORY_DB.get(location_id, "location_not_found")}
    elif product_id:
        result = {}
        for loc, stock_data in INVENTORY_DB.items():
            if product_id in stock_data:
                if loc not in result: result[loc] = {}
                result[loc][product_id] = stock_data[product_id]
        if not result:
            result = {"message": f"Product ID {product_id} not found at any location."}
    else:
        result = INVENTORY_DB # Full inventory if no filters
    logger.info(f"TOOL_RESULT: get_inventory returning: {json.dumps(result)}")
    return json.dumps(result)

@function_tool
def get_shipping_options(source_location_id: str, destination_zone_id: str, product_id: str) -> str:
    """Fetches available shipping options, costs, and ETAs for a product from a source to a destination zone."""
    logger.info(f"TOOL_CALL: get_shipping_options for {product_id} from {source_location_id} to {destination_zone_id}")
    options = SHIPPING_OPTIONS_DB.get(source_location_id, {}).get(destination_zone_id, [])
    product_specific_options = [opt for opt in options if opt[0] == product_id]
    if not product_specific_options:
        logger.warning(f"No shipping options found for {product_id} from {source_location_id} to {destination_zone_id}")
        # Return all options for the zone if product specific not found, agent can filter/decide
        # return json.dumps({"options": options, "message": f"No specific options for {product_id}, showing all for zone."})
        return json.dumps({"options": [], "message": f"No shipping options found for product {product_id} from {source_location_id} to {destination_zone_id}."})

    logger.info(f"TOOL_RESULT: get_shipping_options returning {len(product_specific_options)} options.")
    return json.dumps({"options": product_specific_options})

# --- Main block for testing the tools directly ---
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
    print("--- Testing routing_tools.py ---")

    # Test get_customer_zone
    print("\n[Test] get_customer_zone:")
    print(f"Zone for 10001: {get_customer_zone('10001')}")
    print(f"Zone for 90210: {get_customer_zone('90210')}")
    print(f"Zone for 99999 (unknown): {get_customer_zone('99999')}")

    # Test get_inventory
    print("\n[Test] get_inventory:")
    print(f"Inventory for product_A, 1 unit: {get_inventory('product_A', 1)}")
    print(f"Inventory for product_C, 5 units: {get_inventory('product_C', 5)}") # WH_WEST has 8, WH_SOUTH has 10
    print(f"Inventory for product_X (non-existent), 1 unit: {get_inventory('product_X', 1)}")

    # Test get_shipping_options
    print("\n[Test] get_shipping_options:")
    # Scenario 1: WH_EAST to ZONE_1 for product_A
    print(f"Shipping options from WH_EAST to ZONE_1 for product_A:\n{get_shipping_options('WH_EAST', 'ZONE_1', 'product_A')}")
    
    # Scenario 2: WH_WEST to ZONE_2 for product_B
    print(f"Shipping options from WH_WEST to ZONE_2 for product_B:\n{get_shipping_options('WH_WEST', 'ZONE_2', 'product_B')}")
    
    # Scenario 3: Non-existent warehouse
    print(f"Shipping options from WAREHOUSE_NULL to ZONE_1 for product_A:\n{get_shipping_options('WAREHOUSE_NULL', 'ZONE_1', 'product_A')}")

    # Scenario 4: Product with no specific options in a valid warehouse/zone
    # (Assuming product_C might not have explicit options from WH_EAST to ZONE_1 in SHIPPING_OPTIONS_DB)
    print(f"Shipping options from WH_EAST to ZONE_1 for product_C:\n{get_shipping_options('WH_EAST', 'ZONE_1', 'product_C')}")

    print("\n--- End of routing_tools.py tests ---") 