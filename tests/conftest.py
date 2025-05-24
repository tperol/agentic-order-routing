"""Pytest configuration and fixtures for test suite."""

import pytest
import asyncio
from typing import AsyncGenerator, Dict, Any
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api_server import app


@pytest.fixture
def test_client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_order() -> Dict[str, Any]:
    """Sample order data for testing."""
    return {
        "orderId": "TEST-001",
        "customerId": "cust123",  # Alice Wonderland
        "items": [
            {
                "productId": "product_A",
                "quantity": 2
            }
        ],
        "shippingAddress": "123 Main St, New York, NY 10001"
    }


@pytest.fixture
def invalid_order() -> Dict[str, Any]:
    """Invalid order data for testing error handling."""
    return {
        "orderId": "TEST-002",
        "customerId": "cust999",
        "items": [
            {
                "productId": "product_Z",
                "quantity": 1
            }
        ],
        "shippingAddress": "Invalid Address"
    }


@pytest.fixture
def expected_contextual_data() -> Dict[str, Any]:
    """Expected structure for contextual data endpoint."""
    return {
        "customers": list,
        "products": list,
        "inventory": dict,
        "shipping_options": list,
        "zone_assignments": dict
    }


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_agent_response() -> Dict[str, Any]:
    """Mock response from the order routing agent."""
    return {
        "order_id": "TEST-001",
        "customer_validation": {
            "is_valid": True,
            "customer_id": "cust123",
            "name": "Alice Wonderland",
            "vip_status": True
        },
        "routing_decision": {
            "fulfillment_center": "WH_EAST",
            "zone": "ZONE_1",
            "shipping_method": "CarrierY_Exp",
            "estimated_delivery": "2025-05-26"
        },
        "inventory_check": {
            "all_items_available": True,
            "items": [
                {
                    "product_id": "product_A",
                    "available": True,
                    "warehouse": "WH_EAST"
                }
            ]
        }
    }