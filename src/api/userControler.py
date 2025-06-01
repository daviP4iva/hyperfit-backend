from fastapi import APIRouter, HTTPException
from models.userModel import User
from services import userService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users")

@router.post("")
async def create_user_endpoint(user: User):
    try:
        return await userService.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{email}")
async def get_user_by_email_endpoint(email: str):
    try:
        return await userService.get_user_by_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{email}")
async def delete_user_by_email_endpoint(email: str):
    try:
        await userService.delete_user_by_email(email)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_all_users_endpoint():
    try:
        return await userService.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))