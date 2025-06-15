import logging
from typing import List, Optional
from ..schemas.ebay import EbayItem, EbaySearchRequest, EbaySearchResponse

logger = logging.getLogger(__name__)

class MockEbayService:
    """Mock implementation of eBay Finding API service."""
    
    def __init__(self):
        # Sample furniture data with real images
        self._mock_items = [
            EbayItem(
                item_id="1",
                title="Modern Velvet Sofa with Wood Legs",
                price=599.99,
                condition="New",
                location="New York, NY",
                image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc",
                item_url="https://ebay.com/itm/1",
                shipping_cost=49.99,
                seller_rating=98.5
            ),
            EbayItem(
                item_id="2",
                title="Contemporary Fabric Sofa - 70\" Wide",
                price=799.99,
                condition="New",
                location="Los Angeles, CA",
                image_url="https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e",
                item_url="https://ebay.com/itm/2",
                shipping_cost=59.99,
                seller_rating=99.2
            ),
            EbayItem(
                item_id="3",
                title="Vintage Wood Frame Sofa",
                price=299.99,
                condition="Used - Like New",
                location="Chicago, IL",
                image_url="https://images.unsplash.com/photo-1567016432779-094069958ea5",
                item_url="https://ebay.com/itm/3",
                shipping_cost=89.99,
                seller_rating=97.8
            ),
            EbayItem(
                item_id="4",
                title="Mid-Century Modern Sofa with Tapered Legs",
                price=899.99,
                condition="New",
                location="San Francisco, CA",
                image_url="https://images.unsplash.com/photo-1550254478-ead40cc54513",
                item_url="https://ebay.com/itm/4",
                shipping_cost=69.99,
                seller_rating=99.5
            ),
            EbayItem(
                item_id="5",
                title="Sectional Sofa with Ottoman",
                price=1299.99,
                condition="New",
                location="Miami, FL",
                image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
                item_url="https://ebay.com/itm/5",
                shipping_cost=99.99,
                seller_rating=98.9
            ),
            EbayItem(
                item_id="6",
                title="Convertible Sleeper Sofa",
                price=699.99,
                condition="New",
                location="Seattle, WA",
                image_url="https://images.unsplash.com/photo-1567016376408-0226e4d0c1ea",
                item_url="https://ebay.com/itm/6",
                shipping_cost=79.99,
                seller_rating=97.5
            )
        ]

    async def search_items(self, request: EbaySearchRequest) -> EbaySearchResponse:
        """
        Mock search implementation that filters items based on request parameters.
        In the real implementation, this would call the eBay Finding API.
        """
        logger.info(f"Searching eBay items with request: {request}")
        
        # Filter items based on request parameters
        filtered_items = self._mock_items
        
        if request.category:
            filtered_items = [item for item in filtered_items 
                            if request.category.lower() in item.title.lower()]
        
        if request.keywords:
            filtered_items = [item for item in filtered_items 
                            if any(kw.lower() in item.title.lower() 
                                 for kw in request.keywords)]
        
        if request.min_price is not None:
            filtered_items = [item for item in filtered_items 
                            if item.price >= request.min_price]
        
        if request.max_price is not None:
            filtered_items = [item for item in filtered_items 
                            if item.price <= request.max_price]
        
        if request.condition:
            filtered_items = [item for item in filtered_items 
                            if request.condition.lower() in item.condition.lower()]
        
        if request.location:
            filtered_items = [item for item in filtered_items 
                            if request.location.lower() in item.location.lower()]

        # Simulate pagination
        page = 1
        items_per_page = 10
        total_results = len(filtered_items)
        total_pages = (total_results + items_per_page - 1) // items_per_page
        
        # In a real implementation, we would paginate the results
        # For the mock, we'll just return all filtered items
        return EbaySearchResponse(
            items=filtered_items,
            total_results=total_results,
            page=page,
            total_pages=total_pages
        ) 