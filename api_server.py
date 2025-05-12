# api_server.py
import logging
import asyncio
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List
import uvicorn

from src.agentic_order_routing.main import main
from src.agentic_order_routing.mock_data import INVENTORY_DB, MOCK_CRM_DB, SHIPPING_OPTIONS_DB, ZIP_TO_ZONE_DB


# --- Logging Setup ---
# Create a custom list handler to capture logs for each request
class ListHandler(logging.Handler):
    def __init__(self, log_list: List[str]):
        super().__init__()
        self.log_list = log_list

    def emit(self, record: logging.LogRecord):
        self.log_list.append(self.format(record))

# Configure the root logger or a specific logger for the agent workflow
# We will add/remove the ListHandler per request to keep logs request-specific
workflow_logger = logging.getLogger("agent_workflow") # Same name as used in other modules
workflow_logger.setLevel(logging.INFO) # Set the level for this specific logger

# Basic console handler for server logs (uvicorn will also log)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
))
if not workflow_logger.hasHandlers(): # Avoid adding multiple console handlers on reloads
    workflow_logger.addHandler(console_handler)


# --- FastAPI App ---
app = FastAPI(title="AI Order Routing API")

# Mount static files (for dashboard.html)
# Assumes dashboard.html is in a 'static' directory at the project root
# Create this 'static' directory and place your dashboard.html there.
if not os.path.exists("static"):
    os.makedirs("static", exist_ok=True)
    # You might want to copy the dashboard.html to static/dashboard.html here
    # or instruct the user to do so. For now, we assume it will be there.
    
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Pydantic Models for Request/Response ---
class OrderOptimizationRequest(BaseModel):
    product_id: str
    quantity: int
    customer_id: str
    business_priority: str

class OptimizationResponse(BaseModel):
    result: Dict[str, Any]
    logs: List[str]

class ContextualDataResponse(BaseModel):
    inventory_summary: Dict[str, Dict[str, int]]  # {product_id: {warehouse: stock}}
    warehouse_count: int
    product_count: int
    customer_count: int
    zone_count: int

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_dashboard(request: Request):
    # Serve the dashboard.html
    # Ensure dashboard.html is in the 'static' directory
    dashboard_path = os.path.join("static", "dashboard.html")
    if not os.path.exists(dashboard_path):
        return HTMLResponse("<html><body><h1>Dashboard not found.</h1><p>Place dashboard.html in the 'static' directory.</p></body></html>", status_code=404)
    
    with open(dashboard_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/optimize-route")
async def optimize_route_endpoint(request_data: OrderOptimizationRequest):
    logger.info(f"API_CALL: /optimize-route received request: {request_data.model_dump()}")
    
    request_logs = []
    list_handler = ListHandler(request_logs)
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s') # Simple format for UI
    list_handler.setFormatter(formatter)
    
    # Add per-request handler to capture logs for this specific call
    workflow_logger.addHandler(list_handler)
    
    try:
        raw_order_details = {
            "product_id": request_data.product_id,
            "quantity": request_data.quantity,
            "customer_id": request_data.customer_id
        }
        
        # Run the asynchronous agent workflow
        optimization_result = await main(
            raw_order_details,
            request_data.business_priority
        )
        
        # If optimization_result is None, return a default error response
        if optimization_result is None:
            logger.error("API_RESPONSE_ERROR: Workflow returned None.")
            return {
                "error": "Failed to process the request.",
                "logs": request_logs
            }
        
        # If error in result, return error key
        if "error" in optimization_result:
            logger.error(f"API_RESPONSE_ERROR: Workflow returned an error: {optimization_result['error']}")
            return {
                "error": optimization_result["error"],
                "logs": request_logs
            }

        # Otherwise, format the response for the UI
        response = {
            "recommendation": optimization_result.get("recommendation"),
            "reasoning": optimization_result.get("reasoning"),
            "alternatives_considered": optimization_result.get("alternatives_considered", []),
            "logs": request_logs
        }
        logger.info("API_RESPONSE_SUCCESS: Workflow completed successfully.")
        return response

    except Exception as e:
        logger.error(f"API_EXCEPTION: Unhandled exception in /optimize-route: {e}", exc_info=True)
        # Include logs captured so far, even if an unexpected exception occurred
        return {
            "error": f"Internal server error: {str(e)}",
            "logs": request_logs
        }
    finally:
        # Crucial: Remove the handler so logs don't accumulate across requests
        workflow_logger.removeHandler(list_handler)

@app.get("/contextual-data", response_model=ContextualDataResponse)
async def get_contextual_data_endpoint():
    logger.info("API_CALL: /contextual-data received request")
    try:
        inventory_summary = {}
        all_products = set()
        for wh, products in INVENTORY_DB.items():
            for prod_id, stock in products.items():
                all_products.add(prod_id)
                if prod_id not in inventory_summary:
                    inventory_summary[prod_id] = {}
                inventory_summary[prod_id][wh] = stock
        
        # For a simpler summary for the UI, let's just send the raw INVENTORY_DB
        # or a slightly processed version. The above is a bit complex for a quick viz.
        # Let's send total stock per product and stock per warehouse.
        
        processed_inventory_summary = {}
        for warehouse, stock_data in INVENTORY_DB.items():
            for product, quantity in stock_data.items():
                if product not in processed_inventory_summary:
                    processed_inventory_summary[product] = {}
                processed_inventory_summary[product][warehouse] = quantity

        return ContextualDataResponse(
            inventory_summary=processed_inventory_summary,  # Sending detailed breakdown
            warehouse_count=len(INVENTORY_DB),
            product_count=len(all_products),
            customer_count=len(MOCK_CRM_DB),
            zone_count=len(set(ZIP_TO_ZONE_DB.values()))  # Count unique zones
        )
    except Exception as e:
        logger.error(f"API_EXCEPTION: Error in /contextual-data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching contextual data: {str(e)}")

if __name__ == "__main__":
    # This allows running the server directly with `python api_server.py`
    # For production, use a process manager like Gunicorn: `uvicorn api_server:app --reload`
    logger = logging.getLogger(__name__)
    logger.info("Starting FastAPI server with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

