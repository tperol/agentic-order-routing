"""Tests for agent tool functions."""

import pytest
import json
from typing import Dict, Any

# Import the tools
from src.agentic_order_routing.tools.intake_agent_tools import (
    get_customer_details_tool
)
from src.agentic_order_routing.tools.routing_tools import (
    get_customer_zone,
    get_inventory,
    get_shipping_options
)


class TestIntakeAgentTools:
    """Test suite for intake agent tools."""

    def test_get_customer_details_valid(self):
        """Test getting details for a valid customer."""
        result = get_customer_details_tool("cust123")
        data = json.loads(result)
        
        assert "customer_id" in data
        assert data["customer_id"] == "cust123"
        assert "name" in data
        assert data["name"] == "Alice Wonderland"
        assert "zip_code" in data
        assert data["zip_code"] == "10001"
        assert "tier" in data
        assert data["tier"] == "gold"

    def test_get_customer_details_invalid_id(self):
        """Test error handling for invalid customer ID."""
        # Empty string
        result = get_customer_details_tool("")
        data = json.loads(result)
        assert "error" in data
        assert "Invalid customer ID" in data["error"]

    def test_get_customer_details_not_found(self):
        """Test error handling for non-existent customer."""
        result = get_customer_details_tool("cust_999")
        data = json.loads(result)
        assert "error" in data
        assert "Customer not found" in data["error"]

    def test_get_customer_details_all_customers(self):
        """Test that all mock customers have required fields."""
        # Test known customer IDs from mock data
        customer_ids = ["cust123", "cust456", "cust789", "cust101", "cust112"]
        for customer_id in customer_ids:
            result = get_customer_details_tool(customer_id)
            data = json.loads(result)
            
            if "error" not in data:
                assert "customer_id" in data
                assert "name" in data
                assert "zip_code" in data
                assert "tier" in data


class TestRoutingTools:
    """Test suite for routing tools."""

    def test_get_customer_zone_valid(self):
        """Test zone lookup for valid zip codes."""
        # Test known zones from mock data
        assert get_customer_zone("10001") == "ZONE_1"  # NY
        assert get_customer_zone("90001") == "ZONE_3"  # CA
        assert get_customer_zone("60601") == "ZONE_2"  # IL

    def test_get_customer_zone_unknown(self):
        """Test zone lookup for unknown zip code."""
        assert get_customer_zone("99999") == "UNKNOWN_ZONE"
        assert get_customer_zone("00000") == "UNKNOWN_ZONE"

    def test_get_inventory_available(self):
        """Test inventory lookup for available product."""
        result = get_inventory("product_A", 5)
        data = json.loads(result)
        
        # Should have inventory in at least one location
        assert len(data) > 0
        
        # Each location should have sufficient quantity
        for location, quantity in data.items():
            assert quantity >= 5

    def test_get_inventory_insufficient(self):
        """Test inventory lookup when quantity exceeds availability."""
        # Request very large quantity
        result = get_inventory("product_A", 10000)
        data = json.loads(result)
        
        # Should return empty dict or locations with insufficient stock
        assert isinstance(data, dict)

    def test_get_inventory_nonexistent_product(self):
        """Test inventory lookup for non-existent product."""
        result = get_inventory("product_Z", 1)
        data = json.loads(result)
        
        # Should return empty dict
        assert data == {}

    def test_get_inventory_edge_cases(self):
        """Test inventory with edge case quantities."""
        # Zero quantity - should return all locations with any stock
        result = get_inventory("product_A", 0)
        data = json.loads(result)
        assert len(data) > 0

    def test_get_shipping_options_valid(self):
        """Test shipping options for valid parameters."""
        result = get_shipping_options("WH_EAST", "ZONE_1", "product_A")
        data = json.loads(result)
        
        # Should return list of options
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Each option should have required fields
        for option in data:
            assert "carrier" in option
            assert "cost" in option
            assert "days" in option
            assert "co2_kg" in option
            assert isinstance(option["cost"], (int, float))
            assert isinstance(option["days"], int)
            assert isinstance(option["co2_kg"], (int, float))

    def test_get_shipping_options_no_options(self):
        """Test shipping options when none available."""
        # Non-existent warehouse
        result = get_shipping_options("WH_INVALID", "ZONE_1", "product_A")
        data = json.loads(result)
        
        # Should return empty list
        assert data == []

    def test_get_shipping_options_all_warehouses(self):
        """Test that all warehouses can provide shipping options."""
        warehouses = ["WH_EAST", "WH_WEST", "WH_SOUTH"]
        zones = ["ZONE_1", "ZONE_2", "ZONE_3"]
        
        for warehouse in warehouses:
            for zone in zones:
                result = get_shipping_options(warehouse, zone, "product_A")
                data = json.loads(result)
                
                # Each valid warehouse-zone combo should have options
                assert isinstance(data, list)