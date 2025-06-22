# Test Scripts

This folder contains test scripts for the backend application.

## Available Tests

### `test_environment_switching.py`
Tests the eBay environment configuration system to ensure proper switching between sandbox and production environments.

**Usage:**
```bash
cd backend
python tests/test_environment_switching.py
```

**What it tests:**
- Environment variable loading
- Credential selection based on environment
- URL selection based on environment
- Service initialization with correct URLs

### `debug_ebay_auth.py`
Tests eBay OAuth authentication for both sandbox and production environments.

**Usage:**
```bash
cd backend
python tests/debug_ebay_auth.py
```

**What it tests:**
- eBay OAuth token acquisition
- Credential validation
- Environment-specific authentication

### `test_ebay_search.py`
Tests the eBay search API endpoints end-to-end.

**Usage:**
```bash
cd backend
# Make sure your server is running on localhost:8000
python tests/test_ebay_search.py
```

**What it tests:**
- GET `/api/ebay/search?q=<query>&limit=<limit>&offset=<offset>` endpoint
- POST `/api/ebay/search` endpoint
- Real eBay API integration
- Response parsing and data structure

### `test_ebay_api.py`
Tests the eBay API integration functionality.

## Running Tests

All test scripts can be run from the backend directory:

```bash
cd backend
python tests/<script_name>.py
```

## Environment Variables

Make sure your `.env` file contains the necessary eBay credentials:

```env
# Environment
EBAY_ENVIRONMENT=sandbox  # or "production"

# Sandbox credentials
EBAY_CLIENT_ID_SANDBOX=your_sandbox_client_id
EBAY_CLIENT_SECRET_SANDBOX=your_sandbox_client_secret

# Production credentials  
EBAY_CLIENT_ID_PRODUCTION=your_production_client_id
EBAY_CLIENT_SECRET_PRODUCTION=your_production_client_secret
```

## API Endpoints

### eBay Search Endpoints

- **GET** `/api/ebay/search?q=<query>&limit=<limit>&offset=<offset>`
- **POST** `/api/ebay/search` with JSON body:
  ```json
  {
    "query": "vintage chair",
    "limit": 50,
    "offset": 0
  }
  ```

Both endpoints return an `EbaySearchResponse` with items from the eBay Browse API. 