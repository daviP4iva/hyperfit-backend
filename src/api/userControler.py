from fastapi import APIRouter, HTTPException
from models.userModel import LevelEnum, GoalEnum
from services import userService
import logging
from pydantic import BaseModel
from fastapi import Request
from services import authService

logger = logging.getLogger(__name__)

class UserProfile(BaseModel):
    height: int 
    weight: int 
    level: LevelEnum 
    goal: GoalEnum
    allergens: str | None = None

router = APIRouter(prefix="/user")

@router.get("/me")
async def get_user_by_email_endpoint(request: Request):
    try:
        user = await authService.get_user_by_request(request)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{email}")
async def delete_user_by_email_endpoint(email: str):
    try:
        await userService.delete_user_by_email(email)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_users_endpoint():
    try:
        return await userService.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile")
async def add_user_profile(profile: UserProfile, request: Request):
    try:
        user = await authService.get_user_by_request(request)
        logger.error(f"Updating profile for user: {user}")
        
        # Create update dictionary
        update_data = {
            "height": profile.height,
            "weight": profile.weight,
            "level": profile.level,
            "goal": profile.goal,
            "allergens": profile.allergens
        }
        
        # Update user in database
        updated_user = await userService.update_user(user["_id"], update_data)
        logger.error(f"User profile updated successfully: {updated_user}")
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))