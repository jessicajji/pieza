import logging
import os
from typing import List, Optional, Tuple
import openai
import torch
import clip
from PIL import Image
import requests
from io import BytesIO

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
    
    def get_item_embeddings(self, item: EbayItem) -> Tuple[List[float], Optional[List[float]]]:
        """Generate embeddings for an eBay item.
        
        Args:
            item: eBay item to generate embeddings for
            
        Returns:
            Tuple of (text_embedding, image_embedding)
        """
        # Generate text embedding from item title
        text_embedding = self.get_text_embedding(item.title)
        
        # Generate image embedding if image URL is available
        image_embedding = None
        if item.image_url:
            try:
                image_embedding = self.get_image_embedding(item.image_url)
            except Exception as e:
                logger.error(f"Failed to generate image embedding: {str(e)}")
        
        return text_embedding, image_embedding
    
    def get_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        return self.get_text_embedding(query) 