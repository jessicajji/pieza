from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Dimensions(BaseModel):
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None

class PromptParseResult(BaseModel):
    category: str = Field(..., description="The main category of furniture (e.g., 'sofa', 'chair', 'table')")
    dimensions: Optional[Dimensions] = Field(None, description="Dimensions of the furniture")
    material: List[str] = Field(default_factory=list, description="List of materials mentioned")
    style_keywords: List[str] = Field(default_factory=list, description="List of style-related keywords")
    hard_requirements: List[str] = Field(default_factory=list, description="List of non-negotiable requirements") 