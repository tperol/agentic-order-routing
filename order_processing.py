# order_processing.py
# This file contains the logic for the OrderIntakeAgent.
# Its primary function is to process raw incoming orders, validate them,
# and enrich them with customer data from the MOCK_CRM_DB.

from mock_data import MOCK_CRM_DB # Importing the customer database

def process_order_intake(raw_order: dict) -> dict | None:
    """
    Simulates the Order Intake Agent.
    Validates the raw order structure and enriches it with customer details
    from MOCK_CRM_DB (e.g., zip_code, customer_tier).

    Args:
        raw_order: A dictionary representing the raw order. Expected keys:
                   "product_id", "quantity", "customer_id".

    Returns:
        A dictionary representing the processed and enriched order if successful,
        None otherwise. The processed order includes original details plus
        "customer_name", "customer_zip_code", and "customer_tier".
    """
    print(f"INTAKE_AGENT_LOG: Received raw order for processing: {raw_order}")

    # Basic validation of raw_order structure
    required_keys = ["product_id", "quantity", "customer_id"]
    if not all(key in raw_order for key in required_keys):
        print("INTAKE_AGENT_LOG: Invalid raw order structure. Missing one or more required keys.")
        print(f"INTAKE_AGENT_LOG: Required keys are: {required_keys}")
        return None

    product_id = raw_order["product_id"]
    quantity = raw_order["quantity"]
    customer_id = raw_order["customer_id"]

    if not isinstance(quantity, int) or quantity <= 0:
        print(f"INTAKE_AGENT_LOG: Invalid quantity '{quantity}'. Must be a positive integer.")
        return None
    
    if not product_id or not isinstance(product_id, str):
        print(f"INTAKE_AGENT_LOG: Invalid product_id '{product_id}'. Must be a non-empty string.")
        return None

    if not customer_id or not isinstance(customer_id, str):
        print(f"INTAKE_AGENT_LOG: Invalid customer_id '{customer_id}'. Must be a non-empty string.")
        return None

    # Fetch customer data from MOCK_CRM_DB
    customer_data = MOCK_CRM_DB.get(customer_id)
    if not customer_data:
        print(f"INTAKE_AGENT_LOG: Customer ID '{customer_id}' not found in CRM.")
        return None

    # Enrich the order
    processed_order = {
        "product_id": product_id,
        "quantity": quantity,
        "customer_id": customer_id,
        "customer_name": customer_data.get("name", "N/A"),
        "customer_zip_code": customer_data.get("zip_code"), # Crucial for routing
        "customer_tier": customer_data.get("tier", "standard") # Default tier if not specified
    }

    # Final validation for crucial enriched data
    if not processed_order["customer_zip_code"]:
        print(f"INTAKE_AGENT_LOG: Customer '{customer_id}' found, but missing ZIP code in CRM data. Cannot route.")
        return None

    print(f"INTAKE_AGENT_LOG: Order processed and enriched successfully: {processed_order}")
    return processed_order

# --- Main block for testing the order intake process directly ---
if __name__ == '__main__':
    print("--- Testing order_processing.py ---")

    # Test case 1: Valid order for a known customer
    test_order_1 = {"product_id": "product_A", "quantity": 1, "customer_id": "cust123"}
    print(f"\n[Test 1] Input: {test_order_1}")
    processed_1 = process_order_intake(test_order_1)
    print(f"Processed Output 1: {processed_1}")

    # Test case 2: Valid order for another known customer
    test_order_2 = {"product_id": "product_B", "quantity": 5, "customer_id": "cust456"}
    print(f"\n[Test 2] Input: {test_order_2}")
    processed_2 = process_order_intake(test_order_2)
    print(f"Processed Output 2: {processed_2}")

    # Test case 3: Order for an unknown customer
    test_order_3 = {"product_id": "product_C", "quantity": 2, "customer_id": "cust999_unknown"}
    print(f"\n[Test 3] Input: {test_order_3}")
    processed_3 = process_order_intake(test_order_3)
    print(f"Processed Output 3: {processed_3}") # Expected: None

    # Test case 4: Order with missing product_id
    test_order_4 = {"quantity": 1, "customer_id": "cust123"}
    print(f"\n[Test 4] Input: {test_order_4}")
    processed_4 = process_order_intake(test_order_4)
    print(f"Processed Output 4: {processed_4}") # Expected: None

    # Test case 5: Order with invalid quantity
    test_order_5 = {"product_id": "product_A", "quantity": 0, "customer_id": "cust123"}
    print(f"\n[Test 5] Input: {test_order_5}")
    processed_5 = process_order_intake(test_order_5)
    print(f"Processed Output 5: {processed_5}") # Expected: None

    # Test case 6: Customer exists but is missing a ZIP code in CRM (hypothetical)
    # To test this, you'd temporarily modify MOCK_CRM_DB for a user.
    # For example, if MOCK_CRM_DB['cust_no_zip'] = {"name": "No Zip User", "tier": "bronze"}
    # MOCK_CRM_DB["cust_no_zip"] = {"name": "No Zip User", "zip_code": None, "tier": "bronze"} # Simulate missing zip
    # test_order_6 = {"product_id": "product_A", "quantity": 1, "customer_id": "cust_no_zip"}
    # print(f"\n[Test 6] Input: {test_order_6}")
    # processed_6 = process_order_intake(test_order_6)
    # print(f"Processed Output 6: {processed_6}") # Expected: None
    # del MOCK_CRM_DB["cust_no_zip"] # Clean up

    print("\n--- End of order_processing.py tests ---")
