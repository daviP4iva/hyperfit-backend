from fastapi import APIRouter, HTTPException
from services import userService
from models.userModel import User
import logging
from pydantic import BaseModel
import os
from fastapi.responses import RedirectResponse
from services.authService import google_auth, generate_token
import httpx

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class GoogleCallback(BaseModel):
    code: str

class GoogleLoginResponse(BaseModel):
    token: str
    existed: bool

router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

class Login(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(login: Login):
    return await userService.login(login.email, login.password)

@router.post("/register")
async def register(user: UserRegister):
    logger.error(f"Creating user: {user}")
    user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    return await userService.create_user(user)


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

@router.post("/google/callback")
async def google_callback(code: GoogleCallback):
    try:
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code.code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        async with httpx.AsyncClient() as client:
            # Get tokens
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()
            
            # Get user info
            userinfo_response = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()
            
            # Create or get user
            user, existed = await userService.get_or_create_user_by_google_id(
                user_info['sub'],
                user_info['email'],
                user_info.get('name', '')
            )
            logger.error(f"User: {user}")
            
            # Generate JWT token
            return GoogleLoginResponse(token=generate_token(user["_id"]), existed=existed)
            
    except Exception as e:
        logger.error(f"Error in Google callback: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error in Google authentication: {str(e)}")
    
    