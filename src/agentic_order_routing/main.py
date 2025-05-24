"""Main orchestrator for the Agentic AI Order Routing POC."""


import os
import json
import asyncio
import logging
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace, RunConfig, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.handoffs import Handoff
from pydantic import BaseModel


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import tools for each assistant
from agentic_order_routing.tools.intake_agent_tools import (
    get_customer_details_tool
)
from agentic_order_routing.tools.routing_tools import (
    get_customer_zone, get_inventory, get_shipping_options
)

# --- Load Environment Variables and Model ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gpt-4o-mini"

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_instruction_from_file(filename: str) -> str:
    """Load instruction content from a file in the prompts directory."""
    prompt_file_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Pydantic model for handoff payload ---
class ProcessedOrderModel(BaseModel):
    product_id: str
    quantity: int
    customer_id: str
    customer_name: str
    customer_zip_code: str
    customer_tier: str

class OrderRoutingPayloadModel(BaseModel):
    processed_order: ProcessedOrderModel
    business_priority: str

# --- Handoff callback ---
async def on_handoff(ctx, input_data):
    """Handle handoff to OrderRoutingDecisionAgent."""
    logger.info(
        f"Handoff to OrderRoutingDecisionAgent invoked with input: {input_data}"
    )

# --- Agent Definitions ---
order_routing_agent = Agent(
    name="OrderRoutingDecisionAgent",
    handoff_description=(
        "Specialist agent for determining optimal order fulfillment routes"
    ),
    instructions=load_instruction_from_file(
        "order_routing_decision_agent_instructions.md"
    ),
    tools=[get_customer_zone, get_inventory, get_shipping_options],
    model=MODEL
)

order_routing_handoff = handoff(
    agent=order_routing_agent,
    tool_name_override="transfer_to_OrderRoutingDecisionAgent",
    tool_description_override=(
        "Handoff to the Order Routing Decision Agent with validated order payload."
    ),
    input_type=OrderRoutingPayloadModel,
    on_handoff=on_handoff
)

order_intake_agent = Agent(
    name="OrderIntakeAgent",
    handoff_description="Specialist for validating and enriching raw order data.",
    instructions=load_instruction_from_file("order_intake_agent_instructions.md"),
    tools=[get_customer_details_tool],
    handoffs=[order_routing_handoff],
    model=MODEL
)

async def main(raw_order=None, business_priority=None) -> dict:
    # Restore tracing
    trace_id = gen_trace_id()
    with trace(workflow_name="Order Routing Workflow", trace_id=trace_id):
        print(
            f"View trace: https://platform.openai.com/traces/trace?"
            f"trace_id={trace_id}\n"
        )
        
        # Use defaults if not provided
        if raw_order is None:
            raw_order = {
                "product_id": "product_A", 
                "quantity": 1, 
                "customer_id": "cust123"
            }
        if business_priority is None:
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
        logger.info(f"Final result from main: {result.final_output}")
        # Ensure we always return a valid dict
        if not result.final_output:
            return {"error": "No recommendation produced by agent."}
        try:
            parsed = result.final_output
            # If the agent returned a string, try to parse as JSON
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
            if not isinstance(parsed, dict):
                return {"error": "Agent did not return a valid dict."}
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse agent output: {e}")
            return {"error": f"Failed to parse agent output: {e}"}

if __name__ == "__main__":
    # Example Test Scenarios
    test_scenarios = [
        {
            "name": "SC01: Gold Tier Speed (Valid)", 
            "raw_order": {
                "product_id": "product_A", 
                "quantity": 1, 
                "customer_id": "cust123"
            }, 
            "priority": "PRIORITIZE_GOLD_TIER_SPEED"
        },
        {
            "name": "SC02: Minimize Cost (Valid)", 
            "raw_order": {
                "product_id": "product_D", 
                "quantity": 2, 
                "customer_id": "cust456"
            }, 
            "priority": "MINIMIZE_COST"
        },
        {
            "name": "SC03: Minimize CO2 (Valid)", 
            "raw_order": {
                "product_id": "product_A", 
                "quantity": 1, 
                "customer_id": "cust789"
            }, 
            "priority": "MINIMIZE_CO2"
        },
        {
            "name": "SC04: Balanced (Valid)", 
            "raw_order": {
                "product_id": "product_B", 
                "quantity": 1, 
                "customer_id": "cust101"
            }, 
            "priority": "BALANCED_COST_TIME"
        },
        {
            "name": "SC05: Intake - Invalid Customer ID", 
            "raw_order": {
                "product_id": "product_A", 
                "quantity": 1, 
                "customer_id": "cust_INVALID"
            }, 
            "priority": "MINIMIZE_COST"
        },
        {
            "name": "SC06: Routing - No Stock (High Qty)", 
            "raw_order": {
                "product_id": "product_C", 
                "quantity": 100, 
                "customer_id": "cust123"
            }, 
            "priority": "MINIMIZE_COST"
        },
        {
            "name": "SC07: Intake - Invalid Quantity", 
            "raw_order": {
                "product_id": "product_A", 
                "quantity": -1, 
                "customer_id": "cust123"
            }, 
            "priority": "MINIMIZE_COST"
        },
        {
            "name": "SC08: Intake - Missing Raw Order Key (product_id)", 
            "raw_order": {
                "quantity": 1, 
                "customer_id": "cust123"
            }, 
            "priority": "MINIMIZE_COST"
        },
        {
            "name": "SC09: Routing - No Shipping Options", 
            "raw_order": {
                "product_id": "product_C", 
                "quantity": 1, 
                "customer_id": "cust789"
            }, 
            "priority": "MINIMIZE_COST"
        },
    ]

    async def run_all_tests() -> None:
        """Run all test scenarios."""
        for i, scenario_data in enumerate(test_scenarios):
            print(
                f"\n\n<<<<<<<<<< RUNNING SCENARIO {i+1}: "
                f"{scenario_data['name']} >>>>>>>>>>"
            )
            await main(scenario_data["raw_order"], scenario_data["priority"])
            print("<<<<<<<<<< SCENARIO COMPLETE >>>>>>>>>>\n")

    asyncio.run(run_all_tests())    

