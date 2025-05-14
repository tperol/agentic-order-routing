import os
import logging
from pydantic import BaseModel
from agents import Agent, handoff, RunConfig # Assuming RunConfig might be needed here eventually

# Import tools for these agents
from tools.intake_agent_tools import get_customer_details_tool
from tools.routing_tools import get_customer_zone, get_inventory, get_shipping_options

logger = logging.getLogger(__name__) 

# --- PROMPTS_DIR and load_instruction_from_file (local to this module) ---
# Assumes prompts are in src/prompts/ and this file is in src/application_agents/
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
MODEL = os.getenv("FABRIC_AGENT_MODEL", "gpt-4o-mini") # Consistent model usage

def load_instruction_from_file(filename):
    prompt_file_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Pydantic model for handoff payload --- (Moved from main.py)
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

# --- Handoff callback --- (Moved from main.py)
async def on_order_routing_handoff(ctx, input_data):
    logger.info(f"Handoff to OrderRoutingDecisionAgent invoked with input: {input_data}")

# --- Agent Definitions --- (Moved from main.py)
order_routing_agent = Agent(
    name="OrderRoutingDecisionAgent",
    handoff_description="Specialist agent for determining optimal order fulfillment routes",
    instructions=load_instruction_from_file("order_routing_decision_agent_instructions.md"),
    tools=[get_customer_zone, get_inventory, get_shipping_options],
    model=MODEL
)

order_routing_handoff = handoff(
    agent=order_routing_agent,
    tool_name_override="transfer_to_OrderRoutingDecisionAgent",
    tool_description_override="Handoff to the Order Routing Decision Agent with validated order payload.",
    input_type=OrderRoutingPayloadModel,
    on_handoff=on_order_routing_handoff # Using the renamed callback
)

order_intake_agent = Agent(
    name="OrderIntakeAgent",
    handoff_description="Specialist for validating and enriching raw order data.",
    instructions=load_instruction_from_file("order_intake_agent_instructions.md"),
    tools=[get_customer_details_tool],
    handoffs=[order_routing_handoff],
    model=MODEL
) 