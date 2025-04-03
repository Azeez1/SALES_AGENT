# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Memory.pine_memory import store_conversation_summary, retrieve_memories
import datetime
import os

app = FastAPI()

# Define the request model for storing a memory
class StoreMemoryRequest(BaseModel):
    contact_id: str
    summary_text: str
    timestamp: str  # should be in ISO format (e.g., "2025-04-02T20:00:00")
    sentiment: str

#########   STORE FUNCTION ###################
# @app.post("/store")
# async def store_memory(data: StoreMemoryRequest):
#     try:
#         # Convert timestamp from string to datetime
#         ts = datetime.datetime.fromisoformat(data.timestamp)
#         # Call the function to store the conversation summary in Pinecone
#         store_conversation_summary(
#             contact_id=data.contact_id,
#             summary_text=data.summary_text,
#             timestamp=ts,
#             sentiment=data.sentiment
#         )
#         return {"status": "success", "message": f"Stored memory for {data.contact_id}"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/retrieve")
async def get_memory(contact_id: str, top_k: int = 3):
    try:
        # Retrieve memories for the given contact_id
        results = retrieve_memories(contact_id, top_k=top_k)
        return {"contact_id": contact_id, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
