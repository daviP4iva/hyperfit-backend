import bcrypt
from jose import jwt
import os
from services import userService


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id: str):
    return jwt.encode({'user_id': user_id}, os.getenv('JWT_SECRET'), algorithm='HS256')

def verify_token(token: str):
    return jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])

def get_user_from_token(token: str):
    decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    user = userService.get_user_by_id(user_id)
    return user

def google_auth(token: str):
    pass


