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
async def google_callback(token: str):
    try:
        await google_auth(token)
        return {"message": "User authenticated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error verificando id_token: {e}")
    