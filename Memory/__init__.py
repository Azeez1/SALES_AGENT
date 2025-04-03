# __init__.py
# This file makes it easy to import our Pinecone utilities from the utils package.

from .pine_config import index  # Expose the initialized Pinecone index
from .pine_memory import store_conversation_summary, retrieve_memories  # Expose memory functions
