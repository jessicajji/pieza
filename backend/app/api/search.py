import logging
import os
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.prompt_agent import PromptParsingAgent
from ..services.ebay import MockEbayService
from ..services.embeddings import EmbeddingService
from ..services.vector_db import VectorDBService
from ..schemas.ebay import EbayItem, EbaySearchRequest
from ..schemas.vector_search import VectorSearchRequest, VectorSearchResponse
from ..schemas.prompt import PromptParseResult

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

prompt_agent = PromptParsingAgent(api_key=api_key)
ebay_service = MockEbayService()
embedding_service = EmbeddingService()
vector_db = VectorDBService()

class SearchRequest(BaseModel):
    prompt: str

class SearchResponse(BaseModel):
    items: List[EbayItem]
    total: int
    query: str

def prompt_to_ebay_request(parsed: PromptParseResult) -> EbaySearchRequest:
    """Map PromptParseResult to EbaySearchRequest."""
    return EbaySearchRequest(
        category=parsed.category,
        keywords=parsed.style_keywords or [],
        min_price=None,  # Could be extracted from hard_requirements if present
        max_price=None,  # Could be extracted from hard_requirements if present
        condition=None,  # Could be mapped from style_keywords or hard_requirements
        location=None    # Could be mapped from hard_requirements
    )

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    End-to-end search pipeline:
    1. Parse prompt into structured query
    2. Search eBay for items
    3. Generate embeddings for items
    4. Store items in vector database
    5. Perform vector search
    6. Return top results
    """
    try:
        logger.debug("Starting search pipeline")
        
        # 1. Parse prompt
        logger.debug("Parsing prompt...")
        structured_query = prompt_agent.parse_prompt(request.prompt)
        logger.info(f"Parsed prompt into query: {structured_query}")

        # 2. Map to EbaySearchRequest
        ebay_request = prompt_to_ebay_request(structured_query)
        logger.debug(f"Mapped prompt to eBay request: {ebay_request}")

        # 3. Search eBay
        logger.debug("Searching eBay...")
        ebay_response = await ebay_service.search_items(ebay_request)
        ebay_items = ebay_response.items
        logger.info(f"Found {len(ebay_items)} items from eBay")

        if not ebay_items:
            logger.warning("No items found from eBay")
            return SearchResponse(items=[], total=0, query=request.prompt)

        # 4. Generate embeddings and store in vector DB
        logger.debug("Generating embeddings and storing in vector DB...")
        for i, item in enumerate(ebay_items):
            logger.debug(f"Processing item {i+1}/{len(ebay_items)}")
            try:
                # Generate embeddings
                text_embedding, image_embedding = embedding_service.get_item_embeddings(item)
                logger.debug(f"Generated embeddings for item {item.item_id}")
                
                # Store in vector DB
                vector_db.upsert_item(
                    item_id=item.item_id,
                    text_embedding=text_embedding,
                    image_embedding=image_embedding,
                    metadata=item.dict()
                )
                logger.debug(f"Stored item {item.item_id} in vector DB")
            except Exception as e:
                logger.error(f"Error processing item {item.item_id}: {str(e)}")
                continue

        # 5. Perform vector search
        logger.debug("Performing vector search...")
        vector_request = VectorSearchRequest(
            query=request.prompt,
            limit=5,
            min_score=0.7
        )
        vector_results = vector_db.search(
            query_vector=embedding_service.get_query_embedding(request.prompt),
            limit=vector_request.limit,
            min_score=vector_request.min_score
        )
        logger.info(f"Found {len(vector_results)} results from vector search")

        # 6. Return results
        logger.debug("Preparing response...")
        response = SearchResponse(
            items=[EbayItem(**result.metadata) for result in vector_results],
            total=len(vector_results),
            query=request.prompt
        )
        logger.info("Search pipeline completed successfully")
        return response

    except Exception as e:
        logger.error(f"Error in search pipeline: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 