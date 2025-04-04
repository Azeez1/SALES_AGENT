import os
from pine_memory import store_conversation_summary, retrieve_memories

# Set the OpenAI API key if it's not already set in your environment
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"

def test_store_and_retrieve():
    # Define a sample conversation summary and metadata
    conversation_summary = "This is a test conversation summary to validate our integration."
    contact_id = "test_contact_001"
    timestamp = "2025-04-02T12:00:00Z"  # Use ISO 8601 format or your preferred timestamp format
    sentiment = "neutral"

    # Store the conversation summary in the Pinecone index
    print("Storing conversation summary...")
    store_conversation_summary(conversation_summary, contact_id, timestamp, sentiment)

    # Retrieve the stored memory for the given contact_id
    print("Retrieving stored memory...")
    memories = retrieve_memories(contact_id, top_k=1)



    print("Retrieved memories:", memories)

if __name__ == "__main__":
    test_store_and_retrieve()
