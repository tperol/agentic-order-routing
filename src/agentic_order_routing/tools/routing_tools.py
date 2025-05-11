# This file defines the Python functions that act as "tools" for the OrderRoutingDecisionAgent.
# These tools fetch data from the mock data stores, simulating API calls or queries
# to specialized services or other agents' knowledge bases.

import json
import logging
from agentic_order_routing.mock_data import (
    INVENTORY_DB,
    SHIPPING_OPTIONS_DB,
    ZIP_TO_ZONE_DB,
    PRODUCT_WEIGHT_DB # Though not directly used in CO2 calc yet, it's available
)
from agents import function_tool

logger = logging.getLogger("agent_workflow")

@function_tool
def get_customer_zone(zip_code: str) -> str:
    """
    Determines the shipping zone for a customer based on their zip code.
    This simulates a call to a Customer Zone Service or a geo-mapping utility.

    Args:
        zip_code: The customer's ZIP code.

    Returns:
        The shipping zone string (e.g., "ZONE_1") or "UNKNOWN_ZONE" if not found.
    """
    logger.info(f"TOOL_LOG: get_customer_zone called with zip_code='{zip_code}'")
    zone = ZIP_TO_ZONE_DB.get(zip_code, ZIP_TO_ZONE_DB.get("UNKNOWN_ZIP_DEFAULT", "UNKNOWN_ZONE"))
    logger.info(f"TOOL_LOG: get_customer_zone returning zone='{zone}'")
    return zone

@function_tool
def get_inventory(product_id: str, quantity: int) -> str:
    """
    Checks stock levels for a given product_id and quantity across ALL fulfillment locations.
    This simulates querying an Inventory Agent's knowledge base or an inventory management system.

    Args:
        product_id: The ID of the product to check.
        quantity: The desired quantity of the product.

    Returns:
        A JSON string representing a dictionary of locations that have sufficient stock,
        with location_id as key and available quantity as value.
        Example: '{"WH_EAST": 10, "STORE_CENTRAL": 3}'
    """
    logger.info(f"TOOL_LOG: get_inventory called with product_id='{product_id}', quantity={quantity}")
    available_locations = {}
    for location_id, products_at_location in INVENTORY_DB.items():
        stock_level = products_at_location.get(product_id, 0)
        if stock_level >= quantity:
            available_locations[location_id] = stock_level
    
    result_json = json.dumps(available_locations)
    logger.info(f"TOOL_LOG: get_inventory returning: {result_json}")
    return result_json

@function_tool
def get_shipping_options(warehouse_id: str, zone: str, product_id: str) -> str:
    """
    Fetches available shipping methods, costs, ETAs, and CO2 impact
    from a specific warehouse to a given customer zone for a particular product_id.
    This simulates querying a Logistics Agent or a shipping rate aggregator.

    Args:
        warehouse_id: The ID of the fulfillment warehouse/location.
        zone: The customer's shipping zone.
        product_id: The ID of the product being shipped.

    Returns:
        A JSON string representing a list of shipping option dictionaries.
        Each dictionary contains: "carrier", "cost", "days", "co2_kg".
        Example: '[{"carrier": "CarrierX_Std", "cost": 10, "days": 3, "co2_kg": 0.5}, ...]'
    """
    logger.info(f"TOOL_LOG: get_shipping_options called for warehouse_id='{warehouse_id}', zone='{zone}', product_id='{product_id}'")
    
    # Get all options for the warehouse and zone
    options_for_zone = SHIPPING_OPTIONS_DB.get(warehouse_id, {}).get(zone, [])
    
    # Filter options specifically for the given product_id
    product_specific_options_tuples = [opt for opt in options_for_zone if opt[0] == product_id]
    
    # Reformat the tuples into dictionaries for clearer JSON output to the LLM
    formatted_options = []
    for opt_tuple in product_specific_options_tuples:
        # opt_tuple is (product_id, carrier, cost, days, co2_kg)
        formatted_options.append({
            "carrier": opt_tuple[1],
            "cost": opt_tuple[2],
            "days": opt_tuple[3],
            "co2_kg": opt_tuple[4]
        })
        
    result_json = json.dumps(formatted_options)
    logger.info(f"TOOL_LOG: get_shipping_options returning for {warehouse_id} to {zone} for {product_id}: {result_json}")
    return result_json

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
