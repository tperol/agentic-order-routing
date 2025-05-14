from agents import function_tool
from pydantic import BaseModel, Field
from fabric_data import FABRIC_ORDERS_DATA # Import orders data from fabric_data

class GetOrderStatusByIdInput(BaseModel):
    order_id: str = Field(description="The ID of the order to query.")

@function_tool
def get_order_status_by_id(inputs: GetOrderStatusByIdInput) -> dict:
    """Fetches the current status and shipping information for a specific order ID."""
    order_id = inputs.order_id
    if order_id in FABRIC_ORDERS_DATA:
        return {"status": "success", "data": FABRIC_ORDERS_DATA[order_id]}
    else:
        return {"status": "not_found", "message": f"Order details not found for ID: {order_id}"}

class FindOrdersForCustomerInput(BaseModel):
    customer_identifier: str = Field(description="Customer email or customer ID.")

@function_tool
def find_orders_for_customer(inputs: FindOrdersForCustomerInput) -> dict:
    """Fetches a list of recent orders for a given customer identifier."""
    customer_id_lower = inputs.customer_identifier.lower()
    matching_orders = []
    for order_details in FABRIC_ORDERS_DATA.values():
        if customer_id_lower in order_details.get("customerName", "").lower() or \
           customer_id_lower == order_details.get("orderId", "").lower(): # Simple check
            matching_orders.append(order_details)
    
    if matching_orders:
        return {"status": "success", "data": matching_orders[:5]} # Return up to 5 matches
    else:
        return {"status": "not_found", "message": f"No orders found for customer: {inputs.customer_identifier}"} 