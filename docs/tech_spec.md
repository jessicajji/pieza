# Pieza Tech Spec: Milestone 1

## Overview
This document outlines the technical architecture and implementation plan for Pieza MVP (Milestone 1), which enables AI-powered, prompt-based furniture discovery using vendor search APIs and image-based semantic matching.

## Guiding Principles
- Prioritize speed of development and agent-driven workflows
- Use vendor search APIs only (no scraping or full catalog ingestion)
- Leverage multimodal models for semantic search over product images

## Core Components

### 1. Prompt Parsing Agent
- Tech: OpenAI GPT-4 via function-calling
- Function output schema:
```json
{
  "category": "sofa",
  "dimensions": {"width": 70},
  "material": ["velvet", "wood legs"],
  "style_keywords": ["modern", "low back"],
  "hard_requirements": ["curved back", "two-piece"]
}
```
- Usage: Converts natural language into structured query components + search intent metadata

### 2. Vendor Search API Integrations
- Vendors (tentative): Wayfair Professional, Article, Amazon PA-API, West Elm (if public)
- Query strategy:
  - Use structured fields from prompt parsing agent to call vendor APIs
  - Use broad category + style terms to ensure wide retrieval

### 3. Visual Embedding + Vector Index
- Model: OpenCLIP or BLIP to encode product image + title + description into embedding
- Store: Use vector DB (e.g. Qdrant or Weaviate) to index embeddings
- Pipeline:
  - On API response, fetch product image and metadata
  - Generate embedding on-the-fly and store with product ID + URL + metadata
  - Refresh index periodically (e.g. every 7 days per vendor)

### 4. Semantic Search + Re-Ranking
- User prompt is encoded using same embedding model
- Use the user's original prompt a second time to encode it into a vector using the same model (e.g., CLIP)
- Perform similarity search against the image-based vector index of retrieved products
- Return top-N matches
- Optionally: Use GPT-4 to re-rank top 20 results based on prompt fit

### 5. Frontend Interface
- Stack: React + Next.js + TailwindCSS
- Features:
  - Prompt input bar
  - Chat-based refinement loop
  - Grid view for product results with images, titles, and dimensions

### 6. Backend API Layer
- Stack: FastAPI or Node.js (Express)
- Endpoints:
  - `/search` – receives prompt, calls parsing agent, triggers vendor API queries, updates vector index, performs semantic match, returns products
  - `/refine` – handles follow-up refinements in conversation
  - `/products` – lightweight metadata cache for recent vendor results

### 7. Session-Level Memory
- Scope: Single-session memory stored in backend state or passed client-side
- Includes:
  - Original prompt
  - Parsed spec
  - List of retrieved products
  - Ongoing refinements
- Purpose: Enables prompt refinement and conversational flow without re-asking for original context

## Key Tradeoffs
- Limiting to vendors with APIs reduces coverage but improves stability and compliance
- Embedding image-based search avoids relying on incomplete product metadata
- Refreshing vectors weekly ensures up-to-date results without storing full catalogs

## Next Steps
1. Confirm vendor API documentation and rate limits
2. Choose embedding model + test semantic recall quality
3. Build minimal vector index pipeline from API response → vector DB
4. Stand up basic UI + chat loop connected to backend agent

## Stretch Goals
- Add lightweight telemetry to evaluate prompt-to-match success rate
- Allow product save/shortlist (stub UI for Milestone 2)

## Milestone 2: Future Capabilities

### 1. Agent-Side Memory
- Agent (GPT-4 or hosted assistant) retains contextual history across the session
- Supports more natural back-and-forth conversations and deeper refinement awareness

### 2. Catalog Scraping + Full Vendor Indexing
- Add scraping layer for vendors without search APIs
- Store full catalog snapshots in normalized database
- Enable full-site semantic search rather than snapshot-based retrieval
- Refresh cadence: 1–2x weekly; managed per vendor pipeline

### 3. Long-Term Memory
- Store user preferences, past projects, saved items
- Use to personalize future prompts and refine semantic matching
- Includes preferred styles, dimensions, vendors, and material choices 