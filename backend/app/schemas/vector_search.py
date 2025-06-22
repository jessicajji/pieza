from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class Vendor(str, Enum):
    EBAY = "EBAY"
    # Add more vendors as needed

class VectorSearchRequest(BaseModel):
    """Request model for vector search."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(10, description="Maximum number of results to return")
    min_score: float = Field(0.7, description="Minimum similarity score (0-1)")
    filters: Optional[Dict[str, Any]] = Field(None, description="Optional filters to apply")

class VectorSearchResult(BaseModel):
    """Model for a single vector search result."""
    item_id: str = Field(..., description="UUID for this vector DB entry")
    vendor: Vendor = Field(..., description="Vendor source (e.g., EBAY)")
    vector_item_id: int = Field(..., description="Vendor's item ID as int")
    score: float = Field(..., description="Similarity score (0-1)")
    metadata: Dict[str, Any] = Field(..., description="Item metadata")

class VectorSearchResponse(BaseModel):
    """Response model for vector search."""
    results: List[VectorSearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results found")
    query_vector: Optional[List[float]] = Field(None, description="Query vector used for search") 