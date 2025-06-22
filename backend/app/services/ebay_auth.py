import requests
import base64
import time
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class EbayAuthService:
    """
    Service for managing eBay application-level OAuth tokens.
    """
    _access_token: Optional[str] = None
    _token_expiry_time: int = 0
    
    def _is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired."""
        # Consider token invalid if it's within 60 seconds of expiry
        return self._access_token is not None and time.time() < self._token_expiry_time - 60

    def _get_new_token(self) -> None:
        """Fetch a new application access token from eBay."""
        client_id = settings.ebay_client_id
        client_secret = settings.ebay_client_secret

        if not client_id or not client_secret:
            logger.error("eBay client ID or client secret is not configured.")
            raise ValueError("Missing eBay API credentials.")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
        }
        body = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
        
        try:
            logger.info(f"Requesting new eBay application access token from {settings.ebay_token_url}")
            response = requests.post(settings.ebay_token_url, headers=headers, data=body)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            self._access_token = data["access_token"]
            # Set expiry time with a small buffer
            self._token_expiry_time = time.time() + data["expires_in"]
            logger.info("Successfully obtained new eBay application access token.")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching eBay access token: {e}")
            self._access_token = None
            self._token_expiry_time = 0
            raise

    def get_access_token(self) -> str:
        """
        Get a valid application access token, refreshing if necessary.
        """
        if not self._is_token_valid():
            self._get_new_token()
        
        if self._access_token is None:
            raise Exception("Failed to retrieve eBay access token.")
            
        return self._access_token

# Create a singleton instance of the service
ebay_auth_service = EbayAuthService() 