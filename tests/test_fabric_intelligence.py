import asyncio
import pytest # Pytest is a common choice for test runners

# Adjust import path based on how tests will be run (e.g., from project root with src in PYTHONPATH)
from main import main_fabric_intelligence

# Test queries are now lists of messages
fabric_intelligence_test_scenarios = [
    {"name": "FI_SC01: Inventory Query", "messages": [{"role": "user", "content": "How much stock of 100084-000012-2 do we have?"}]},
    {"name": "FI_SC02: Order Query", "messages": [{"role": "user", "content": "What is the status of order XYZ789?"}]},
    {"name": "FI_SC03: Ambiguous Query", "messages": [{"role": "user", "content": "Tell me about stuff."}]},
    {"name": "FI_SC04: Greeting", "messages": [{"role": "user", "content": "Hello there!"}]},
    {"name": "FI_SC05: Broad Inventory Query", "messages": [{"role": "user", "content": "Tell me about bookcase inventory"}]},
    {
        "name": "FI_SC06: Follow-up Inventory Query", 
        "messages": [
            {"role": "user", "content": "where is product 100084-000012-2 ?"},
            {"role": "assistant", "content": "Details for SKU 100084-000012-2: Product Name: 3-Shelf Bookcase / Grey / Small Location: Warehouse East Channel: Online Store Status: Low stock Available to Purchase: 130 Available to Backorder: 18 Available to Preorder: 15"},
            {"role": "user", "content": "how many are available to purchase?"}
        ]
    }
]

@pytest.mark.anyio
async def test_fabric_intelligence_scenarios():
    print("\n\n========== RUNNING FABRIC INTELLIGENCE TESTS (via pytest) ==========")
    for i, scenario_data in enumerate(fabric_intelligence_test_scenarios):
        print(f"\n\n<<<<<<<<<< RUNNING FI SCENARIO {i+1}: {scenario_data['name']} >>>>>>>>>>")
        print(f"Input Messages: {scenario_data['messages']}")
        response = await main_fabric_intelligence(scenario_data["messages"])
        print(f"Agent Response: {response}")
        assert "response" in response, f"Scenario {scenario_data['name']} failed to produce a response key"
        if scenario_data["name"] == "FI_SC06: Follow-up Inventory Query":
            assert "130" in response["response"], "Follow-up query did not get the correct availability"
        print("<<<<<<<<<< FI SCENARIO COMPLETE >>>>>>>>>>\n")

# To run these tests, you would typically use the pytest command from your project root directory.
# Example: `PYTHONPATH=src pytest tests/test_fabric_intelligence.py` 