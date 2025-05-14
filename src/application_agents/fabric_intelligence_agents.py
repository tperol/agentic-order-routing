import os
from agents import Agent, handoff # This should now refer to the external library
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

MODEL = os.getenv("FABRIC_AGENT_MODEL", "gpt-4o-mini")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

def load_instruction(filename):
    prompt_file_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

from tools.inventory_agent_tools import get_inventory_details_for_sku, get_overall_stock_for_product
from tools.order_agent_tools import get_order_status_by_id, find_orders_for_customer

class AgentQueryInput(BaseModel):
    query: str

async def log_fi_handoff(ctx, input_data):
    logger.info(f"Fabric Intelligence Handoff invoked. Context: {ctx}, Input: {input_data}")

inventory_agent = Agent(
    name="InventoryAgent",
    handoff_description="Specialist agent for answering questions about product inventory.",
    instructions=load_instruction("inventory_agent_instructions.md"),
    tools=[get_inventory_details_for_sku, get_overall_stock_for_product],
    model=MODEL
)

order_agent = Agent(
    name="OrderAgent",
    handoff_description="Specialist agent for answering questions about customer orders.",
    instructions=load_instruction("order_agent_instructions.md"),
    tools=[get_order_status_by_id, find_orders_for_customer],
    model=MODEL
)

handoff_to_inventory_agent = handoff(
    agent=inventory_agent,
    tool_name_override="transfer_to_InventoryAgent",
    tool_description_override="Handoff to the InventoryAgent for inventory-related queries.",
    input_type=AgentQueryInput,
    on_handoff=log_fi_handoff
)

handoff_to_order_agent = handoff(
    agent=order_agent,
    tool_name_override="transfer_to_OrderAgent",
    tool_description_override="Handoff to the OrderAgent for order-related queries.",
    input_type=AgentQueryInput,
    on_handoff=log_fi_handoff
)

fabric_intelligence_root_agent = Agent(
    name="FabricIntelligenceRootAgent",
    instructions=load_instruction("fabric_intelligence_root_agent_instructions.md"),
    tools=[], 
    handoffs=[handoff_to_inventory_agent, handoff_to_order_agent],
    model=MODEL
) 