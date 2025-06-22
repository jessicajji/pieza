#!/usr/bin/env python3
"""
Bulk import script for eBay furniture items with batch embedding generation.
Fetches items from eBay and adds them to the vector database in batches.
"""

import asyncio
import logging
import sys
from typing import List, Dict, Any
import time

# Add the backend directory to the path
sys.path.append('.')

from app.services.ebay_api import ebay_api_service
from app.services.vector_db import vector_db_service
from app.schemas.ebay import EbayItem
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BulkEbayImporter:
    """Bulk importer for eBay furniture items."""
    
    def __init__(self):
        self.ebay_service = ebay_api_service
        self.vector_service = vector_db_service
        self.batch_size = 50  # Process items in batches of 50
        self.max_items = 1000  # Maximum items to import (adjust as needed)
        
    def get_furniture_categories(self) -> List[str]:
        """Get eBay category IDs for furniture."""
        # eBay furniture category IDs
        return [
            "11700",  # Antiques
            "162912",  # Furniture
            "38219",   # Home & Garden > Furniture
            "63514",   # Home & Garden > Furniture > Chairs
            "63515",   # Home & Garden > Furniture > Tables
            "63516",   # Home & Garden > Furniture > Beds
            "63517",   # Home & Garden > Furniture > Storage
            "63518",   # Home & Garden > Furniture > Living Room
            "63519",   # Home & Garden > Furniture > Dining Room
            "63520",   # Home & Garden > Furniture > Bedroom
            "63521",   # Home & Garden > Furniture > Office
        ]
    
    def get_search_keywords(self) -> List[str]:
        """Get furniture search keywords."""
        return [
            "chair", "table", "desk", "bed", "sofa", "couch", "dresser", "cabinet",
            "bookshelf", "nightstand", "dining table", "coffee table", "end table",
            "armchair", "recliner", "ottoman", "bench", "stool", "wardrobe",
            "vintage chair", "antique table", "modern sofa", "wooden desk",
            "leather chair", "fabric sofa", "metal table", "glass table",
            "dining chair", "office chair", "gaming chair", "accent chair"
        ]
    
    async def fetch_items_from_ebay(self, keyword: str, limit: int = 200) -> List[EbayItem]:
        """Fetch items from eBay for a given keyword."""
        try:
            logger.info(f"Fetching items for keyword: '{keyword}' (limit: {limit})")
            response = self.ebay_service.search_items_by_keyword(keyword, limit=limit)
            logger.info(f"Found {len(response.items)} items for '{keyword}'")
            return response.items
        except Exception as e:
            logger.error(f"Error fetching items for '{keyword}': {e}")
            return []
    
    def filter_quality_items(self, items: List[EbayItem]) -> List[EbayItem]:
        """Filter items based on quality criteria."""
        filtered_items = []
        
        for item in items:
            # Skip items with missing critical data
            if not item.title or not item.price or item.price <= 0:
                continue
                
            # Skip items with very low seller ratings
            if item.seller_rating < 90:
                continue
                
            # Skip items with very generic titles
            if len(item.title) < 10:
                continue
                
            filtered_items.append(item)
        
        logger.info(f"Filtered {len(items)} items down to {len(filtered_items)} quality items")
        return filtered_items
    
    def deduplicate_items(self, items: List[EbayItem]) -> List[EbayItem]:
        """Remove duplicate items based on title similarity."""
        seen_titles = set()
        unique_items = []
        
        for item in items:
            # Normalize title for comparison
            normalized_title = item.title.lower().strip()
            
            # Skip if we've seen a very similar title
            if any(self._title_similarity(normalized_title, seen) > 0.8 for seen in seen_titles):
                continue
                
            seen_titles.add(normalized_title)
            unique_items.append(item)
        
        logger.info(f"Deduplicated {len(items)} items down to {len(unique_items)} unique items")
        return unique_items
    
    def _title_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles."""
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    async def process_batch(self, items: List[EbayItem]) -> int:
        """Process a batch of items and add them to the vector database."""
        if not items:
            return 0
            
        try:
            logger.info(f"Processing batch of {len(items)} items...")
            
            # Convert EbayItems to the format expected by vector_db_service
            furniture_items = []
            for item in items:
                furniture_item = {
                    "id": item.item_id,
                    "title": item.title,
                    "description": f"{item.title} - {item.condition} condition",
                    "price": item.price,
                    "currency": item.currency,
                    "condition": item.condition,
                    "location": item.location,
                    "image_url": item.image_url,
                    "item_url": item.item_url,
                    "shipping_cost": item.shipping_cost or 0.0,
                    "seller_rating": item.seller_rating,
                    "vendor": "EBAY",
                    "vendor_item_id": item.item_id,
                    "category": "furniture",
                    "dimensions": None,
                    "materials": [],
                    "style": [],
                    "tags": []
                }
                furniture_items.append(furniture_item)
            
            # Add items to vector database
            added_count = 0
            for item in furniture_items:
                try:
                    self.vector_service.add_item(item)
                    added_count += 1
                except Exception as e:
                    logger.warning(f"Failed to add item {item['id']}: {e}")
                    continue
            
            logger.info(f"Successfully added {added_count} items to vector database")
            return added_count
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            return 0
    
    async def run_bulk_import(self):
        """Run the bulk import process."""
        logger.info("🚀 Starting bulk eBay furniture import...")
        logger.info(f"Target: {self.max_items} items, Batch size: {self.batch_size}")
        
        all_items = []
        keywords = self.get_search_keywords()
        
        # Fetch items from eBay
        for keyword in keywords:
            if len(all_items) >= self.max_items:
                break
                
            items = await self.fetch_items_from_ebay(keyword, limit=100)
            all_items.extend(items)
            
            # Rate limiting - be nice to eBay API
            await asyncio.sleep(1)
        
        logger.info(f"Fetched {len(all_items)} total items from eBay")
        
        # Filter and deduplicate
        quality_items = self.filter_quality_items(all_items)
        unique_items = self.deduplicate_items(quality_items)
        
        # Process in batches
        total_added = 0
        for i in range(0, len(unique_items), self.batch_size):
            batch = unique_items[i:i + self.batch_size]
            added = await self.process_batch(batch)
            total_added += added
            
            logger.info(f"Progress: {total_added}/{len(unique_items)} items processed")
            
            # Rate limiting between batches
            await asyncio.sleep(2)
        
        logger.info(f"✅ Bulk import completed! Added {total_added} items to vector database")

async def main():
    """Main function."""
    importer = BulkEbayImporter()
    await importer.run_bulk_import()

if __name__ == "__main__":
    asyncio.run(main()) 