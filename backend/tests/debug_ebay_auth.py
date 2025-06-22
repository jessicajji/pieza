#!/usr/bin/env python3
"""
Debug script for eBay authentication issues using config system.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from app.core.config import settings
import base64


def debug_ebay_auth(env: str):
    """Test eBay OAuth for the given environment ('sandbox' or 'production')."""
    if env == "production":
        client_id = settings.EBAY_CLIENT_ID_PRODUCTION
        client_secret = settings.EBAY_CLIENT_SECRET_PRODUCTION
        token_url = settings.EBAY_TOKEN_URL_PRODUCTION
    else:
        client_id = settings.EBAY_CLIENT_ID_SANDBOX
        client_secret = settings.EBAY_CLIENT_SECRET_SANDBOX
        token_url = settings.EBAY_TOKEN_URL_SANDBOX

    print(f"\n🔍 Testing {env.title()} Credentials:")
    print(f"  Client ID: {client_id[:10]}..." if client_id else "  Client ID: ❌ Not set")
    print(f"  Client Secret: {'*' * 10}..." if client_secret else "  Client Secret: ❌ Not set")
    print(f"  Token URL: {token_url}")

    if not client_id or not client_secret:
        print("❌ Missing credentials in .env file")
        return False

    # Test Base64 encoding
    try:
        credentials = f"{client_id}:{client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        print(f"✅ Base64 encoding successful: {encoded[:20]}...")
    except Exception as e:
        print(f"❌ Base64 encoding failed: {e}")
        return False

    # Test the actual API call
    print("\n🌐 Testing API call...")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded}"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Success! Token: {token_data.get('access_token', '')[:20]}...")
            return True
        else:
            print(f"❌ Error Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 eBay Authentication Debug Tool (Config-based)")
    print("=" * 40)

    prod_success = debug_ebay_auth("production")
    sandbox_success = debug_ebay_auth("sandbox")

    print("\n📋 Summary:")
    if prod_success:
        print("✅ Production credentials work")
    if sandbox_success:
        print("✅ Sandbox credentials work")
    if not prod_success and not sandbox_success:
        print("❌ Both environments failed - check your credentials and .env") 