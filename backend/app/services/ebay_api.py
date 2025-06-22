import requests
import logging
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode

from .ebay_auth import ebay_auth_service
from ..schemas.ebay import EbayItem, EbaySearchRequest, EbaySearchResponse
from ..core.config import settings

logger = logging.getLogger(__name__)

class EbayAPIService:
    """
    Service for making calls to the eBay Browse API.
    Uses application-level OAuth tokens for authentication.
    """
    
    SEARCH_ENDPOINT = "/buy/browse/v1/item_summary/search"
    
    def __init__(self):
        self.auth_service = ebay_auth_service
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests including authorization."""
        return {
            "Authorization": f"Bearer {self.auth_service.get_access_token()}",
            "Content-Type": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY-US"  # US marketplace
        }
    
    def _transform_ebay_item(self, item_data: Dict[str, Any]) -> EbayItem:
        """Transform eBay API response item to our EbayItem schema."""
        # Extract price information
        price_data = item_data.get("price", {})
        price = float(price_data.get("value", "0")) if price_data.get("value") else 0.0
        
        # Extract shipping cost
        shipping_options = item_data.get("shippingOptions", [])
        shipping_cost = 0.0
        if shipping_options:
            shipping_cost_data = shipping_options[0].get("shippingCost", {})
            shipping_cost = float(shipping_cost_data.get("value", "0")) if shipping_cost_data.get("value") else 0.0
        
        # Extract seller information
        seller_data = item_data.get("seller", {})
        seller_rating = float(seller_data.get("feedbackPercentage", "0")) if seller_data.get("feedbackPercentage") else 0.0
        
        # Extract location
        location_data = item_data.get("location", {})
        location_parts = []
        if location_data.get("city"):
            location_parts.append(location_data["city"])
        if location_data.get("stateOrProvince"):
            location_parts.append(location_data["stateOrProvince"])
        if location_data.get("country"):
            location_parts.append(location_data["country"])
        location = ", ".join(location_parts) if location_parts else "Unknown"
        
        # Extract image URL
        image_data = item_data.get("image", {})
        image_url = image_data.get("imageUrl", "") if image_data else ""
        
        return EbayItem(
            item_id=item_data.get("itemId", ""),
            title=item_data.get("title", ""),
            price=price,
            condition=item_data.get("condition", "Unknown"),
            location=location,
            image_url=image_url,
            item_url=item_data.get("itemWebUrl", ""),
            shipping_cost=shipping_cost,
            seller_rating=seller_rating
        )
    
    def search_items_by_keyword(self, query: str, limit: int = 50, offset: int = 0) -> EbaySearchResponse:
        """
        Search for items on eBay using keywords.
        
        Args:
            query: Search query string
            limit: Number of items to return (max 200)
            offset: Number of items to skip for pagination
            
        Returns:
            EbaySearchResponse with search results
        """
        try:
            # Build query parameters
            params = {
                "q": query,
                "limit": min(limit, 200),  # eBay max is 200
                "offset": offset
            }
            
            url = f"{settings.ebay_base_url}{self.SEARCH_ENDPOINT}?{urlencode(params)}"
            headers = self._get_headers()
            
            logger.info(f"Searching eBay for: '{query}' (limit: {limit}, offset: {offset})")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Transform the response
            items = []
            for item_data in data.get("itemSummaries", []):
                try:
                    item = self._transform_ebay_item(item_data)
                    items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to transform item {item_data.get('itemId', 'unknown')}: {e}")
                    continue
            
            total = data.get("total", 0)
            
            logger.info(f"Found {len(items)} items out of {total} total for query: '{query}'")
            
            return EbaySearchResponse(
                items=items,
                total=total,
                limit=limit,
                offset=offset
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching eBay API: {e}")
            raise Exception(f"Failed to search eBay: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in search_items_by_keyword: {e}")
            raise
    
    def search_items_by_category(self, category_id: str, limit: int = 50, offset: int = 0) -> EbaySearchResponse:
        """
        Search for items in a specific eBay category.
        
        Args:
            category_id: eBay category ID
            limit: Number of items to return (max 200)
            offset: Number of items to skip for pagination
            
        Returns:
            EbaySearchResponse with search results
        """
        try:
            # Build query parameters
            params = {
                "category_ids": category_id,
                "limit": min(limit, 200),
                "offset": offset
            }
            
            url = f"{settings.ebay_base_url}{self.SEARCH_ENDPOINT}?{urlencode(params)}"
            headers = self._get_headers()
            
            logger.info(f"Searching eBay category {category_id} (limit: {limit}, offset: {offset})")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Transform the response (same as keyword search)
            items = []
            for item_data in data.get("itemSummaries", []):
                try:
                    item = self._transform_ebay_item(item_data)
                    items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to transform item {item_data.get('itemId', 'unknown')}: {e}")
                    continue
            
            total = data.get("total", 0)
            
            logger.info(f"Found {len(items)} items out of {total} total in category {category_id}")
            
            return EbaySearchResponse(
                items=items,
                total=total,
                limit=limit,
                offset=offset
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching eBay category API: {e}")
            raise Exception(f"Failed to search eBay category: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in search_items_by_category: {e}")
            raise

# Create a singleton instance
ebay_api_service = EbayAPIService() 