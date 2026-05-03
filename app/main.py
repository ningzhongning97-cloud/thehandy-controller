"""
FastAPI backend for The Handy AI Voice Controller
"""

import os
import sys
import logging
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.ai_brain import AIBrain
from thehandy import HandyController
from thehandy.exceptions import HandyException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="The Handy AI Voice Controller")

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Global instances
handy: HandyController = None
ai_brain: AIBrain = None


def get_handy() -> HandyController:
    global handy
    if handy is None:
        handy = HandyController()
    return handy


def get_ai() -> AIBrain:
    global ai_brain, handy
    if ai_brain is None:
        ai_brain = AIBrain(handy_controller=handy)  # handy can be None (no device)
    return ai_brain


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    actions: list[dict] = []


class ConnectRequest(BaseModel):
    connection_key: str


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/connect")
async def connect_device(req: ConnectRequest):
    global handy, ai_brain
    try:
        handy = HandyController(connection_key=req.connection_key)
        handy.connect()
        ai_brain = AIBrain(handy_controller=handy)
        return {"status": "connected", "message": "设备连接成功"}
    except HandyException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def device_status():
    try:
        h = get_handy()
        return {"connected": h.is_connected()}
    except Exception:
        return {"connected": False}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        ai = get_ai()
        reply, actions = await ai.chat(req.message)
        return ChatResponse(reply=reply, actions=actions)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-persona")
async def set_persona(data: dict):
    try:
        persona = data.get("persona", "flame")
        ai = get_ai()
        ai.set_persona(persona)
        names = {"ice": "冷颜", "flame": "热焰"}
        return {"status": "ok", "persona": persona, "name": names.get(persona, persona)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auto-tick", response_model=ChatResponse)
async def auto_tick():
    try:
        ai = get_ai()
        reply, actions = await ai.auto_tick()
        return ChatResponse(reply=reply, actions=actions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ElevenLabs voice IDs per persona
PERSONA_VOICES = {
    "flame":   "AZnzlk1XvdvUeBnXmlld",  # Domi - strong, passionate
    "ice":     "21m00Tcm4TlvDq8ikWAM",  # Rachel - calm, controlled
    "kitten":  "EXAVITQu4vr4xnSDxMaL",  # Bella - soft, young
    "oneesan": "21m00Tcm4TlvDq8ikWAM",  # Rachel - mature, warm
    "kouhai":  "MF3mGyEYCl7XYWbV9V6O",  # Elli - young, emotional
    "boss":    "AZnzlk1XvdvUeBnXmlld",  # Domi - strong
}


class TTSRequest(BaseModel):
    text: str
    persona: str = "flame"


@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ElevenLabs API key not configured")

    voice_id = PERSONA_VOICES.get(req.persona, PERSONA_VOICES["flame"])
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={"xi-api-key": api_key, "Content-Type": "application/json"},
            json={
                "text": req.text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.5},
            },
            timeout=30,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"ElevenLabs error: {resp.text}")

        return StreamingResponse(
            iter([resp.content]),
            media_type="audio/mpeg",
            headers={"Content-Length": str(len(resp.content))},
        )


@app.post("/stop")
async def stop_device():
    try:
        h = get_handy()
        h.stop()
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
