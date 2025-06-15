from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.api import search

app = FastAPI(
    title="Pieza Search API",
    description="API for searching furniture items using natural language",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 