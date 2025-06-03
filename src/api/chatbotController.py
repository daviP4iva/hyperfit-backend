from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
import os
import httpx
from typing import Optional
from fastapi import Request
from services.authService import get_user_by_request
from repositories.userRepository import update_user

router = APIRouter(prefix="/chat")

@router.post("")
async def chat_with_model(message: str, request: Request):
    if message is None:
        raise HTTPException(status_code=400, detail="No message provided")
    try:
        messages = [
            {
                "role": "system",
                "content": "Eres un chatbot insertado en una aplicación de fitness. Tu objetivo es ayudar a los usuarios con sus preguntas relacionadas con el fitness, la nutrición y el bienestar. No quiero que uses marcaciones especiales como **, ya que inserto como string y no se ve, ya que se mostrará en la pantalla como un mensaje de chat. No te enrolles mucho, mensajes cortos y utiliza emojis. Recomienda ejercicios en gimnasio, rutinas de entrenamiento.",
            }
        ]
        user = get_user_by_request(request)
        if user.history:
            messages.extend([msg.dict() for msg in user.history])
        
        

        messages.append({
            "role": "user",
            "content": message
        })

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "deepseek-ai/DeepSeek-V3-0324",
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
            response = data["choices"][0]["message"]["content"]
            user.history.append({"role": "assistant", "content": response})
            await userService.update_user(user)
            return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))