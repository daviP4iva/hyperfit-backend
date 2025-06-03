import bcrypt
import os
from fastapi import Request, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv
from jose import jwt
from services import userService
import logging

load_dotenv()

logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id: str):
    return jwt.encode({'user_id': user_id}, os.getenv('JWT_SECRET'), algorithm='HS256')

def verify_token(token: str):
    return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])

async def get_user_from_token(token: str):
    decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    from services import userService
    user = await userService.get_user_by_id(user_id)
    return user

async def get_user_by_request(request: Request):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await get_user_from_token(token[7:])


async def google_auth(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        user_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        from services import userService
        user = await userService.get_or_create_user_by_google_id(user_id, email, name)
        return generate_token(user["_id"])
    except Exception as e:
        print("Error verifying Google token:", e)
        return None


