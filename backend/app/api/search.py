import logging
import os
from typing import List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..services.prompt_agent import PromptParsingAgent
from ..services.ebay_api import ebay_api_service
from ..services.embeddings import EmbeddingService
from ..services.vector_db import VectorDBService
from ..schemas.ebay import EbayItem, EbaySearchRequest, EbaySearchResponse
from ..schemas.vector_search import VectorSearchRequest, VectorSearchResponse
from ..schemas.prompt import PromptParseResult

# Configure logging
logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

prompt_agent = PromptParsingAgent(api_key=api_key)
embedding_service = EmbeddingService()
vector_db = VectorDBService()

class SearchRequest(BaseModel):
    prompt: str

class SearchResponse(BaseModel):
    items: List[EbayItem]
    total: int
    query: str

def prompt_to_ebay_query(parsed: PromptParseResult) -> str:
    """Convert PromptParseResult to a search query string for eBay."""
    # Combine category and style keywords into a search query
    query_parts = []
    
    if parsed.category:
        query_parts.append(parsed.category)
    
    if parsed.style_keywords:
        query_parts.extend(parsed.style_keywords)
    
    # If no specific keywords, use a general furniture search
    if not query_parts:
        query_parts.append("furniture")
    
    return " ".join(query_parts)

@router.get("/ebay/search")
async def search_ebay_direct(
    q: str = Query(..., description="Search query"),
    limit: int = Query(50, ge=1, le=200, description="Number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip")
) -> EbaySearchResponse:
    """
    Direct eBay search endpoint for testing and direct access.
    """
    try:
        logger.info(f"Direct eBay search for: '{q}' (limit: {limit}, offset: {offset})")
        
        response = ebay_api_service.search_items_by_keyword(
            query=q,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Found {len(response.items)} items out of {response.total} total")
        return response
        
    except Exception as e:
        logger.error(f"Error searching eBay: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"eBay search failed: {str(e)}")

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    End-to-end search pipeline:
    1. Parse prompt into structured query
    2. Search eBay for items using real API
    3. Generate embeddings for items
    4. Store items in vector database
    5. Perform vector search
    6. Return top results
    """
    try:
        logger.debug(f"Starting search pipeline with prompt: {request.prompt}")
        
        # 1. Parse prompt
        logger.debug("Parsing prompt...")
        structured_query = prompt_agent.parse_prompt(request.prompt)
        logger.info(f"Parsed prompt into query: {structured_query}")

        # 2. Convert to eBay search query
        ebay_query = prompt_to_ebay_query(structured_query)
        logger.debug(f"Converted prompt to eBay query: '{ebay_query}'")

        # 3. Search eBay using real API
        logger.debug("Searching eBay with real API...")
        ebay_response = ebay_api_service.search_items_by_keyword(
            query=ebay_query,
            limit=50,  # Get more items for better vector search results
            offset=0
        )
        ebay_items = ebay_response.items
        logger.info(f"Found {len(ebay_items)} items from eBay")

        if not ebay_items:
            logger.warning("No items found from eBay")
            return SearchResponse(items=[], total=0, query=request.prompt)

        # 4. Generate embeddings and store in vector DB
        logger.debug("Generating embeddings and storing in vector DB...")
        for i, item in enumerate(ebay_items):
            logger.debug(f"Processing item {i+1}/{len(ebay_items)}: {item.title}")
            try:
                # Generate embeddings
                text_embedding, image_embedding = embedding_service.get_item_embeddings(item)
                logger.debug(f"Generated embeddings for item {item.item_id}")
                
                # Store in vector DB
                vector_db.add_item(
                    item=item,
                    text_vector=text_embedding,
                    image_vector=image_embedding
                )
                logger.debug(f"Stored item {item.item_id} in vector DB")
            except Exception as e:
                logger.error(f"Error processing item {item.item_id}: {str(e)}", exc_info=True)
                continue

        # 5. Perform vector search
        logger.debug("Performing vector search...")
        vector_request = VectorSearchRequest(
            query=request.prompt,
            limit=5,
            min_score=0.5
        )
        query_embedding = embedding_service.get_query_embedding(request.prompt)
        logger.debug(f"Generated query embedding with length: {len(query_embedding)}")
        
        vector_results = vector_db.search(
            query_vector=query_embedding,
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