#!/usr/bin/env python3
"""
Test script for eBay search integration.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import json

def test_ebay_search_direct():
    """Test the direct eBay search endpoint."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Direct eBay Search...")
    try:
        response = requests.get(
            f"{base_url}/api/ebay/search",
            params={
                "q": "vintage chair",
                "limit": 5,
                "offset": 0
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('items', []))} items")
            print(f"Total available: {data.get('total', 0)}")
            
            # Show first item details
            if data.get('items'):
                first_item = data['items'][0]
                print(f"\n📦 First item:")
                print(f"  Title: {first_item.get('title', 'N/A')}")
                print(f"  Price: ${first_item.get('price', 0):.2f}")
                print(f"  Condition: {first_item.get('condition', 'N/A')}")
                print(f"  Location: {first_item.get('location', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_main_search_pipeline():
    """Test the main search pipeline that uses real eBay API."""
    base_url = "http://localhost:8000"
    
    print("\n🔍 Testing Main Search Pipeline (with real eBay)...")
    try:
        response = requests.post(
            f"{base_url}/api/search",
            json={
                "prompt": "I need a vintage wooden chair for my dining room"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data.get('items', []))} items")
            print(f"Total: {data.get('total', 0)}")
            print(f"Query: {data.get('query', 'N/A')}")
            
            # Show first item details
            if data.get('items'):
                first_item = data['items'][0]
                print(f"\n📦 First item:")
                print(f"  Title: {first_item.get('title', 'N/A')}")
                print(f"  Price: ${first_item.get('price', 0):.2f}")
                print(f"  Condition: {first_item.get('condition', 'N/A')}")
                print(f"  Location: {first_item.get('location', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 eBay Search Integration Test")
    print("=" * 40)
    
    test_ebay_search_direct()
    test_main_search_pipeline()
    
    print("\n✅ Test completed!") 