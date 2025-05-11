# run_poc.py
# Main orchestrator for the Agentic AI Order Routing POC.
# This script manages interactions with two OpenAI Assistants:
# 1. OrderIntakeAssistant: Processes and enriches raw orders.
# 2. OrderRoutingDecisionAssistant: Determines the optimal fulfillment route.

import os
import json
import asyncio
import logging
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, gen_trace_id, trace, RunConfig
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import tools for each assistant
from intake_agent_tools import get_customer_details_tool
from routing_tools import get_customer_zone, get_inventory, get_shipping_options

# --- Load Environment Variables and Model ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gpt-4o"

# --- Agent Definitions ---
order_routing_agent = Agent(
    name="OrderRoutingDecisionAgent",
    handoff_description="Specialist agent for determining optimal order fulfillment routes",
    instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}
You are the AI Order Routing Decision Agent.
Your input will be a JSON string containing:
1.  A 'processed_order' object (with product_id, quantity, customer_id, customer_name, customer_zip_code, customer_tier).
2.  A 'business_priority' string.

Your primary role is to parse this input, use specialized tools to gather fulfillment options,
and then decide the optimal fulfillment route based on the provided data and priority.

Available Tools:
1. `get_customer_zone(zip_code)`: Queries a Customer Zone Service.
2. `get_inventory(product_id, quantity)`: Queries an Inventory service for stock levels.
3. `get_shipping_options(warehouse_id, zone, product_id)`: Queries a Logistics service for shipping methods, costs, ETAs, and CO2 data.

Workflow:
1.  Parse the input JSON string to get the 'processed_order' dictionary and the 'business_priority' string.
2.  Extract `customer_zip_code` from `processed_order` and use `get_customer_zone` to determine the shipping zone. 
    If the tool returns an error or an unknown zone that prevents further processing, output an error JSON.
3.  Extract `product_id` and `quantity` from `processed_order` and use `get_inventory` to find all fulfillment locations with sufficient stock.
4.  If `get_inventory` returns an error or indicates no stock (e.g., empty JSON object '{{}}' or a tool error), 
    your output MUST be a JSON string: {{"error": "No stock available for the product at any location."}}.
5.  For each valid location with stock:
    a. Use `get_shipping_options` with the location, customer's zone, and product_id to get shipping options. Accumulate all valid options.
6.  If no shipping options are found from any stocked location to the customer's zone after checking all possibilities, 
    your output MUST be a JSON string: {{"error": "No shipping options available from stocked locations to the customer's zone."}}.
7.  Evaluate all collected fulfillment routes (location + shipping option) against the `business_priority`.
    Consider the `customer_tier` from the `processed_order` if the priority is "PRIORITIZE_GOLD_TIER_SPEED" 
    (e.g., gold tier might allow slightly higher cost for significantly faster speed).
    * Valid priorities: "MINIMIZE_COST", "MINIMIZE_DELIVERY_TIME", "MINIMIZE_CO2", "BALANCED_COST_TIME", "PRIORITIZE_GOLD_TIER_SPEED".
8.  Your final output MUST be a single JSON string containing:
    {{
        "recommendation": {{ "fulfillment_location": "...", "carrier": "...", "cost": ..., "delivery_days": ..., "co2_kg": ... }},
        "reasoning": "A clear, concise explanation of why this option was chosen, referencing the priority and key data points.",
        "alternatives_considered": [ {{ "fulfillment_location": "...", "carrier": "...", "cost": ..., "delivery_days": ..., "co2_kg": ...}}, ... ] // 1-2 best viable alternatives
    }}
9.  If no single route can be definitively recommended (e.g., all options have issues), clearly state this in an error JSON as per step 6 or 8.
Do not add any conversational fluff, introductions, or conclusions. Your entire output must be a single, valid JSON string.
""",
    tools=[get_customer_zone, get_inventory, get_shipping_options],
    model=MODEL
)



order_intake_agent = Agent(
    name="OrderIntakeAgent",
    handoff_description="Specialist for validating and enriching raw order data.",
    instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}
You are an AI Order Intake Agent. Your primary responsibility is to receive raw order information,
validate its basic structure, enrich it with customer details using available tools, and then
prepare a structured payload for handoff to the "OrderRoutingDecisionAgent".

Input: You will receive a JSON string containing two top-level keys:
1.  'raw_order': An object with `product_id` (string), `quantity` (positive integer), and `customer_id` (string).
2.  'business_priority': A string indicating the routing priority.

Your Workflow:
1.  Parse the input JSON string to get the 'raw_order' dictionary and the 'business_priority' string.
2.  Validate Raw Order Structure: From the 'raw_order' object, ensure `product_id`, `quantity`,
    and `customer_id` are present and valid (quantity is a positive integer).
    If validation fails, your output MUST be a JSON string: {{"error": "Validation failed: [specific reason for failure]"}}. Do not proceed to handoff.
3.  Enrich with Customer Details: Use the `get_customer_details_tool` with the `customer_id`
    from the 'raw_order' to fetch the customer's name, ZIP code, and tier.
4.  Handle Tool Output from `get_customer_details_tool`:
    * If the tool returns an error (e.g., customer not found, ZIP missing from CRM),
        your output MUST be that error JSON string (the tool already formats it as JSON). Do not proceed to handoff.
    * If successful, it will return customer details as a JSON string. Parse this.
5.  Construct Processed Order: Combine the original valid 'raw_order' information (product_id, quantity, customer_id)
    with the successfully retrieved customer details (customer_name, customer_zip_code, customer_tier)
    to create a `processed_order` dictionary.
    This object MUST include: `product_id`, `quantity`, `customer_id`, `customer_name`,
    `customer_zip_code`, and `customer_tier`.
6.  Prepare Handoff Payload: If all steps were successful, construct a JSON string that will be the input for the "OrderRoutingDecisionAgent".
    This JSON string MUST contain two top-level keys:
    - "processed_order": The `processed_order` dictionary you constructed.
    - "business_priority": The `business_priority` string you received in your initial input.
    Example of the JSON string to prepare: `{{"processed_order": {{...}}, "business_priority": "MINIMIZE_COST"}}`
7.  Handoff: Call the `transfer_to_OrderRoutingDecisionAgent` function. The content of your message just before calling this function
    (i.e., the JSON string prepared in step 6) will be passed as input to the "OrderRoutingDecisionAgent".
    If any prior step resulted in an error (validation, tool call), your final response MUST be ONLY the JSON string
    containing that error message. In this error case, DO NOT call the handoff function.
Do not add any conversational fluff, introductions, or conclusions beyond the required JSON output.
""",
    tools=[get_customer_details_tool],
    handoffs=[order_routing_agent],
    model=MODEL
)

async def main():
    # Restore tracing
    trace_id = gen_trace_id()
    with trace(workflow_name="Order Routing Workflow", trace_id=trace_id):
        print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
        
        # Start with the order intake agent
        raw_order = {"product_id": "product_A", "quantity": 1, "customer_id": "cust123"}
        business_priority = "PRIORITIZE_GOLD_TIER_SPEED"
        
        # Create initial message with both order and priority
        initial_message = json.dumps({
            "raw_order": raw_order,
            "business_priority": business_priority
        })
        
        # Run the conversation with tracing
        logger.info("Starting order processing with intake agent")
        result = await Runner.run(
            starting_agent=order_intake_agent,
            input=initial_message,
            run_config=RunConfig()
        )
        logger.info("Order processing completed")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

