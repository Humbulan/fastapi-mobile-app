from motor.motor_asyncio import AsyncIOMotorClient
import os
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# MongoDB connection - use environment variable for production
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")

# Create MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
database = client.fastapi_app

# Collections
users_collection = database.users
sessions_collection = database.sessions
premium_data_collection = database.premium_data

# Pydantic models for MongoDB documents
class User(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str
    premium: bool = False
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: str

class TokenData(BaseModel):
    username: str
    premium: bool

# MongoDB helper functions
async def get_user_by_username(username: str):
    user = await users_collection.find_one({"username": username})
    return user

async def get_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    return user

async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    return result

async def update_user(username: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()
    result = await users_collection.update_one(
        {"username": username}, 
        {"$set": update_data}
    )
    return result

async def save_session_data(session_data: dict):
    result = await sessions_collection.insert_one(session_data)
    return result

async def get_session_data(session_id: str):
    session = await sessions_collection.find_one({"session_id": session_id})
    return session

print("✅ MongoDB configuration loaded successfully!")
