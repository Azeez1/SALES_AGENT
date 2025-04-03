
import os
from pinecone import Pinecone, ServerlessSpec

# Load your Pinecone API key and environment variables from your environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "memorytest"

# Initialize Pinecone with new client format
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if the index exists; if not, create it with the specified dimension for OpenAI embeddings
if INDEX_NAME not in pc.list_indexes():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Dimension for OpenAI embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the created or existing Pinecone index
index = pc.Index(INDEX_NAME)

print(f"Connected to Pinecone index: {INDEX_NAME}")
