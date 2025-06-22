#!/usr/bin/env python3
"""
Test script for eBay API integration.
Run this to verify that our authentication and search functionality works.
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ebay_auth():
    """Test eBay authentication service."""
    try:
        from app.services.ebay_auth import ebay_auth_service
        
        logger.info("Testing eBay authentication...")
        token = ebay_auth_service.get_access_token()
        logger.info(f"✅ Successfully obtained access token: {token[:20]}...")
        return True
        
    except Exception as e:
        logger.error(f"❌ Authentication failed: {e}")
        return False

def test_ebay_search():
    """Test eBay search functionality."""
    try:
        from app.services.ebay_api import ebay_api_service
        
        logger.info("Testing eBay search...")
        
        # Test a simple search
        search_query = "modern sofa"
        logger.info(f"Searching for: '{search_query}'")
        
        response = ebay_api_service.search_items_by_keyword(search_query, limit=5)
        
        logger.info(f"✅ Search successful! Found {len(response.items)} items out of {response.total} total")
        
        # Display first few results
        for i, item in enumerate(response.items[:3]):
            logger.info(f"  {i+1}. {item.title} - ${item.price} ({item.condition})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🧪 Starting eBay API integration tests...")
    
    # Test authentication
    auth_success = test_ebay_auth()
    
    if not auth_success:
        logger.error("❌ Authentication test failed. Cannot proceed with search test.")
        return
    
    # Test search
    search_success = test_ebay_search()
    
    if auth_success and search_success:
        logger.info("🎉 All tests passed! eBay API integration is working correctly.")
    else:
        logger.error("❌ Some tests failed. Please check the configuration and try again.")

if __name__ == "__main__":
    main() 