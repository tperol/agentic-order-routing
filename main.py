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
MODEL = "gpt-4o"

# --- Agent Definitions ---
order_routing_agent = Agent(
    name="OrderRoutingDecisionAgent",
    handoff_description="Specialist agent for determining optimal order fulfillment routes",
    instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}
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
4.  If no stock is found anywhere, your output MUST be a JSON string: {{"error": "No stock available for the product."}}.
5.  For each valid location with stock:
    a. Use `get_shipping_options` to get all shipping options to the customer's zone for the product.
6.  Evaluate all potential fulfillment routes (location + shipping option) against the stated `business_priority`.
    * Valid priorities: "MINIMIZE_COST", "MINIMIZE_DELIVERY_TIME", "MINIMIZE_CO2", "BALANCED_COST_TIME", "PRIORITIZE_GOLD_TIER_SPEED".
    * If "PRIORITIZE_GOLD_TIER_SPEED" and the `customer_tier` in the processed order is "gold", give extra weight to faster options, even if slightly more expensive.
7.  Present your final recommendation as a JSON string. This JSON should contain:
    `recommendation`: {{ "fulfillment_location": "...", "carrier": "...", "cost": ..., "delivery_days": ..., "co2_kg": ... }},
    `reasoning`: "A clear explanation...",
    `alternatives_considered`: [ {{ "fulfillment_location": "...", ...}}, ... ] (1-2 alternatives)
8.  If no suitable route is found after checking options, your output MUST be a JSON string: {{"error": "No suitable shipping options found."}}.

You can engage in a conversation about your decision-making process. When asked about your reasoning,
explain your thought process, the factors you considered, and why you made specific choices.
Do not add any conversational fluff. Your entire output must be a single JSON string.
""",
    tools=[get_customer_zone, get_inventory, get_shipping_options],
    model=MODEL
)



order_intake_agent = Agent(
    name="OrderIntakeAgent",
    handoff_description="Specialist agent for processing and validating incoming orders",
    instructions="""
You are an AI Order Intake Agent. Your primary responsibility is to receive raw order information,
validate its basic structure, enrich it with customer details, and then prepare a structured
'processed_order' JSON object for handoff to the Order Routing Decision Agent named "OrderRoutingDecisionAgent".

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

When you have successfully processed an order, you should hand off to the OrderRoutingDecisionAgent
by including the processed order and the business priority in your response.
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

