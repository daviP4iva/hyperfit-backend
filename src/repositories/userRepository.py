from db.session import get_user_collection
from models.userModel import User
from bson import ObjectId

async def create_user(user: User):
    collection = get_user_collection()
    user_dict = user.dict()
    user_dict["_id"] = str(ObjectId())
    result = await collection.insert_one(user_dict)
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

async def get_or_create_user_by_google_id(google_id: str, email: str, name: str):
    collection = get_user_collection()
    user = await collection.find_one({"google_id": google_id})
    if user:
        user["_id"] = str(user["_id"])
        return user
    # Si no existe, creamos el usuario
    user_dict = {
        "name": name,
        "email": email,
        "password": "",  # No hay password para Google
        "tipo_cuenta": "Personal",
        "altura": 0.0,
        "peso": 0.0,
        "nivel": "Principiante",
        "objetivo": "Mantener",
        "alergenos": "",
        "google_id": google_id
    }
    result = await collection.insert_one(user_dict)
    user_dict["_id"] = str(user_dict["_id"])
    return user_dict

