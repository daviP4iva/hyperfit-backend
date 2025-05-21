from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

async def connect_to_mongo():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        await client.admin.command('ismaster')
        db = client[DB_NAME]
        logger.info("Connected to MongoDB")
    except ConnectionFailure as e:
        logger.error(f"MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client is not None:
        client.close()
        logger.info("MongoDB connection closed")

def get_user_collection():
    return db["users"]
