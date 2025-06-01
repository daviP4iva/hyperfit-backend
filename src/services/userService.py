from repositories import userRepository
from models.userModel import User
from fastapi import HTTPException
from services import authService

async def create_user(user: User):
    if await get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    user = await userRepository.create_user(user)
    return authService.generate_token(user["_id"])

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
