# This file contains tool functions for the OrderIntakeAssistant/Agent.
# These tools help in validating and enriching raw order data.

import json
from agentic_order_routing.mock_data import MOCK_CRM_DB # Importing the customer database
from agents import function_tool

@function_tool
def get_customer_details_tool(customer_id: str) -> str:
    """
    Fetches customer details from the MOCK_CRM_DB based on customer_id.
    This tool is designed to be used by an AI agent (e.g., OrderIntakeAgent).

    Args:
        customer_id: The ID of the customer.

    Returns:
        A JSON string containing customer details (name, zip_code, tier) if found.
        Returns a JSON string with an error message if the customer is not found
        or if crucial data like zip_code is missing.
    """
    print(f"INTAKE_TOOL_LOG: get_customer_details_tool called for customer_id='{customer_id}'")

    if not customer_id or not isinstance(customer_id, str):
        error_msg = {"error": "Invalid customer_id format. Must be a non-empty string."}
        print(f"INTAKE_TOOL_LOG: Returning error: {json.dumps(error_msg)}")
        return json.dumps(error_msg)

    customer_data = MOCK_CRM_DB.get(customer_id)
    if not customer_data:
        error_msg = {"error": f"Customer ID '{customer_id}' not found in CRM."}
        print(f"INTAKE_TOOL_LOG: Returning error: {json.dumps(error_msg)}")
        return json.dumps(error_msg)

    # Ensure essential data for routing is present
    zip_code = customer_data.get("zip_code")
    if not zip_code:
        error_msg = {"error": f"Customer ID '{customer_id}' found, but essential zip_code is missing from CRM data."}
        print(f"INTAKE_TOOL_LOG: Returning error: {json.dumps(error_msg)}")
        return json.dumps(error_msg)

    # Prepare successful data structure
    customer_details_for_agent = {
        "customer_id": customer_id,
        "name": customer_data.get("name", "N/A"),
        "zip_code": zip_code, # Already validated to exist
        "tier": customer_data.get("tier", "standard") # Default tier if not specified
    }
    
    result_json = json.dumps(customer_details_for_agent)
    print(f"INTAKE_TOOL_LOG: Returning customer details: {result_json}")
    return result_json

# --- Main block for testing the tool directly ---
if __name__ == '__main__':
    print("--- Testing intake_agent_tools.py ---")

    # Test case 1: Valid customer
    print(f"\n[Test 1] Customer 'cust123':")
    details_1 = get_customer_details_tool("cust123")
    print(f"Output 1: {details_1}")
    # Expected: {"customer_id": "cust123", "name": "Alice Wonderland", "zip_code": "10001", "tier": "gold"}

    # Test case 2: Another valid customer
    print(f"\n[Test 2] Customer 'cust456':")
    details_2 = get_customer_details_tool("cust456")
    print(f"Output 2: {details_2}")
    # Expected: {"customer_id": "cust456", "name": "Bob The Builder", "zip_code": "90210", "tier": "silver"}


    # Test case 3: Unknown customer
    print(f"\n[Test 3] Customer 'cust999_unknown':")
    details_3 = get_customer_details_tool("cust999_unknown")
    print(f"Output 3: {details_3}") 
    # Expected: {"error": "Customer ID 'cust999_unknown' not found in CRM."}

    # Test case 4: Invalid customer_id format (e.g., empty string)
    print(f"\n[Test 4] Customer '':")
    details_4 = get_customer_details_tool("")
    print(f"Output 4: {details_4}") 
    # Expected: {"error": "Invalid customer_id format. Must be a non-empty string."}
    
    # Test case 5: Customer exists but is missing a ZIP code in CRM (hypothetical)
    # Temporarily modify MOCK_CRM_DB for this test
    original_cust101_data = MOCK_CRM_DB.get("cust101")
    if original_cust101_data:
        temp_cust_data = original_cust101_data.copy()
        original_zip = temp_cust_data.pop("zip_code", None) # Remove zip_code

        MOCK_CRM_DB["cust101_temp_nozip"] = temp_cust_data # Add temporary data without zip

        print(f"\n[Test 5] Customer 'cust101_temp_nozip' (temporarily no zip):")
        details_5 = get_customer_details_tool("cust101_temp_nozip")
        print(f"Output 5: {details_5}")
        # Expected: {"error": "Customer ID 'cust101_temp_nozip' found, but essential zip_code is missing from CRM data."}
        
        # Clean up: remove temporary entry
        del MOCK_CRM_DB["cust101_temp_nozip"]
    else:
        print("\n[Test 5] Skipped: cust101 not found in MOCK_CRM_DB for modification.")

    print("\n--- End of intake_agent_tools.py tests ---")
