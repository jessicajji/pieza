import logging
from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams

from ..schemas.ebay import EbayItem
from ..schemas.vector_search import VectorSearchResult

logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "furniture_items"
VECTOR_SIZE = 1536  # OpenAI text-embedding-3-small dimension

class VectorDBService:
    """Service for managing vector database operations."""
    
    def __init__(self, host: str = "localhost", port: int = 6333):
        """Initialize the vector database service.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
        """
        self.client = QdrantClient(host=host, port=port)
        self._ensure_collection()
        logger.info("VectorDBService initialized")
    
    def _ensure_collection(self) -> None:
        """Ensure the furniture items collection exists."""
        collections = self.client.get_collections().collections
        collection_names = [collection.name for collection in collections]
        
        if COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {COLLECTION_NAME}")
    
    def add_item(self, item: EbayItem, text_vector: List[float], image_vector: Optional[List[float]] = None) -> None:
        """Add an item to the vector database.
        
        Args:
            item: The eBay item to add
            text_vector: Text embedding vector
            image_vector: Optional image embedding vector
        """
        # Convert item to dict for storage
        item_dict = item.model_dump()
        
        # Store vectors and metadata
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=item.item_id,
                    vector=text_vector,
                    payload=item_dict
                )
            ]
        )
        logger.info(f"Added item to vector database: {item.item_id}")
    
    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        min_score: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar items using vector similarity.
        
        Args:
            query_vector: Query vector to search with
            limit: Maximum number of results to return
            min_score: Minimum similarity score (0-1)
            filters: Optional filters to apply
            
        Returns:
            List of search results with scores
        """
        # Prepare search parameters
        search_params = models.SearchParams(
            hnsw_ef=128,
            exact=False
        )
        
        # Execute search
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            score_threshold=min_score,
            search_params=search_params,
            query_filter=filters
        )
        
        # Convert results to our schema
        search_results = [
            VectorSearchResult(
                item_id=hit.id,
                score=hit.score,
                metadata=hit.payload
            )
            for hit in results
        ]
        
        logger.info(f"Found {len(search_results)} results")
        return search_results
    
    def delete_item(self, item_id: str) -> None:
        """Delete an item from the vector database.
        
        Args:
            item_id: ID of the item to delete
        """
        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.PointIdsList(
                points=[item_id]
            )
        )
        logger.info(f"Deleted item from vector database: {item_id}") 