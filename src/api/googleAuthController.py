from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import RedirectResponse
from fastapi import status
from services.authService import google_auth
import os
import httpx
import logging

router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/v1/auth/google/callback")


@router.get("/google")
async def login_with_google():
    logger.info(f"GOOGLE_CLIENT_ID: {GOOGLE_CLIENT_ID}")
    #logger.info(f"GOOGLE_CLIENT_SECRET: {GOOGLE_CLIENT_SECRET}")
    logger.info(f"GOOGLE_REDIRECT_URI: {GOOGLE_REDIRECT_URI}")
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=consent" 
    )
    return RedirectResponse(google_auth_url)

@router.get("/google/callback")
async def google_callback(code: str):
    logger.info(f"code: {code}")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        tokens = response.json()
    # Obtener información del usuario con el id_token
    id_token_value = tokens.get("id_token")
    if not id_token_value:
        raise HTTPException(status_code=400, detail="No se pudo obtener el id_token de Google.")
    # Decodificar el id_token para obtener info del usuario
    from google.oauth2 import id_token
    from google.auth.transport import requests as grequests
    try:
        idinfo = id_token.verify_oauth2_token(id_token_value, grequests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo.get("email")
        name = idinfo.get("name")
        sub = idinfo.get("sub")
        # Aquí puedes buscar o crear el usuario en tu base de datos
        from services import userService
        user = await userService.get_or_create_user_by_google_id(sub, email, name)
        # Generar tu propio JWT
        from services.authService import generate_token
        jwt_token = generate_token(user["_id"])
        # Puedes devolver el token o redirigir a tu frontend con el token
        frontend_url = "http://localhost:3000/google/callback"
        return RedirectResponse(f"{frontend_url}?token={jwt_token}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verificando id_token: {e}")