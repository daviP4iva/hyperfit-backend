from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import os
import httpx
from typing import Optional

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str
    model: str = "deepseek-ai/DeepSeek-V3-0324"
    history: Optional[list[Message]] = None

@router.post("/chat")
async def chat_with_model(req: Optional[ChatRequest] = Body(None)):
    if req is None:
        raise HTTPException(status_code=400, detail="No body provided")
    try:
        messages = [
            {
                "role": "system",
                "content": "Eres un chatbot insertado en una aplicación de fitness. Tu objetivo es ayudar a los usuarios con sus preguntas relacionadas con el fitness, la nutrición y el bienestar. No quiero que uses marcaciones especiales como **, ya que inserto como string y no se ve, ya que se mostrará en la pantalla como un mensaje de chat. No te enrolles mucho, mensajes cortos y utiliza emojis. Recomienda ejercicios en gimnasio, rutinas de entrenamiento.",
            }
        ]
        if req.history:
            messages.extend([msg.dict() for msg in req.history])
        messages.append({
            "role": "user",
            "content": req.user_message
        })

        api_token = os.getenv("OPENROUTER_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        body = {
            "model": req.model,
            "messages": messages,
            "stream": False,
            "max_tokens": 1024,
            "temperature": 0.7
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://llm.chutes.ai/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return {"response": data["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))