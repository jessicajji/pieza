import logging
import os
from typing import List, Optional, Tuple, Dict, Any
import openai
import torch
import clip
from PIL import Image
import requests
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor

from ..schemas.ebay import EbayItem

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating text and image embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        # Initialize OpenAI client
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
        
        # Load CLIP model
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
            logger.info(f"CLIP model loaded on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {str(e)}")
            raise
    
    def get_text_embedding(self, text: str) -> List[float]:
        """Generate text embedding using OpenAI's text-embedding-3-small model.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Text embedding vector
        """
        response = self.openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def get_bulk_text_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """Generate text embeddings for multiple texts in batches.
        
        Args:
            texts: List of texts to generate embeddings for
            batch_size: Number of texts to process in each batch
            
        Returns:
            List of text embedding vectors
        """
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing text embedding batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
            
            try:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=batch
                )
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
                
                # Rate limiting - be nice to OpenAI API
                if i + batch_size < len(texts):
                    import time
                    time.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"Error processing text embedding batch: {e}")
                # Add empty embeddings for failed batch
                all_embeddings.extend([[0.0] * 1536] * len(batch))
        
        return all_embeddings
    
    def get_image_embedding(self, image_url: str) -> List[float]:
        """Generate image embedding using CLIP model.
        
        Args:
            image_url: URL of the image to generate embedding for
            
        Returns:
            Image embedding vector
        """
        # Download and preprocess image
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Generate embedding
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features = image_features / image_features.norm(dim=1, keepdim=True)
        
        return image_features[0].cpu().numpy().tolist()
    
    def get_bulk_image_embeddings(self, image_urls: List[str], max_workers: int = 4) -> List[Optional[List[float]]]:
        """Generate image embeddings for multiple images in parallel.
        
        Args:
            image_urls: List of image URLs to generate embeddings for
            max_workers: Maximum number of parallel workers
            
        Returns:
            List of image embedding vectors (None for failed embeddings)
        """
        embeddings = [None] * len(image_urls)
        
        def process_single_image(args):
            idx, url = args
            try:
                return idx, self.get_image_embedding(url)
            except Exception as e:
                logger.warning(f"Failed to generate image embedding for {url}: {e}")
                return idx, None
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Process images in parallel
            futures = [executor.submit(process_single_image, (i, url)) for i, url in enumerate(image_urls)]
            
            for future in futures:
                try:
                    idx, embedding = future.result()
                    embeddings[idx] = embedding
                except Exception as e:
                    logger.error(f"Error in image embedding processing: {e}")
        
        return embeddings
    
    def get_item_embeddings(self, item: EbayItem) -> Tuple[List[float], Optional[List[float]]]:
        """Generate embeddings for an eBay item using all available fields for text embedding."""
        # Combine as much info as possible for the text embedding
        text_parts = [
            item.title,
            f"Condition: {item.condition}",
            f"Location: {item.location}",
            f"Price: {item.price} USD",
            f"Shipping cost: {item.shipping_cost if item.shipping_cost is not None else 'N/A'} USD",
            f"Seller rating: {item.seller_rating}",
            f"Item URL: {item.item_url}"
        ]
        # If category or description fields exist, add them
        if hasattr(item, 'category') and getattr(item, 'category', None):
            text_parts.append(f"Category: {item.category}")
        if hasattr(item, 'description') and getattr(item, 'description', None):
            text_parts.append(f"Description: {item.description}")
        text = ". ".join(str(part) for part in text_parts if part)
        text_embedding = self.get_text_embedding(text)

        # Always embed the image if image_url is present
        image_embedding = None
        if item.image_url:
            try:
                image_embedding = self.get_image_embedding(item.image_url)
            except Exception as e:
                logger.error(f"Failed to generate image embedding: {str(e)}")
        return text_embedding, image_embedding
    
    def get_bulk_item_embeddings(self, items: List[EbayItem], batch_size: int = 50) -> List[Tuple[List[float], Optional[List[float]]]]:
        """Generate embeddings for multiple eBay items in batches.
        
        Args:
            items: List of eBay items to generate embeddings for
            batch_size: Number of items to process in each batch
            
        Returns:
            List of (text_embedding, image_embedding) tuples
        """
        all_embeddings = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            logger.info(f"Processing item embedding batch {i//batch_size + 1}/{(len(items) + batch_size - 1)//batch_size}")
            
            # Prepare text data for batch processing
            texts = []
            image_urls = []
            
            for item in batch:
                # Prepare text for embedding
                text_parts = [
                    item.title,
                    f"Condition: {item.condition}",
                    f"Location: {item.location}",
                    f"Price: {item.price} USD",
                    f"Shipping cost: {item.shipping_cost if item.shipping_cost is not None else 'N/A'} USD",
                    f"Seller rating: {item.seller_rating}",
                    f"Item URL: {item.item_url}"
                ]
                if hasattr(item, 'category') and getattr(item, 'category', None):
                    text_parts.append(f"Category: {item.category}")
                if hasattr(item, 'description') and getattr(item, 'description', None):
                    text_parts.append(f"Description: {item.description}")
                
                text = ". ".join(str(part) for part in text_parts if part)
                texts.append(text)
                
                # Collect image URLs
                image_urls.append(item.image_url if item.image_url else None)
            
            # Generate text embeddings in batch
            text_embeddings = self.get_bulk_text_embeddings(texts)
            
            # Generate image embeddings in parallel
            image_embeddings = self.get_bulk_image_embeddings([url for url in image_urls if url])
            
            # Combine results
            batch_embeddings = []
            img_idx = 0
            for j, item in enumerate(batch):
                text_emb = text_embeddings[j]
                img_emb = None
                if image_urls[j]:
                    img_emb = image_embeddings[img_idx]
                    img_idx += 1
                
                batch_embeddings.append((text_emb, img_emb))
            
            all_embeddings.extend(batch_embeddings)
            
            # Rate limiting between batches
            if i + batch_size < len(items):
                import time
                time.sleep(1)
        
        return all_embeddings
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        return self.get_text_embedding(query) 