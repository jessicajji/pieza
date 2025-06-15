from typing import List, Optional
from pydantic import BaseModel, Field

class EbayItem(BaseModel):
    """Schema for a single eBay item."""
    item_id: str = Field(..., description="eBay item ID")
    title: str = Field(..., description="Item title")
    price: float = Field(..., description="Item price in USD")
    currency: str = Field(default="USD", description="Currency code")
    condition: str = Field(..., description="Item condition")
    location: str = Field(..., description="Item location")
    image_url: str = Field(..., description="URL to item image")
    item_url: str = Field(..., description="URL to eBay listing")
    shipping_cost: Optional[float] = Field(None, description="Shipping cost in USD")
    seller_rating: float = Field(..., description="Seller's rating (0-100)")

class EbaySearchRequest(BaseModel):
    """Schema for eBay search request."""
    category: str = Field(..., description="Furniture category")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    min_price: Optional[float] = Field(None, description="Minimum price")
    max_price: Optional[float] = Field(None, description="Maximum price")
    condition: Optional[str] = Field(None, description="Item condition")
    location: Optional[str] = Field(None, description="Preferred location")

class EbaySearchResponse(BaseModel):
    """Schema for eBay search response."""
    items: List[EbayItem] = Field(..., description="List of matching items")
    total_results: int = Field(..., description="Total number of results")
    page: int = Field(..., description="Current page number")
    total_pages: int = Field(..., description="Total number of pages") 