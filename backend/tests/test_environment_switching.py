#!/usr/bin/env python3
"""
Test script to verify eBay environment switching functionality.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.services.ebay_auth import EbayAuthService
from app.services.ebay_api import EbayAPIService

def test_environment_configuration():
    """Test that environment configuration is working correctly."""
    print("=== Testing eBay Environment Configuration ===\n")
    
    # Test current environment
    print(f"Current EBAY_ENVIRONMENT: {settings.EBAY_ENVIRONMENT}")
    print(f"Using sandbox credentials: {settings.EBAY_ENVIRONMENT != 'production'}")
    
    # Test credential selection
    print(f"\nCredential Selection:")
    print(f"  Client ID: {settings.ebay_client_id[:10]}..." if settings.ebay_client_id else "  Client ID: None")
    print(f"  Client Secret: {'*' * 10}..." if settings.ebay_client_secret else "  Client Secret: None")
    
    # Test URL selection
    print(f"\nURL Selection:")
    print(f"  Token URL: {settings.ebay_token_url}")
    print(f"  Base URL: {settings.ebay_base_url}")
    
    # Test auth service
    auth_service = EbayAuthService()
    print(f"\nAuth Service Test:")
    print(f"  Using token URL: {settings.ebay_token_url}")
    
    # Test API service
    api_service = EbayAPIService()
    print(f"\nAPI Service Test:")
    print(f"  Using base URL: {settings.ebay_base_url}")
    print(f"  Search URL: {settings.ebay_base_url}{api_service.SEARCH_ENDPOINT}")
    
    # Test environment-specific URLs
    print(f"\nEnvironment-Specific URLs:")
    print(f"  Sandbox Token URL: {settings.EBAY_TOKEN_URL_SANDBOX}")
    print(f"  Sandbox Base URL: {settings.EBAY_BASE_URL_SANDBOX}")
    print(f"  Production Token URL: {settings.EBAY_TOKEN_URL_PRODUCTION}")
    print(f"  Production Base URL: {settings.EBAY_BASE_URL_PRODUCTION}")
    
    print(f"\n=== Environment Configuration Test Complete ===")

if __name__ == "__main__":
    test_environment_configuration() 