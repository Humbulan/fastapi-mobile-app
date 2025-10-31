from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime

# Your MongoDB Atlas connection string
MONGODB_URL = os.environ.get(
    "MONGODB_URL", 
    "mongodb+srv://Humbulani:YOUR_PASSWORD_HERE@skim99.1go8lny.mongodb.net/?retryWrites=true&w=majority&appName=Skim99"
)

# Create MongoDB client with proper configuration
try:
    client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
    
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    
    # Get database and collections
    database = client.fastapi_app
    users_collection = database.users
    sessions_collection = database.sessions
    premium_data_collection = database.premium_data
    
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    # Fallback to local development (you can remove this in production)
    client = None
    database = None
    users_collection = None
    sessions_collection = None
    premium_data_collection = None

# MongoDB helper functions
async def get_user_by_username(username: str):
    if not users_collection:
        return None
    user = users_collection.find_one({"username": username})
    return user

async def get_user_by_email(email: str):
    if not users_collection:
        return None
    user = users_collection.find_one({"email": email})
    return user

async def create_user(user_data: dict):
    if not users_collection:
        return None
    result = users_collection.insert_one(user_data)
    return result

async def update_user(username: str, update_data: dict):
    if not users_collection:
        return None
    update_data["updated_at"] = datetime.utcnow()
    result = users_collection.update_one(
        {"username": username}, 
        {"$set": update_data}
    )
    return result

async def save_session_data(session_data: dict):
    if not sessions_collection:
        return None
    result = sessions_collection.insert_one(session_data)
    return result

async def get_session_data(session_id: str):
    if not sessions_collection:
        return None
    session = sessions_collection.find_one({"session_id": session_id})
    return session

# Test the connection on startup
if client:
    try:
        client.admin.command('ping')
        print("🎉 MongoDB Atlas connection is working perfectly!")
    except Exception as e:
        print(f"⚠️  MongoDB connection test failed: {e}")
