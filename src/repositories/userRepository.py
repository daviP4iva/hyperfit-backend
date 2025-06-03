from db.session import get_user_collection
from models.userModel import User
from bson import ObjectId
import logging
from services import authService

logger = logging.getLogger(__name__)

async def create_user(user: User):
    collection = get_user_collection()
    user_dict = user.model_dump()
    result = await collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    logger.error(f"Created user in DB: {user_dict}")
    return user_dict

async def get_user_by_email(email: str):
    collection = get_user_collection()
    user = await collection.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
        return user
    return None

async def get_all_users():
    collection = get_user_collection()
    users = []
    async for user in collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

async def delete_user_by_email(email: str):
    collection = get_user_collection()
    result = await collection.delete_one({"email": email})
    return result.deleted_count

async def get_user_by_id(user_id: str):
    collection = get_user_collection()
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    return None

async def get_user_history(user_id: str):
    collection = get_user_collection()
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user["history"]
    return None

async def update_user(user_id: str, update_data: dict):
    collection = get_user_collection()
    result = await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        logger.warning(f"No changes made to user {user_id}")
        return None
    
    # Fetch and return the updated user
    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    if updated_user:
        updated_user["_id"] = str(updated_user["_id"])
    return updated_user

async def get_or_create_user_by_google_id(google_id: str, email: str, name: str):
    collection = get_user_collection()
    user = await collection.find_one({"email": email})
    if user:
        logger.error(f"User already exists: {user}")
        user["_id"] = str(user["_id"])
        return user, True
    # Si no existe, creamos el usuario
    user: User = User(
        name=name,
        email=email,
        google_id=google_id
    )
    logger.error(f"Creating user: {user}")
    return await create_user(user), False

