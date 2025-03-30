# main.py
from fastapi import FastAPI, Request, Response
from twilio.twiml.voice_response import VoiceResponse
import httpx
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
ELEVEN_LABS_VOICE_ID = os.getenv(
    "ELEVEN_LABS_VOICE_ID")  # Your chosen voice ID

app = FastAPI()


async def generate_speech(text: str):
    """Generate speech using Eleven Labs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_LABS_VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


@app.post("/call")
async def handle_call(request: Request):
    """Handle incoming calls from Twilio"""
    form_data = await request.form()

    # Create TwiML response
    response = VoiceResponse()

    # In a real implementation, you'd capture the caller's speech
    # and send it to your LLM for processing

    # For now, use a static message
    message = "Hello! I'm your AI assistant powered by Eleven Labs. How can I help you today?"

    # Option 1: Use Twilio's built-in TTS (for testing)
    response.say(message)

    # Option 2: Use Eleven Labs for voice synthesis
    # This would require hosting the audio file and using <Play>
    # audio_data = await generate_speech(message)
    # audio_url = "URL to hosted audio file"  # You'd need to save and host the audio
    # response.play(audio_url)

    return Response(content=str(response), media_type="application/xml")
