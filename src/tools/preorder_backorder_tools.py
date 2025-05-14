from agents import function_tool
from pydantic import BaseModel, Field
import datetime
import random

# For tools that might need access to broader data:
from fabric_data import FABRIC_INVENTORY_DATA, FABRIC_ORDERS_DATA, MOCK_CRM_DB

class ProductETAGetInput(BaseModel):
    sku: str = Field(description="The SKU code of the product.")

@function_tool
def get_product_eta_tool(inputs: ProductETAGetInput) -> dict:
    """Fetches the Estimated Time of Arrival (ETA) or restock date for a given SKU."""
    # Mock implementation: Check if product has an ETA, otherwise generate a random future date
    sku = inputs.sku
    for item in FABRIC_INVENTORY_DATA:
        if item["skuCode"] == sku:
            if item.get("eta"): # Assuming an 'eta' field might exist in detailed inventory data
                return {"status": "success", "sku": sku, "eta": item["eta"], "message": f"ETA for {sku} is {item['eta']}."}
            elif item["status"] == "Preorder" or item["status"] == "Backorder":
                days_offset = random.randint(7, 45)
                eta_date = (datetime.date.today() + datetime.timedelta(days=days_offset)).isoformat()
                return {"status": "success", "sku": sku, "eta": eta_date, "message": f"Estimated restock for {sku} is around {eta_date}."}
            else:
                return {"status": "not_applicable", "sku": sku, "message": f"{sku} is currently 'Available' or 'Low stock', no specific ETA applies for restock."}
    return {"status": "not_found", "sku": sku, "message": f"SKU {sku} not found in inventory records."}

class AlternativeSourcingInput(BaseModel):
    sku: str = Field(description="The SKU of the item.")
    original_order_id: str = Field(description="The original order ID containing the item.")

@function_tool
def check_alternative_sourcing_tool(inputs: AlternativeSourcingInput) -> dict:
    """Checks for alternative fulfillment options for an item on a specific order (e.g., drop-shipping, transfer from another store). Placeholder."""
    # Mock implementation
    if random.choice([True, False]):
        return {"status": "found", "sku": inputs.sku, "order_id": inputs.original_order_id, "message": f"Alternative sourcing found for {inputs.sku}: Can be drop-shipped in 3-5 days."}
    else:
        return {"status": "not_found", "sku": inputs.sku, "order_id": inputs.original_order_id, "message": f"No immediate alternative sourcing found for {inputs.sku}."}

class NotifyCustomerInput(BaseModel):
    customer_id: str = Field(description="The ID of the customer to notify.")
    order_id: str = Field(description="The relevant order ID for the notification.")
    message: str = Field(description="The message content to send to the customer.")

@function_tool
def notify_customer_tool(inputs: NotifyCustomerInput) -> dict:
    """Simulates sending a notification message to the customer regarding their pre-order/backorder."""
    # Mock implementation - in a real system, this would integrate with an email/SMS service
    print(f"SIMULATION: Notifying customer {inputs.customer_id} for order {inputs.order_id}: '{inputs.message}'")
    return {"status": "success", "message": "Customer notification simulated successfully."} 