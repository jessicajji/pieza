from dotenv import load_dotenv
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file before anything else
# This is crucial because other modules may depend on these variables at import time
# pydantic's settings management will automatically override with any variables
# already present in the environment.
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

from app.api import search, ebay_compliance

app = FastAPI(
    title="Pieza Search API",
    description="API for searching furniture items using natural language",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(ebay_compliance.router, prefix="/api", tags=["ebay-compliance"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pieza API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 