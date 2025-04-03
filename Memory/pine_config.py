
import os
import pinecone

# Load your Pinecone API key and environment variables from your environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")  # e.g., 'us-west1-gcp'
INDEX_NAME = "memorytest"

# Initialize Pinecone with init() instead of configure()
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# Check if the index exists; if not, create it with the specified dimension for OpenAI embeddings
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Dimension for OpenAI embeddings
        metric="cosine"
    )

# Connect to the created or existing Pinecone index
index = pinecone.Index(INDEX_NAME)

print(f"Connected to Pinecone index: {INDEX_NAME}")
