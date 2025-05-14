# src/api_server.py

import asyncio
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS # For handling Cross-Origin Resource Sharing

# Assuming PYTHONPATH is set to include src, or api_server.py is run with src as CWD
from main import main_fabric_intelligence # Import your agent workflow entry point
from fabric_data import MOCK_CRM_DB, FABRIC_ORDERS_DATA # Import customer data and order data

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, good for development

# Configure basic logging for the Flask app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/fabric-intelligence-chat', methods=['POST'])
def handle_chat_query():
    try:
        data = request.get_json()
        # Expecting a 'messages' array now, similar to OpenAI API format
        if not data or 'messages' not in data or not isinstance(data['messages'], list):
            logger.warning("API_SERVER: Received bad request - no messages array provided.")
            return jsonify({"error": "No messages array provided"}), 400

        messages_history = data['messages']
        logger.info(f"API_SERVER: Received messages history (last message is current query): {messages_history[-1] if messages_history else '[]'}")

        # Flask routes are synchronous, so we use asyncio.run() to call the async agent function.
        # For production, consider async Flask (e.g., Quart) or other async handling.
        agent_response_dict = asyncio.run(main_fabric_intelligence(messages_history))
        
        logger.info(f"API_SERVER: Agent response: {agent_response_dict}")
        return jsonify(agent_response_dict) # main_fabric_intelligence already returns a dict

    except Exception as e:
        logger.error(f"API_SERVER: Error handling request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers', methods=['GET'])
def get_all_customers():
    try:
        logger.info("API_SERVER: Request received for /api/customers")
        # MOCK_CRM_DB is a dict; convert to a list of customer objects for easier iteration on frontend
        customer_list = []
        for cust_id, details in MOCK_CRM_DB.items():
            customer_list.append({
                "customerId": cust_id,
                "name": details.get("name"),
                "email": details.get("email"),
                "zipCode": details.get("zip_code"),
                "tier": details.get("tier")
            })
        logger.info(f"API_SERVER: Returning {len(customer_list)} customers.")
        return jsonify(customer_list)
    except Exception as e:
        logger.error(f"API_SERVER: Error handling /api/customers request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_all_orders_summary():
    try:
        logger.info("API_SERVER: Request received for /api/orders (summary list)")
        orders_summary_list = []
        for order_id, details in FABRIC_ORDERS_DATA.items():
            order_summary = details.get('orderSummary', {})
            currency_symbol = "$" if order_summary.get('currency') == 'USD' else order_summary.get('currency', '')
            order_total_str = f"{currency_symbol}{order_summary.get('total', '0.00')}"
            
            orders_summary_list.append({
                "orderNumber": details.get("orderId"),
                "customerName": details.get("customerName"),
                "customerEmail": details.get("customerEmail"),
                "orderTotal": order_total_str,
                "orderStatus": details.get("status"),
                "paymentStatus": details.get("paymentStatus", "Paid")
            })
        logger.info(f"API_SERVER: Returning summary for {len(orders_summary_list)} orders.")
        return jsonify(orders_summary_list)
    except Exception as e:
        logger.error(f"API_SERVER: Error handling /api/orders request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order_details(order_id):
    try:
        logger.info(f"API_SERVER: Request received for /api/orders/{order_id}")
        order_details = FABRIC_ORDERS_DATA.get(order_id)
        if order_details:
            logger.info(f"API_SERVER: Returning details for order {order_id}.")
            return jsonify(order_details)
        else:
            logger.warning(f"API_SERVER: Order {order_id} not found.")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        logger.error(f"API_SERVER: Error handling /api/orders/{order_id} request: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Note: For this to work, you might need to run this with PYTHONPATH=src 
    # if you are in the project root, e.g., `PYTHONPATH=src python src/api_server.py`
    # Or, if you cd into src, then `python api_server.py` might work if imports are adjusted.
    # The agent library and its dependencies (like openai) must be in the Python environment.
    # Also, ensure Flask and Flask-CORS are installed: `pip install Flask Flask-CORS`
    logger.info("Starting Flask API server for Fabric Intelligence...")
    app.run(host='0.0.0.0', port=5001, debug=True) # Using port 5001 to avoid conflict with http.server 