from fastapi import FastAPI, HTTPException
import requests
import base64
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # Allow requests from all origins (update this with your specific requirements)

    allow_credentials=True,

    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],

    allow_headers=["*"],

)

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
HEADERS = {"Authorization": "Bearer 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"}



def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.ok:
        return response.content
    else:
        return None
 
@app.post("/generate_audioclip/")
async def generate_audio(request_data: dict):
    text = request_data.get('text')
    if not text:
        raise HTTPException(status_code=400, detail="Text field is missing")
   
    payload = {"inputs": text}
    audio_bytes = query(payload)
    if audio_bytes:
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {"audio_url": f"data:audio/wav;base64,{audio_base64}"}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate audio")
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
