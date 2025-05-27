from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

# Crear cliente OpenAI con base_url para OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

router = APIRouter()

class ChatRequest(BaseModel):
    user_message: str
    model: str = "deepseek/deepseek-chat-v3-0324:free"

@router.post("/chat")
async def chat_with_model(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model=req.model,
            messages=[
                {
                    "role": "system",
                    "content": "Eres un chatbot insertado en una aplicación de fitness. Tu objetivo es ayudar a los usuarios con sus preguntas relacionadas con el fitness, la nutrición y el bienestar. No quiero que uses marcaciones especiales, ya que se mostrará en la pantalla como un mensaje de chat. No te enrolles mucho y utiliza emojis. Recomienda ejercicios en gimnasio, rutinas de entrenamiento.",
                },
                {
                    "role": "user",
                    "content": req.user_message
                }
            ],
        )
        # Acceso correcto para openai>=1.0.0 con OpenAI()
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
