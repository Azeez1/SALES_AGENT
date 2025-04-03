import os
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

# Load your Pinecone API key and environment variables from your environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "memorytest"

# Create a Pinecone client instance using the new gRPC class
pc = Pinecone(api_key=PINECONE_API_KEY)

# Get the list of existing index names (as a set of names)
existing_indexes = {info["name"] for info in pc.list_indexes()}

# Check if the index exists; if not, create it with the specified dimension for OpenAI embeddings
if INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,  # Dimension for OpenAI embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    print(f"Created Pinecone index: {INDEX_NAME}")
else:
    print(f"Pinecone index {INDEX_NAME} already exists.")

# Connect to the created or existing Pinecone index
index = pc.Index(INDEX_NAME)

print(f"Connected to Pinecone index: {INDEX_NAME}")
