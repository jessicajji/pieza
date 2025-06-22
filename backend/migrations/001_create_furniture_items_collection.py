import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PayloadSchemaType
from dotenv import load_dotenv

# Load .env from backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

print("QDRANT_URL:", os.environ.get("QDRANT_URL"))
print("QDRANT_API_KEY:", os.environ.get("QDRANT_API_KEY"))

COLLECTION_NAME = "furniture_items"
VECTOR_SIZE = 1536  # Adjust if your embedding size is different

QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables must be set.")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# 1. Create collection if it doesn't exist
if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
    print(f"Creating collection {COLLECTION_NAME}...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
else:
    print(f"Collection {COLLECTION_NAME} already exists.")

# 2. Create payload indexes
print("Creating vendor index...")
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="vendor",
    field_schema=PayloadSchemaType.KEYWORD
)
print("Creating vector_item_id index...")
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="vector_item_id",
    field_schema=PayloadSchemaType.INTEGER
)
print("Done.") 