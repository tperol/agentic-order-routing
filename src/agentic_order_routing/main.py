# Main orchestrator for the Agentic AI Order Routing POC.


import os
import json
from pathlib import Path
import asyncio
import logging
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace, RunConfig
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import tools for each assistant
from agentic_order_routing.tools.intake_agent_tools import get_customer_details_tool
from agentic_order_routing.tools.routing_tools import get_customer_zone, get_inventory, get_shipping_options

# --- Load Environment Variables and Model ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gpt-4o"

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_instruction_from_file(filename):
    prompt_file_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Agent Definitions ---
order_routing_agent = Agent(
    name="OrderRoutingDecisionAgent",
    handoff_description="Specialist agent for determining optimal order fulfillment routes",
    instructions=load_instruction_from_file("order_routing_decision_agent_instructions.md"),
    tools=[get_customer_zone, get_inventory, get_shipping_options],
    model=MODEL
)

order_intake_agent = Agent(
    name="OrderIntakeAgent",
    handoff_description="Specialist for validating and enriching raw order data.",
    instructions=load_instruction_from_file("order_intake_agent_instructions.md"),
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

    # # Example Test Scenarios
    # test_scenarios = [
    #     {"name": "SC01: Gold Tier Speed (Valid)", "raw_order": {"product_id": "product_A", "quantity": 1, "customer_id": "cust123"}, "priority": "PRIORITIZE_GOLD_TIER_SPEED"},
    #     {"name": "SC02: Minimize Cost (Valid)", "raw_order": {"product_id": "product_D", "quantity": 2, "customer_id": "cust456"}, "priority": "MINIMIZE_COST"},
    #     {"name": "SC03: Minimize CO2 (Valid)", "raw_order": {"product_id": "product_A", "quantity": 1, "customer_id": "cust789"}, "priority": "MINIMIZE_CO2"},
    #     {"name": "SC04: Balanced (Valid)", "raw_order": {"product_id": "product_B", "quantity": 1, "customer_id": "cust101"}, "priority": "BALANCED_COST_TIME"},
    #     {"name": "SC05: Intake - Invalid Customer ID", "raw_order": {"product_id": "product_A", "quantity": 1, "customer_id": "cust_INVALID"}, "priority": "MINIMIZE_COST"},
    #     {"name": "SC06: Routing - No Stock (High Qty)", "raw_order": {"product_id": "product_C", "quantity": 100, "customer_id": "cust123"}, "priority": "MINIMIZE_COST"},
    #     {"name": "SC07: Intake - Invalid Quantity", "raw_order": {"product_id": "product_A", "quantity": -1, "customer_id": "cust123"}, "priority": "MINIMIZE_COST"},
    #     {"name": "SC08: Intake - Missing Raw Order Key (product_id)", "raw_order": {"quantity": 1, "customer_id": "cust123"}, "priority": "MINIMIZE_COST"},
    #     {"name": "SC09: Routing - No Shipping Options", "raw_order": {"product_id": "product_C", "quantity": 1, "customer_id": "cust789"}, "priority": "MINIMIZE_COST"}, # cust789 is ZONE_1
    # ]

    # async def run_all_tests():
    #     for i, scenario_data in enumerate(test_scenarios):
    #         print(f"\n\n<<<<<<<<<< RUNNING SCENARIO {i+1}: {scenario_data['name']} >>>>>>>>>>")
    #         await main(scenario_data["raw_order"], scenario_data["priority"])
    #         print("<<<<<<<<<< SCENARIO COMPLETE >>>>>>>>>>\n")

    # asyncio.run(run_all_tests())    

