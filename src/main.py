# Main orchestrator for the Agentic AI Order Routing POC.

import os
import json
import asyncio
import logging
from dotenv import load_dotenv

from agents import Agent, Runner, gen_trace_id, trace, RunConfig, handoff

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import specific agents (starting points for workflows)
from application_agents.fabric_intelligence_agents import fabric_intelligence_root_agent
from application_agents.order_processing_agents import order_intake_agent # For the order processing workflow

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def main_order_processing(raw_order=None, business_priority=None):
    trace_id = gen_trace_id()
    with trace(workflow_name="Order Routing Workflow", trace_id=trace_id):
        print(f"View trace for Order Routing: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
        
        if raw_order is None:
            raw_order = {"product_id": "product_A", "quantity": 1, "customer_id": "cust123"}
        if business_priority is None:
            business_priority = "PRIORITIZE_GOLD_TIER_SPEED"
        
        initial_message = json.dumps({
            "raw_order": raw_order,
            "business_priority": business_priority
        })
        
        logger.info("Starting order processing with intake agent")
        result = await Runner.run(
            starting_agent=order_intake_agent, 
            input=initial_message,
            run_config=RunConfig()
        )
        logger.info("Order processing completed")
        logger.info(f"Final result from order processing: {result.final_output}")
        if not result.final_output:
            return {"error": "No recommendation produced by order processing agent."}
        try:
            parsed = result.final_output
            if isinstance(parsed, str):
                parsed = json.loads(parsed)
            if not isinstance(parsed, dict):
                return {"error": "Order processing agent did not return a valid dict."}
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse order processing agent output: {e}")
            return {"error": f"Failed to parse order processing agent output: {e}"}

async def main_fabric_intelligence(messages: list):
    """Runs a user query (now a list of messages) through the FabricIntelligenceRootAgent."""
    if not messages or not isinstance(messages, list) or len(messages) == 0:
        return {"error": "Messages list must be a non-empty list."}
    
    # Ensure messages are in the correct format if needed, or assume library handles it.
    # The library expects a list of dicts with "role" and "content".

    trace_id = gen_trace_id()
    with trace(workflow_name="Fabric Intelligence Workflow", trace_id=trace_id):
        print(f"View trace for Fabric Intelligence: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

        logger.info(f"Starting Fabric Intelligence query processing with messages: {messages}")
        result = await Runner.run(
            starting_agent=fabric_intelligence_root_agent,
            input=messages, # Pass the list of messages as input
            run_config=RunConfig()
        )
        logger.info("Fabric Intelligence query processing completed")
        final_output = result.final_output if result.final_output else "No specific response generated."
        logger.info(f"Final result from Fabric Intelligence: {final_output}")
        
        return {"response": final_output}

# The if __name__ == "__main__" block for direct test execution was moved to tests/ directory. 