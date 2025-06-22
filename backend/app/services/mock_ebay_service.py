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
            ),
            EbayItem(
                item_id="7",
                title="Scandinavian Minimalist Sofa",
                price=850.00,
                condition="New",
                location="Portland, OR",
                image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4",
                item_url="https://ebay.com/itm/7",
                shipping_cost=60.00,
                seller_rating=99.1
            ),
            EbayItem(
                item_id="8",
                title="Industrial Reclaimed Wood Coffee Table",
                price=320.00,
                condition="Used - Good",
                location="Brooklyn, NY",
                image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                item_url="https://ebay.com/itm/8",
                shipping_cost=45.00,
                seller_rating=97.8
            ),
            EbayItem(
                item_id="9",
                title="Mid-Century Walnut Sideboard",
                price=1200.00,
                condition="New",
                location="Austin, TX",
                image_url="https://images.unsplash.com/photo-1465101046530-73398c7f28ca",
                item_url="https://ebay.com/itm/9",
                shipping_cost=80.00,
                seller_rating=98.7
            ),
            EbayItem(
                item_id="10",
                title="Modern Tufted Velvet Armchair",
                price=410.00,
                condition="New",
                location="Chicago, IL",
                image_url="https://images.unsplash.com/photo-1515378791036-0648a3ef77b2",
                item_url="https://ebay.com/itm/10",
                shipping_cost=35.00,
                seller_rating=99.0
            ),
            EbayItem(
                item_id="11",
                title="Bohemian Rattan Lounge Chair",
                price=275.00,
                condition="Used - Like New",
                location="Santa Barbara, CA",
                image_url="https://images.unsplash.com/photo-1503389152951-9c3d8b6e9c94",
                item_url="https://ebay.com/itm/11",
                shipping_cost=30.00,
                seller_rating=98.2
            ),
            EbayItem(
                item_id="12",
                title="Contemporary Glass Dining Table",
                price=950.00,
                condition="New",
                location="Miami, FL",
                image_url="https://images.unsplash.com/photo-1468436139062-f60a71c5c892",
                item_url="https://ebay.com/itm/12",
                shipping_cost=90.00,
                seller_rating=99.3
            ),
            EbayItem(
                item_id="13",
                title="Classic Leather Chesterfield Sofa",
                price=1800.00,
                condition="Used - Excellent",
                location="Boston, MA",
                image_url="https://images.unsplash.com/photo-1519125323398-675f0ddb6308",
                item_url="https://ebay.com/itm/13",
                shipping_cost=120.00,
                seller_rating=97.9
            ),
            EbayItem(
                item_id="14",
                title="Farmhouse Pine Dining Bench",
                price=220.00,
                condition="New",
                location="Nashville, TN",
                image_url="https://images.unsplash.com/photo-1465101178521-c1a9136a3b99",
                item_url="https://ebay.com/itm/14",
                shipping_cost=40.00,
                seller_rating=98.6
            ),
            EbayItem(
                item_id="15",
                title="Art Deco Mirrored Bar Cart",
                price=540.00,
                condition="New",
                location="Las Vegas, NV",
                image_url="https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
                item_url="https://ebay.com/itm/15",
                shipping_cost=55.00,
                seller_rating=99.4
            ),
            EbayItem(
                item_id="16",
                title="Vintage Oak Bookshelf",
                price=330.00,
                condition="Used - Good",
                location="Denver, CO",
                image_url="https://images.unsplash.com/photo-1465101046530-73398c7f28ca",
                item_url="https://ebay.com/itm/16",
                shipping_cost=50.00,
                seller_rating=97.5
            ),
            EbayItem(
                item_id="17",
                title="Modern Modular Sectional Sofa",
                price=2100.00,
                condition="New",
                location="Seattle, WA",
                image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4",
                item_url="https://ebay.com/itm/17",
                shipping_cost=150.00,
                seller_rating=99.7
            ),
            EbayItem(
                item_id="18",
                title="Minimalist White Lacquer Nightstand",
                price=180.00,
                condition="New",
                location="San Diego, CA",
                image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                item_url="https://ebay.com/itm/18",
                shipping_cost=25.00,
                seller_rating=98.8
            ),
            EbayItem(
                item_id="19",
                title="Industrial Metal Bar Stools (Set of 2)",
                price=160.00,
                condition="New",
                location="Houston, TX",
                image_url="https://images.unsplash.com/photo-1515378791036-0648a3ef77b2",
                item_url="https://ebay.com/itm/19",
                shipping_cost=35.00,
                seller_rating=99.2
            ),
            EbayItem(
                item_id="20",
                title="French Provincial Carved Dresser",
                price=950.00,
                condition="Used - Excellent",
                location="New Orleans, LA",
                image_url="https://images.unsplash.com/photo-1468436139062-f60a71c5c892",
                item_url="https://ebay.com/itm/20",
                shipping_cost=85.00,
                seller_rating=98.1
            ),
            EbayItem(
                item_id="21",
                title="Modern Glass and Chrome Coffee Table",
                price=420.00,
                condition="New",
                location="Los Angeles, CA",
                image_url="https://images.unsplash.com/photo-1503389152951-9c3d8b6e9c94",
                item_url="https://ebay.com/itm/21",
                shipping_cost=40.00,
                seller_rating=99.0
            ),
            EbayItem(
                item_id="22",
                title="Rustic Live Edge Walnut Desk",
                price=1100.00,
                condition="New",
                location="Boulder, CO",
                image_url="https://images.unsplash.com/photo-1519125323398-675f0ddb6308",
                item_url="https://ebay.com/itm/22",
                shipping_cost=70.00,
                seller_rating=98.7
            ),
            EbayItem(
                item_id="23",
                title="Contemporary Tufted King Bed Frame",
                price=1300.00,
                condition="New",
                location="Dallas, TX",
                image_url="https://images.unsplash.com/photo-1465101178521-c1a9136a3b99",
                item_url="https://ebay.com/itm/23",
                shipping_cost=100.00,
                seller_rating=99.5
            ),
            EbayItem(
                item_id="24",
                title="Mid-Century Modern Walnut Coffee Table",
                price=600.00,
                condition="Used - Good",
                location="San Francisco, CA",
                image_url="https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
                item_url="https://ebay.com/itm/24",
                shipping_cost=45.00,
                seller_rating=98.3
            ),
            EbayItem(
                item_id="25",
                title="Classic Mahogany Dining Table",
                price=1400.00,
                condition="Used - Excellent",
                location="Philadelphia, PA",
                image_url="https://images.unsplash.com/photo-1465101046530-73398c7f28ca",
                item_url="https://ebay.com/itm/25",
                shipping_cost=90.00,
                seller_rating=97.6
            ),
            EbayItem(
                item_id="26",
                title="Modern Velvet Swivel Chair",
                price=350.00,
                condition="New",
                location="Atlanta, GA",
                image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4",
                item_url="https://ebay.com/itm/26",
                shipping_cost=30.00,
                seller_rating=99.1
            ),
            EbayItem(
                item_id="27",
                title="Industrial Pipe Bookshelf",
                price=290.00,
                condition="New",
                location="Detroit, MI",
                image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb",
                item_url="https://ebay.com/itm/27",
                shipping_cost=35.00,
                seller_rating=98.4
            ),
            EbayItem(
                item_id="28",
                title="Scandinavian Oak Dining Chairs (Set of 4)",
                price=780.00,
                condition="New",
                location="Minneapolis, MN",
                image_url="https://images.unsplash.com/photo-1515378791036-0648a3ef77b2",
                item_url="https://ebay.com/itm/28",
                shipping_cost=60.00,
                seller_rating=99.3
            ),
            EbayItem(
                item_id="29",
                title="Boho Woven Storage Ottoman",
                price=210.00,
                condition="New",
                location="Phoenix, AZ",
                image_url="https://images.unsplash.com/photo-1468436139062-f60a71c5c892",
                item_url="https://ebay.com/itm/29",
                shipping_cost=25.00,
                seller_rating=98.9
            ),
            EbayItem(
                item_id="30",
                title="Modern Glass Console Table",
                price=480.00,
                condition="New",
                location="San Jose, CA",
                image_url="https://images.unsplash.com/photo-1503389152951-9c3d8b6e9c94",
                item_url="https://ebay.com/itm/30",
                shipping_cost=40.00,
                seller_rating=99.2
            ),
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