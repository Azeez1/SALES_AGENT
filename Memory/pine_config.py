
# pinecone_config.py
# This file contains configuration settings and index initialization for Pinecone.

import os
from pinecone import Pinecone

# Load your Pinecone API keys and environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")  # e.g., 'us-west1-gcp'
INDEX_NAME = "memorytest"

# Initialize Pinecone with your API key
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if the index exists; if not, create it with the specified dimension for OpenAI embeddings
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Dimension for OpenAI embeddings
        metric="cosine"
    )

# Connect to the created or existing Pinecone index
index = pc.Index(INDEX_NAME)
