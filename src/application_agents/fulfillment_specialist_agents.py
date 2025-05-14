import os
import logging
from pydantic import BaseModel
from agents import Agent, handoff

# Assuming MODEL and load_instruction are defined consistently or imported from a shared util
# For now, defining them locally for clarity as done in other agent files.
MODEL = os.getenv("FABRIC_AGENT_MODEL", "gpt-4o-mini") 
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

logger = logging.getLogger(__name__)

def load_instruction(filename):
    prompt_file_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Import tools for this agent
from tools.preorder_backorder_tools import (
    get_product_eta_tool,
    check_alternative_sourcing_tool,
    notify_customer_tool
)

# Pydantic model for handoff payload if more complex data is needed beyond just the query
# For now, reusing AgentQueryInput if the root agent just passes the query string
# from .fabric_intelligence_agents import AgentQueryInput # Or define locally if preferred
class AgentQueryInput(BaseModel): # Defining locally for clarity or if it might diverge
    query: str
    order_id: str | None = None # Optional order_id context for this agent
    sku: str | None = None      # Optional sku context

# --- Specialist Agent Definition: PreorderBackorderAgent ---
preorder_backorder_agent = Agent(
    name="PreorderBackorderAgent",
    handoff_description="Specialist for managing pre-orders and backorders, including ETAs and customer notifications.",
    instructions=load_instruction("preorder_backorder_agent_instructions.md"),
    tools=[
        get_product_eta_tool,
        check_alternative_sourcing_tool,
        notify_customer_tool
    ],
    model=MODEL
)

# --- Handoff Definition for PreorderBackorderAgent ---
# Placeholder on_handoff callback for this agent if needed
async def log_preorder_backorder_handoff(ctx, input_data):
    logger.info(f"Preorder/Backorder Agent Handoff invoked. Context: {ctx}, Input: {input_data}")

handoff_to_preorder_backorder_agent = handoff(
    agent=preorder_backorder_agent,
    tool_name_override="transfer_to_PreorderBackorderAgent",
    tool_description_override="Handoff to the Preorder/Backorder Management Agent for queries about item ETAs, pre-order status, or backorder updates.",
    input_type=AgentQueryInput, # Expects query, and optionally order_id/sku for context
    on_handoff=log_preorder_backorder_handoff
) 