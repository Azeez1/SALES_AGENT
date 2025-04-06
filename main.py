# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Memory.pine_memory import store_conversation_summary, retrieve_memories
import datetime
import os
import logging
from fastapi.responses import JSONResponse
from fastapi import Request

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

logging.basicConfig(level=logging.INFO)


@app.get("/")
def root():
    return {"message": "FastAPI is working ✅"}


@app.get("/retrieve")
async def get_memory(contact_id: str, top_k: int = 3):
    try:
        logging.info(f"🔍 Fetching memory for: {contact_id}, top_k={top_k}")
        raw_results = retrieve_memories(contact_id, top_k=top_k)

        # Serialize each result properly
        results = []
        for r in raw_results:
            results.append({
                "id": r.get("id"),
                "score": r.get("score"),
                "metadata": r.get("metadata", {})
            })

        logging.info(f"✅ Cleaned Results: {results}")
        return {"contact_id": contact_id, "results": results}

    except Exception as e:
        logging.error(f"❌ Error in /retrieve: {e}")
        raise HTTPException(status_code=500, detail=str(e))






@app.post("/conversation-initiation")
async def conversation_initiation(request: Request):
    try:
        # 🧠 Grab caller ID from custom header
        caller_id = request.headers.get("x-caller-id")

        if not caller_id:
            print("⚠️ No caller ID received in header. Returning fallback memory.")
            return {
                "client_data": {
                    "long_term_memory": "No prior memory available for this caller."
                }
            }

        print(f"📞 Caller ID from header: {caller_id}")

        # 🔍 Retrieve Pinecone memory
        memories = retrieve_memories(caller_id)

        # 📝 Format memory for LLM injection
        if not memories:
            memory_text = "No past memory found for this caller."
        else:
            memory_text = "\n".join([
                f"{m['metadata']['timestamp']} - {m['metadata']['sentiment']}"
                for m in memories
            ])

        return {
            "client_data": {
                "long_term_memory": memory_text
            }
        }

    except Exception as e:
        print("❌ Error in initiation:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
