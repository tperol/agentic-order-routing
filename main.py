# run_poc.py
# Main orchestrator for the Agentic AI Order Routing POC.
# This script manages interactions with two OpenAI Assistants:
# 1. OrderIntakeAssistant: Processes and enriches raw orders.
# 2. OrderRoutingDecisionAssistant: Determines the optimal fulfillment route.

import os
import json
import time # For polling
from agents import Agent, Runner, gen_trace_id, trace
from dotenv import load_dotenv

# Import tools for each assistant
from intake_agent_tools import get_customer_details_tool
from routing_tools import get_customer_zone, get_inventory, get_shipping_options

# --- Load Environment Variables (OpenAI API Key) ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file or environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Assistant Definitions ---

# 1. OrderIntakeAssistant: Processes and enriches raw orders.
ORDER_INTAKE_ASSISTANT_NAME = "OrderIntakePOC_Assistant_v2"
ORDER_INTAKE_ASSISTANT_INSTRUCTIONS = """
You are an AI Order Intake Agent. Your primary responsibility is to receive raw order information,
validate its basic structure, enrich it with customer details, and then prepare a structured
'processed_order' JSON object for handoff to the Order Routing Decision Agent.

Input: You will receive a raw order as a JSON string, typically containing at least
`product_id`, `quantity`, and `customer_id`.

Your Workflow:
1.  Parse the input JSON string to get the raw order dictionary.
2.  Validate Raw Order Structure: Ensure the raw order contains the essential fields:
    `product_id` (string), `quantity` (positive integer), and `customer_id` (string).
    If validation fails, your output MUST be a JSON string: {"error": "Validation failed: [reason]"}.
3.  Enrich with Customer Details: Use the `get_customer_details_tool` with the `customer_id`
    from the raw order to fetch the customer's name, ZIP code, and tier.
4.  Handle Tool Output:
    * If `get_customer_details_tool` returns an error (e.g., customer not found, ZIP missing),
        your output MUST be that error JSON string.
    * If successful, it will return customer details as a JSON string. Parse this.
5.  Construct Processed Order: Combine the original valid order information with the successfully
    retrieved and valid customer details to create a `processed_order` dictionary.
    This object MUST include: `product_id`, `quantity`, `customer_id`, `customer_name`,
    `customer_zip_code`, and `customer_tier`.
6.  Output: Your final response MUST be ONLY the `processed_order` as a JSON string if all steps
    were successful. If any step results in an error, your final response MUST be ONLY the
    JSON string containing the error message (e.g., `{"error": "Detailed error message"}`).
    Do not add any conversational fluff or introductory/concluding remarks.
"""
ORDER_INTAKE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_details_tool",
            "description": "Fetches customer details (name, zip_code, tier) from the CRM based on customer_id. Returns a JSON string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "The ID of the customer to fetch details for."}
                },
                "required": ["customer_id"],
            },
        },
    }
]

# 2. OrderRoutingDecisionAssistant: Determines the optimal fulfillment route.
ORDER_ROUTING_DECISION_ASSISTANT_NAME = "OrderRoutingDecisionPOC_Assistant_v2"
ORDER_ROUTING_DECISION_ASSISTANT_INSTRUCTIONS = """
You are the AI Order Routing Decision Agent. You will receive a 'processed_order' JSON
(which includes product, quantity, customer details like ZIP code and tier) and a 'business_priority' string.

Your primary role is to orchestrate information gathering using specialized tools and then
decide the optimal fulfillment route.

Available Tools:
1. `get_customer_zone(zip_code)`: Queries our Customer Zone Service.
2. `get_inventory(product_id, quantity)`: Queries our Inventory Agent's knowledge base for stock.
3. `get_shipping_options(warehouse_id, zone, product_id)`: Queries our Logistics Agent for shipping methods, costs, ETAs, and CO2 data.

Workflow:
1.  Acknowledge the processed order details (parse the JSON string) and the business priority.
2.  Use `get_customer_zone` to determine the customer's shipping zone from their `customer_zip_code`.
3.  Use `get_inventory` to find all fulfillment locations with sufficient stock for the order's `product_id` and `quantity`.
4.  If no stock is found anywhere, your output MUST be a JSON string: {"error": "No stock available for the product."}.
5.  For each valid location with stock:
    a. Use `get_shipping_options` to get all shipping options to the customer's zone for the product.
6.  Evaluate all potential fulfillment routes (location + shipping option) against the stated `business_priority`.
    * Valid priorities: "MINIMIZE_COST", "MINIMIZE_DELIVERY_TIME", "MINIMIZE_CO2", "BALANCED_COST_TIME", "PRIORITIZE_GOLD_TIER_SPEED".
    * If "PRIORITIZE_GOLD_TIER_SPEED" and the `customer_tier` in the processed order is "gold", give extra weight to faster options, even if slightly more expensive.
7.  Present your final recommendation as a JSON string. This JSON should contain:
    `recommendation`: { "fulfillment_location": "...", "carrier": "...", "cost": ..., "delivery_days": ..., "co2_kg": ... },
    `reasoning`: "A clear explanation...",
    `alternatives_considered`: [ { "fulfillment_location": "...", ...}, ... ] (1-2 alternatives)
8.  If no suitable route is found after checking options, your output MUST be a JSON string: {"error": "No suitable shipping options found."}.
Do not add any conversational fluff. Your entire output must be a single JSON string.
"""
ORDER_ROUTING_DECISION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_zone",
            "description": "Determines the shipping zone for a customer based on their zip code.",
            "parameters": {
                "type": "object",
                "properties": {"zip_code": {"type": "string", "description": "The customer's ZIP code."}},
                "required": ["zip_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_inventory",
            "description": "Checks stock levels for a product across all fulfillment locations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The ID of the product."},
                    "quantity": {"type": "integer", "description": "The desired quantity."},
                },
                "required": ["product_id", "quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_shipping_options",
            "description": "Fetches shipping methods, costs, ETAs, and CO2 impact from a warehouse to a zone for a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "warehouse_id": {"type": "string", "description": "The ID of the fulfillment warehouse/location."},
                    "zone": {"type": "string", "description": "The customer's shipping zone."},
                    "product_id": {"type": "string", "description": "The ID of the product being shipped."},
                },
                "required": ["warehouse_id", "zone", "product_id"],
            },
        },
    },
]

# --- Helper Function to Get or Create Assistant ---
def get_or_create_assistant(name, instructions, tools_config, model="gpt-4o"): # Using gpt-4o
    # Check if assistant already exists (simplified: by name in a list, real app might use metadata)
    try:
        assistants = client.beta.assistants.list(limit=100)
        for assistant in assistants.data:
            if assistant.name == name:
                print(f"Found existing assistant '{name}' with ID: {assistant.id}")
                return assistant
    except Exception as e:
        print(f"Error listing assistants: {e}. Proceeding to create a new one.")

    print(f"Creating new assistant: {name}...")
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools_config,
        model=model
    )
    print(f"Created assistant '{name}' with ID: {assistant.id}")
    return assistant

# --- Helper Function to Run an Assistant with a User Message ---
def run_assistant(assistant_id, user_message_content, available_tools_map):
    print(f"\n--- Running Assistant ID: {assistant_id} ---")
    print(f"User Message: {user_message_content}")

    thread = client.beta.threads.create()
    print(f"Created Thread ID: {thread.id}")

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message_content
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    print(f"Created Run ID: {run.id}")

    while run.status in ["queued", "in_progress", "requires_action"]:
        if run.status == "requires_action":
            print("Run requires action. Processing tool calls...")
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"  Tool Call: {func_name}({args})")
                
                if func_name in available_tools_map:
                    tool_function = available_tools_map[func_name]
                    try:
                        output = tool_function(**args)
                        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                    except Exception as e:
                        print(f"  Error calling tool {func_name}: {e}")
                        # It's important to still submit an output, even if it's an error message
                        tool_outputs.append({"tool_call_id": tool_call.id, "output": json.dumps({"error": str(e)})})
                else:
                    print(f"  Error: Unknown tool function {func_name}")
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": json.dumps({"error": f"Unknown tool: {func_name}"})})
            
            if tool_outputs:
                try:
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                except Exception as e:
                    print(f"Error submitting tool outputs: {e}")
                    run.status = "failed" # Manually fail the run if submission fails
                    break 
        
        time.sleep(1) # Poll interval
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Polling Run Status: {run.status}")

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id, order="desc") # Get latest first
        assistant_message = None
        for msg in messages.data:
            if msg.role == "assistant":
                assistant_message = msg.content[0].text.value
                break
        print(f"Assistant Response: {assistant_message}")
        return assistant_message
    else:
        print(f"Run finished with status: {run.status}")
        if run.last_error:
            print(f"Run Error: {run.last_error.message}")
        return json.dumps({"error": f"Run failed or ended unexpectedly with status: {run.status}"})


# --- Main Orchestration Logic ---
def orchestrate_order_routing(raw_order_details, business_priority, intake_assistant, routing_assistant):
    print(f"\n\n=== Orchestrating Order Routing for: {raw_order_details}, Priority: {business_priority} ===")

    # Step 1: Call OrderIntakeAssistant
    print("\n--- Step 1: Calling Order Intake Assistant ---")
    intake_tools_map = {"get_customer_details_tool": get_customer_details_tool}
    # The OrderIntakeAssistant expects the raw_order as a JSON string in the content
    raw_order_json_string = json.dumps(raw_order_details)
    
    processed_order_json_str = run_assistant(
        intake_assistant.id,
        raw_order_json_string, # Pass the raw order as a JSON string
        intake_tools_map
    )

    try:
        processed_order_data = json.loads(processed_order_json_str)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: OrderIntakeAssistant did not return valid JSON: {processed_order_json_str}")
        return {"error": "Intake assistant failed to produce valid JSON."}

    if "error" in processed_order_data:
        print(f"Order Intake Failed: {processed_order_data['error']}")
        return processed_order_data # Return the error from intake

    print(f"Intake Successful. Processed Order: {processed_order_data}")

    # Step 2: Call OrderRoutingDecisionAssistant
    print("\n--- Step 2: Calling Order Routing Decision Assistant ---")
    routing_tools_map = {
        "get_customer_zone": get_customer_zone,
        "get_inventory": get_inventory,
        "get_shipping_options": get_shipping_options
    }
    # The OrderRoutingDecisionAssistant expects a JSON string containing both processed_order and business_priority
    routing_input_dict = {
        "processed_order": processed_order_data,
        "business_priority": business_priority
    }
    routing_input_json_string = json.dumps(routing_input_dict)

    final_recommendation_json_str = run_assistant(
        routing_assistant.id,
        routing_input_json_string,
        routing_tools_map
    )
    
    try:
        final_recommendation_data = json.loads(final_recommendation_json_str)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: OrderRoutingDecisionAssistant did not return valid JSON: {final_recommendation_json_str}")
        return {"error": "Routing assistant failed to produce valid JSON."}

    print("\n--- Final Routing Recommendation ---")
    # Pretty print the final JSON output
    print(json.dumps(final_recommendation_data, indent=2))
    return final_recommendation_data


if __name__ == "__main__":
    print("Initializing Assistants (this might take a moment)...")
    order_intake_assistant = get_or_create_assistant(
        ORDER_INTAKE_ASSISTANT_NAME,
        ORDER_INTAKE_ASSISTANT_INSTRUCTIONS,
        ORDER_INTAKE_TOOLS
    )
    order_routing_decision_assistant = get_or_create_assistant(
        ORDER_ROUTING_DECISION_ASSISTANT_NAME,
        ORDER_ROUTING_DECISION_ASSISTANT_INSTRUCTIONS,
        ORDER_ROUTING_DECISION_TOOLS
    )
    print("Assistants initialized.")

    # --- Test Scenarios ---
    raw_order_1 = {"product_id": "product_A", "quantity": 1, "customer_id": "cust123"} # Alice, Gold, Zip 10001
    priority_1 = "PRIORITIZE_GOLD_TIER_SPEED"
    orchestrate_order_routing(raw_order_1, priority_1, order_intake_assistant, order_routing_decision_assistant)

    raw_order_2 = {"product_id": "product_D", "quantity": 2, "customer_id": "cust456"} # Bob, Silver, Zip 90210
    priority_2 = "MINIMIZE_COST"
    orchestrate_order_routing(raw_order_2, priority_2, order_intake_assistant, order_routing_decision_assistant)

    raw_order_3 = {"product_id": "product_A", "quantity": 1, "customer_id": "cust789"} # Charlie, Bronze, Zip 60606
    priority_3 = "MINIMIZE_CO2"
    orchestrate_order_routing(raw_order_3, priority_3, order_intake_assistant, order_routing_decision_assistant)
    
    raw_order_4_invalid_cust = {"product_id": "product_A", "quantity": 1, "customer_id": "cust_INVALID"}
    priority_4 = "MINIMIZE_COST"
    orchestrate_order_routing(raw_order_4_invalid_cust, priority_4, order_intake_assistant, order_routing_decision_assistant)

    raw_order_5_invalid_structure = {"prod_id": "product_A", "qty": 1, "cust_id": "cust123"} # Wrong keys
    priority_5 = "MINIMIZE_COST"
    orchestrate_order_routing(raw_order_5_invalid_structure, priority_5, order_intake_assistant, order_routing_decision_assistant)

