"""Tests for mock data integrity and structure."""

import pytest
from typing import Dict, List, Any

from src.agentic_order_routing.mock_data import (
    MOCK_CRM_DB as CUSTOMERS,
    INVENTORY_DB as INVENTORY,
    SHIPPING_OPTIONS_DB as SHIPPING_OPTIONS,
    PRODUCT_WEIGHT_DB as PRODUCTS,
    ZIP_TO_ZONE_DB as ZONE_ASSIGNMENTS
)


class TestMockDataIntegrity:
    """Test suite for validating mock data structure and content."""

    def test_customers_structure(self):
        """Test that all customers have required fields."""
        assert len(CUSTOMERS) > 0
        
        for customer_id, customer in CUSTOMERS.items():
            assert isinstance(customer_id, str)
            assert customer_id.startswith("cust")
            
            # Required fields
            assert "name" in customer
            assert "zip_code" in customer
            assert "tier" in customer
            
            # Validate tier values
            assert customer["tier"] in ["gold", "silver", "bronze"]

    def test_products_structure(self):
        """Test that all products have weight data."""
        assert len(PRODUCTS) > 0
        
        for product_id, weight in PRODUCTS.items():
            assert isinstance(product_id, str)
            assert product_id.startswith("product_")
            
            # Validate weight is numeric and positive
            assert isinstance(weight, (int, float))
            assert weight > 0

    def test_inventory_structure(self):
        """Test that inventory data is properly structured."""
        assert len(INVENTORY) > 0
        
        for location_id, products in INVENTORY.items():
            assert isinstance(location_id, str)
            assert location_id.startswith(("WH_", "STORE_"))
            assert isinstance(products, dict)
            
            for product_id, quantity in products.items():
                assert isinstance(product_id, str)
                assert product_id.startswith("product_")
                assert isinstance(quantity, int)
                assert quantity >= 0
                
                # Product should exist in PRODUCTS
                assert product_id in PRODUCTS

    def test_shipping_options_structure(self):
        """Test that shipping options are properly structured."""
        assert len(SHIPPING_OPTIONS) > 0
        
        for location_id, zones in SHIPPING_OPTIONS.items():
            assert isinstance(location_id, str)
            assert location_id.startswith(("WH_", "STORE_"))
            assert isinstance(zones, dict)
            
            for zone_id, options in zones.items():
                assert isinstance(zone_id, str)
                assert zone_id.startswith("ZONE_")
                assert isinstance(options, list)
                assert len(options) > 0
                
                for option in options:
                    # Each option is a tuple: (product_id, carrier, cost, days, co2_kg)
                    assert isinstance(option, tuple)
                    assert len(option) == 5
                    
                    product_id, carrier, cost, days, co2_kg = option
                    assert isinstance(product_id, str)
                    assert product_id.startswith("product_")
                    assert isinstance(carrier, str)
                    assert isinstance(cost, (int, float))
                    assert cost > 0
                    assert isinstance(days, int)
                    assert days > 0
                    assert isinstance(co2_kg, (int, float))
                    assert co2_kg >= 0

    def test_zone_assignments_structure(self):
        """Test that zone assignments are properly structured."""
        assert len(ZONE_ASSIGNMENTS) > 0
        
        for zip_code, zone in ZONE_ASSIGNMENTS.items():
            assert isinstance(zip_code, str)
            assert len(zip_code) == 5  # US ZIP codes
            assert zip_code.isdigit()
            
            assert isinstance(zone, str)
            assert zone.startswith("ZONE_")

    def test_data_consistency(self):
        """Test consistency across different data structures."""
        # All products in inventory should exist in PRODUCTS
        for location, products in INVENTORY.items():
            for product_id in products:
                assert product_id in PRODUCTS, f"Product {product_id} in inventory but not in PRODUCTS"
        
        # All customer zip codes should have zone assignments
        for customer_id, customer in CUSTOMERS.items():
            if "zip_code" in customer and customer["zip_code"]:
                zip_code = customer["zip_code"]
                # Check if zip code is in zone assignments or use default
                if zip_code not in ZONE_ASSIGNMENTS:
                    assert "UNKNOWN_ZIP_DEFAULT" in ZONE_ASSIGNMENTS

    def test_inventory_coverage(self):
        """Test that key products are available in multiple locations."""
        # Check that product_A (frequently used in tests) exists in multiple locations
        locations_with_product_A = [
            loc for loc, products in INVENTORY.items() 
            if "product_A" in products and products["product_A"] > 0
        ]
        
        assert len(locations_with_product_A) >= 2, "product_A should be available in at least 2 locations"

    def test_shipping_options_coverage(self):
        """Test that all warehouse-zone combinations have shipping options."""
        warehouses = set(SHIPPING_OPTIONS.keys())
        zones = set()
        
        # Extract zones from shipping options
        for location_id, zone_options in SHIPPING_OPTIONS.items():
            zones.update(zone_options.keys())
        
        # Verify we have options for multiple combinations
        assert len(warehouses) >= 3, "Should have at least 3 warehouses"
        assert len(zones) >= 3, "Should have at least 3 zones"