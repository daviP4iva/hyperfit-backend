from fastapi import APIRouter, HTTPException, Request, Response, Body, status
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional

# Crear cliente OpenAI con base_url para OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_message: str
    model: str = "google/gemini-2.0-flash-exp:free"
    history: Optional[list[Message]] = None

@router.post("/chat")
async def chat_with_model(req: Optional[ChatRequest] = Body(None)):
    if req is None:
        raise HTTPException(status_code=400, detail="No body provided")
    try:
        # Construye la lista de mensajes
        messages = [
            {
                "role": "system",
                "content": "Eres un chatbot insertado en una aplicación de fitness. Tu objetivo es ayudar a los usuarios con sus preguntas relacionadas con el fitness, la nutrición y el bienestar. No quiero que uses marcaciones especiales como **, ya que inserto como string y no se ve, ya que se mostrará en la pantalla como un mensaje de chat. No te enrolles mucho, mensajes cortos y utiliza emojis. Recomienda ejercicios en gimnasio, rutinas de entrenamiento.",
            }
        ]
        if req.history:
            # Añade el historial previo
            messages.extend([msg.dict() for msg in req.history])
        # Añade el mensaje actual del usuario
        messages.append({
            "role": "user",
            "content": req.user_message
        })
        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))