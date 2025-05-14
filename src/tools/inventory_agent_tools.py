from agents import function_tool
from pydantic import BaseModel, Field
from fabric_data import FABRIC_INVENTORY_DATA 

# Placeholder mock data - in a real app, this would connect to fabric_data.py or a DB
# ... (rest of file, MOCK_FABRIC_INVENTORY_FOR_TOOLS should be removed if not used, or also use new import)
# For now, I'll assume the tools only use FABRIC_INVENTORY_DATA as per recent changes.
# The MOCK_FABRIC_INVENTORY_FOR_TOOLS seems like a leftover from previous refactoring stages.
# I will remove MOCK_FABRIC_INVENTORY_FOR_TOOLS to avoid confusion.

class GetInventoryDetailsForSKUInput(BaseModel):
    sku: str = Field(description="The SKU code of the product to query.")

@function_tool
def get_inventory_details_for_sku(inputs: GetInventoryDetailsForSKUInput) -> dict:
    """Fetches detailed inventory information for a specific SKU, including stock levels across different locations and channels."""
    sku_to_find = inputs.sku
    for item in FABRIC_INVENTORY_DATA:
        if item["skuCode"] == sku_to_find:
            return {"status": "success", "data": item}
    return {"status": "not_found", "message": f"Inventory details not found for SKU: {sku_to_find}"}

class GetOverallStockForProductInput(BaseModel):
    product_name_query: str = Field(description="A query string for the product name (e.g., 'Bookcase', 'Red Chair').")

@function_tool
def get_overall_stock_for_product(inputs: GetOverallStockForProductInput) -> dict:
    """Fetches summarized stock information for products matching a product name query."""
    query_lower = inputs.product_name_query.lower()
    matching_items = [
        item for item in FABRIC_INVENTORY_DATA 
        if query_lower in item["productName"].lower()
    ]
    
    if not matching_items:
        return {"status": "not_found", "message": f"No products found matching query: '{inputs.product_name_query}'"}
    
    return {
        "status": "success", 
        "message": f"Found {len(matching_items)} items matching '{inputs.product_name_query}'.",
        "data": matching_items[:10] 
    } 