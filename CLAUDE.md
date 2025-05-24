# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-driven order routing system POC that demonstrates intelligent fulfillment decisions using multiple AI agents orchestrated via OpenAI's agents framework.

## Architecture

The system uses a multi-agent architecture:
- **OrderIntakeAgent**: Validates orders and enriches with customer data
- **OrderRoutingDecisionAgent**: Core orchestration agent (OpenAI Assistant) that makes routing decisions
- **Tool-based agents**: InventoryQueryAgent, LogisticsOptionsAgent, CustomerZoneService (implemented as tools)

Key flows:
1. Order intake → Customer validation → Data enrichment
2. Routing decision → Inventory check → Shipping options → Zone assignment
3. Results aggregation → Dashboard display

## Commands

```bash
# Install dependencies (development mode)
pip install -e .

# Run the FastAPI server (main entry point)
python api_server.py

# Run CLI demo
cd src && python -m agentic_order_routing.main

# The project requires these environment variables in .env:
# OPENAI_API_KEY=your_key
# GEMINI_API_KEY=your_key
```

## Key Files and Patterns

- **api_server.py**: FastAPI server with REST endpoints and static file serving
- **main.py**: Core agent orchestration logic using handoff patterns
- **mock_data.py**: All simulated databases (customers, inventory, shipping, zones, products)
- **Tools**: Separate tool modules for intake and routing functionality
- **Prompts**: Markdown instructions for each agent in `prompts/` directory

The codebase uses:
- Async/await patterns throughout
- Pydantic models for data validation
- Agent handoff pattern for delegation between agents
- Tool-based architecture for modularity

## API Endpoints

- `GET /`: Serves the operator dashboard
- `POST /optimize-route`: Main order processing endpoint
- `GET /contextual-data`: Returns mock database information for debugging