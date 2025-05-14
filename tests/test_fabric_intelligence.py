import asyncio
import pytest # Pytest is a common choice for test runners

# Adjust import path based on how tests will be run (e.g., from project root with src in PYTHONPATH)
from main import main_fabric_intelligence

# Test queries are now lists of messages
fabric_intelligence_test_scenarios = [
    {"name": "FI_SC01: Inventory Query", "messages": [{"role": "user", "content": "How much stock of 100084-000012-2 do we have?"}]},
    {"name": "FI_SC02: Order Query", "messages": [{"role": "user", "content": "What is the status of order 7201122334455?"}]},
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
    },
    {
        "name": "FI_SC07: Preorder ETA Query",
        "messages": [{"role": "user", "content": "What is the ETA for SKU S007-SOFA-GRN?"}]
    },
    {
        "name": "FI_SC08: Backorder Query with Order Context",
        "messages": [{"role": "user", "content": "My order 6110822858950 has item 420081-000015-2 which is on preorder, can you update me?"}]
    },
    {
        "name": "FI_SC09: Notify customer about backorder",
        "messages": [{"role": "user", "content": "Please notify customer for order 8302233445566 about the backordered item GEN011-SHE-0123 and give them an ETA."}]
    }
]

@pytest.mark.anyio
async def test_fabric_intelligence_scenarios():
    print("\n\n========== RUNNING FABRIC INTELLIGENCE TESTS (via pytest) ==========")
    for i, scenario_data in enumerate(fabric_intelligence_test_scenarios):
        print(f"\n\n<<<<<<<<<< RUNNING FI SCENARIO {i+1}: {scenario_data['name']} >>>>>>>>>>")
        print(f"Input Messages: {scenario_data['messages']}")
        response_data = await main_fabric_intelligence(scenario_data["messages"])
        print(f"Agent Response: {response_data}")
        assert "response" in response_data, f"Scenario {scenario_data['name']} failed to produce a response key"
        actual_response_text = response_data["response"].lower()

        if scenario_data["name"] == "FI_SC02: Order Query":
            assert "status of order 7201122334455" in actual_response_text or "shipped" in actual_response_text or "alice wonderland" in actual_response_text, "FI_SC02 did not return expected order info for 7201122334455"
        if scenario_data["name"] == "FI_SC06: Follow-up Inventory Query":
            assert "130" in actual_response_text, "Follow-up query for FI_SC06 did not get the correct availability"
        if scenario_data["name"] == "FI_SC07: Preorder ETA Query":
            assert "s007-sofa-grn" in actual_response_text, "FI_SC07 did not mention the SKU S007-SOFA-GRN"
            assert ("eta" in actual_response_text or "estimated time of arrival" in actual_response_text or "estimated restock" in actual_response_text), "FI_SC07 did not contain ETA keywords"
            assert "2025-07-28" in actual_response_text, "FI_SC07 ETA date missing or incorrect"
        if scenario_data["name"] == "FI_SC09: Notify customer about backorder":
            assert "notified" in actual_response_text and ("customer" in actual_response_text or "successfully" in actual_response_text), "FI_SC09 agent response did not confirm notification as expected"
        print("<<<<<<<<<< FI SCENARIO COMPLETE >>>>>>>>>>\n")

# To run these tests, you would typically use the pytest command from your project root directory.
# Example: `PYTHONPATH=src pytest tests/test_fabric_intelligence.py` 