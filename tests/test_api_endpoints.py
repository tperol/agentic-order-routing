"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


class TestAPIEndpoints:
    """Test suite for API endpoints."""

    def test_dashboard_serving(self, test_client: TestClient):
        """Test that the dashboard is served correctly."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_optimize_route_valid_order(
        self, test_client: TestClient, sample_order: Dict[str, Any]
    ):
        """Test optimize route endpoint with valid order."""
        response = test_client.post("/optimize-route", json=sample_order)
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "success"
        assert "result" in data
        
        # Verify result structure
        result = data["result"]
        assert "order_id" in result
        assert result["order_id"] == sample_order["orderId"]

    def test_optimize_route_invalid_customer(
        self, test_client: TestClient, invalid_order: Dict[str, Any]
    ):
        """Test optimize route endpoint with invalid customer."""
        response = test_client.post("/optimize-route", json=invalid_order)
        
        # The endpoint should still return 200 but with error in result
        assert response.status_code == 200
        data = response.json()
        
        # Check if error is properly handled
        if data["status"] == "error":
            assert "error" in data
        else:
            # Or check if the result contains validation failure
            result = data["result"]
            assert "customer_validation" in result
            assert not result["customer_validation"].get("is_valid", True)

    def test_optimize_route_missing_fields(self, test_client: TestClient):
        """Test optimize route endpoint with missing required fields."""
        incomplete_order = {
            "orderId": "TEST-003"
            # Missing customerId and items
        }
        
        response = test_client.post("/optimize-route", json=incomplete_order)
        # Should handle gracefully, either with 422 or 200 with error
        assert response.status_code in [200, 422]

    def test_contextual_data_response(
        self, test_client: TestClient, expected_contextual_data: Dict[str, Any]
    ):
        """Test contextual data endpoint returns correct structure."""
        response = test_client.get("/contextual-data")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify all expected keys are present
        for key, expected_type in expected_contextual_data.items():
            assert key in data
            assert isinstance(data[key], expected_type)
        
        # Verify inventory aggregation
        if "inventory" in data:
            inventory = data["inventory"]
            assert "total_products" in inventory
            assert "warehouses" in inventory
            assert isinstance(inventory["total_products"], int)
            assert isinstance(inventory["warehouses"], list)

    def test_contextual_data_counts(self, test_client: TestClient):
        """Test that contextual data contains expected counts."""
        response = test_client.get("/contextual-data")
        assert response.status_code == 200
        
        data = response.json()
        
        # Verify we have data in each category
        assert len(data.get("customers", [])) > 0
        assert len(data.get("products", [])) > 0
        assert len(data.get("shipping_options", [])) > 0
        assert data.get("inventory", {}).get("total_products", 0) > 0

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, test_client: TestClient, sample_order: Dict[str, Any]):
        """Test that the API can handle concurrent requests."""
        import asyncio
        import httpx
        
        async def make_request():
            async with httpx.AsyncClient(app=test_client.app, base_url="http://test") as client:
                response = await client.post("/optimize-route", json=sample_order)
                return response
        
        # Make 5 concurrent requests
        tasks = [make_request() for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200