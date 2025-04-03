# pinecone_memory.py
# This file defines functions to store and retrieve conversation summaries (semantic memory) in Pinecone.

import os
import datetime

# Updated import based on deprecation warning:
from langchain_openai import OpenAIEmbeddings

from .pine_config import index  # Import the initialized Pinecone index

# Read the OpenAI API key from the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the embedding model with the API key
embedding_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

def store_conversation_summary(contact_id, summary_text, timestamp, sentiment):
    """
    Converts a conversation summary into an embedding and stores it in Pinecone.

    Parameters:
      - contact_id (str): Unique identifier for the contact.
      - summary_text (str): The text summary of the conversation.
      - timestamp (str or datetime): When the conversation occurred.
      - sentiment (str): Sentiment of the conversation (e.g., positive, negative).
    """
    # Ensure timestamp is in ISO format if it's a datetime object
    if isinstance(timestamp, datetime.datetime):
        timestamp_str = timestamp.isoformat()
    else:
        timestamp_str = str(timestamp)

    # Generate an embedding from the summary text
    embedding = embedding_model.embed_query(summary_text)
    # Create a unique vector ID using the contact ID and timestamp
    vector_id = f"{contact_id}-{timestamp_str}"

    # Prepare metadata to store along with the vector
    metadata = {
        "contact_id": contact_id,
        "timestamp": timestamp_str,
        "sentiment": sentiment
    }
    # Upsert the vector into Pinecone with its metadata
    index.upsert([(vector_id, embedding, metadata)])
    print(f"Stored memory for {contact_id} at {timestamp_str}")

def retrieve_memories(contact_id, top_k=3):
    """
    Retrieves the top 'k' most relevant memories for a given contact based on semantic similarity.

    Parameters:
      - contact_id (str): Unique identifier for the contact.
      - top_k (int): Number of memories to retrieve.

    Returns:
      - List of matching memories with metadata.
    """
    # Generate an embedding from the contact_id to use as a query vector
    query_vector = embedding_model.embed_query(contact_id)
    # Query Pinecone for the top_k similar vectors
    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )
    return results['matches']
