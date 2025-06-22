import logging
from typing import List, Optional, Dict, Any
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType
import os

from ..schemas.ebay import EbayItem
from ..schemas.vector_search import VectorSearchResult

logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "furniture_items"
VECTOR_SIZE = 1536  # OpenAI text-embedding-3-small dimension

class VectorDBService:
    """Service for managing vector database operations."""
    
    def __init__(self):
        """Initialize the vector database service.
        
        Args:
            host: Qdrant server host
            port: Qdrant server port
        """ 
        self.client = QdrantClient(
            url=os.getenv('QDRANT_URL'),
            api_key=os.getenv("QDRANT_API_KEY")
        )
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
        """Add an item to the vector database, deduping by vendor and vector_item_id."""
        # Convert item to dict for storage
        item_dict = item.model_dump()
        vendor = "EBAY"
        try:
            vector_item_id = int(item.item_id)
        except Exception:
            vector_item_id = hash(item.item_id)
        # Check for existing item with same vendor and vector_item_id
        existing = self.client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(key="vendor", match=models.MatchValue(value=vendor)),
                    models.FieldCondition(key="vector_item_id", match=models.MatchValue(value=vector_item_id)),
                ]
            )
        )[0]
        if existing:
            logger.info(f"Duplicate found for vendor={vendor}, vector_item_id={vector_item_id}, skipping add.")
            return
        # Generate a UUID for internal tracking
        internal_id = str(uuid.uuid4())
        # Add internal ID, vendor, and vector_item_id to metadata
        item_dict["internal_id"] = internal_id
        item_dict["vendor"] = vendor
        item_dict["vector_item_id"] = vector_item_id
        # Store vectors and metadata
        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=internal_id,
                    vector=text_vector,
                    payload=item_dict
                )
            ]
        )
        logger.info(f"Added item to vector database: {item.item_id} (internal_id: {internal_id})")
    
    def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        min_score: float = 0.7,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar items using vector similarity, deduping by (vendor, vector_item_id)."""
        logger.debug(f"Starting vector search with limit={limit}, min_score={min_score}")
        logger.debug(f"Query vector length: {len(query_vector)}")
        search_params = models.SearchParams(
            hnsw_ef=128,
            exact=False
        )
        try:
            results = self.client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=limit * 3,  # get more to allow for deduplication
                score_threshold=min_score,
                search_params=search_params,
                query_filter=filters
            )
            logger.debug(f"Raw search results count: {len(results)}")
            # Deduplicate by (vendor, vector_item_id)
            seen = set()
            deduped = []
            for hit in results:
                vendor = hit.payload.get("vendor")
                vector_item_id = hit.payload.get("vector_item_id")
                key = (vendor, vector_item_id)
                if key in seen:
                    continue
                seen.add(key)
                deduped.append(hit)
                if len(deduped) >= limit:
                    break
            search_results = [
                VectorSearchResult(
                    item_id=hit.payload.get("internal_id"),
                    vendor=hit.payload.get("vendor"),
                    vector_item_id=hit.payload.get("vector_item_id"),
                    score=hit.score,
                    metadata=hit.payload
                )
                for hit in deduped
            ]
            logger.info(f"Found {len(search_results)} results (deduped)")
            return search_results
        except Exception as e:
            logger.error(f"Error during vector search: {str(e)}", exc_info=True)
            raise
    
    def delete_by_vendor(self, vendor_id: str) -> None:
        """Delete all items for a specific vendor."""
        logger.info(f"Attempting to delete all items for vendor_id: {vendor_id}")
        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="vendor",
                            match=models.MatchValue(value=vendor_id)
                        )
                    ]
                )
            )
        )
        logger.info(f"Successfully submitted deletion request for vendor_id: {vendor_id}")

    def delete_item(self, item_id: str) -> None:
        """Delete an item from the vector database.
        
        Args:
            item_id: ID of the item to delete
        """
        # First find the internal ID for this eBay item
        search_results = self.client.scroll(
            collection_name=COLLECTION_NAME,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="item_id",
                        match=models.MatchValue(value=item_id)
                    )
                ]
            )
        )[0]
        
        if search_results:
            internal_id = search_results[0].id
            self.client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=models.PointIdsList(
                    points=[internal_id]
                )
            )
            logger.info(f"Deleted item from vector database: {item_id} (internal_id: {internal_id})")
        else:
            logger.warning(f"Item not found in vector database: {item_id}")
    
    def clear(self) -> None:
        """Delete all points in the collection."""
        self.client.delete(collection_name=COLLECTION_NAME, points_selector=models.PointIdsList(points=[]))
        logger.info(f"Cleared all points from collection: {COLLECTION_NAME}")

    def create_payload_index(self, field_name: str, field_schema: PayloadSchemaType) -> None:
        """Create a payload index for a specific field in the collection."""
        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name=field_name,
            field_schema=field_schema
        )
        logger.info(f"Created payload index for field: {field_name} with schema: {field_schema}")

    def create_vector_item_id_index(self) -> None:
        """Create a payload index for the vector_item_id field in the collection."""
        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="vector_item_id",
            field_schema=PayloadSchemaType.INTEGER
        )
        logger.info("Created payload index for vector_item_id") 