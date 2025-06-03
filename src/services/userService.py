from repositories import userRepository
from models.userModel import User
from fastapi import HTTPException
from services import authService
import logging

logger = logging.getLogger(__name__)

async def login(email: str, password: str):
    user = await userRepository.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not authService.verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")
    return authService.generate_token(user["_id"])

async def create_user(user: User):
    if await get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before storing
    user.password = authService.hash_password(user.password)
    
    # Create user in database
    created_user = await userRepository.create_user(user)
    logger.error(f"Created user: {created_user}")
    
    # Generate token using the user's _id
    return authService.generate_token(created_user["_id"])

async def get_user_by_email(email: str):
    user = await userRepository.get_user_by_email(email)
    if not user:
        return None
    return user

async def delete_user_by_email(email: str):
    await userRepository.delete_user_by_email(email)

async def get_user_by_id(user_id: str):
    user = await userRepository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_all_users():
    return await userRepository.get_all_users()

async def get_or_create_user_by_google_id(google_id: str, email: str, name: str):
    user, existed = await userRepository.get_or_create_user_by_google_id(google_id, email, name)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create or get user")
    return user, existed

async def update_user(user_id: str, update_data: dict):
    logger.error(f"Updating user {user_id} with data: {update_data}")
    return await userRepository.update_user(user_id, update_data)