from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class VectorSearchRequest(BaseModel):
    """Request model for vector search."""
    query: str = Field(..., description="Search query text")
    limit: int = Field(10, description="Maximum number of results to return")
    min_score: float = Field(0.7, description="Minimum similarity score (0-1)")
    filters: Optional[Dict[str, Any]] = Field(None, description="Optional filters to apply")

class VectorSearchResult(BaseModel):
    """Model for a single vector search result."""
    item_id: str = Field(..., description="Unique identifier of the item")
    score: float = Field(..., description="Similarity score (0-1)")
    metadata: Dict[str, Any] = Field(..., description="Item metadata")

class VectorSearchResponse(BaseModel):
    """Response model for vector search."""
    results: List[VectorSearchResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results found")
    query_vector: Optional[List[float]] = Field(None, description="Query vector used for search") 