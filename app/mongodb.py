from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime

# Your MongoDB Atlas connection string
MONGODB_URL = os.environ.get(
    "MONGODB_URL", 
    "mongodb+srv://Humbulani:YOUR_PASSWORD_HERE@skim99.1go8lny.mongodb.net/?retryWrites=true&w=majority&appName=Skim99"
)

print(f"🔧 Attempting MongoDB connection to: {MONGODB_URL.split('@')[1].split('/')[0] if '@' in MONGODB_URL else MONGODB_URL}")

# Create MongoDB client with CORRECTED SSL configuration
try:
    # --- FIXED: Removed conflicting tlsInsecure parameter ---
    client = MongoClient(
        MONGODB_URL, 
        server_api=ServerApi('1'),
        # KEEP THIS: Bypass SSL certificate validation
        tlsAllowInvalidCertificates=True,
        # REMOVED: tlsInsecure=True (conflicts with tlsAllowInvalidCertificates)
        # Additional stable connection parameters
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        serverSelectionTimeoutMS=30000,
        maxPoolSize=10
    )
    
    # Test connection
    client.admin.command('ping')
    print("✅ SUCCESS: Connected to MongoDB Atlas with corrected SSL configuration!")
    
    # Get database and collections
    database = client.fastapi_app
    users_collection = database.users
    sessions_collection = database.sessions
    premium_data_collection = database.premium_data
    
    print("🎉 MongoDB collections initialized successfully!")
    
except Exception as e:
    print(f"❌ CRITICAL: MongoDB connection failed: {e}")
    print("💡 This indicates a fundamental environment issue with Render's free tier.")
    # Fallback to local development
    client = None
    database = None
    users_collection = None
    sessions_collection = None
    premium_data_collection = None

# MongoDB helper functions
def get_user_by_username(username: str):
    if not users_collection:
        print("⚠️  MongoDB not connected - returning None for user lookup")
        return None
    try:
        user = users_collection.find_one({"username": username})
        return user
    except Exception as e:
        print(f"❌ Error in get_user_by_username: {e}")
        return None

def get_user_by_email(email: str):
    if not users_collection:
        return None
    try:
        user = users_collection.find_one({"email": email})
        return user
    except Exception as e:
        print(f"❌ Error in get_user_by_email: {e}")
        return None

def create_user(user_data: dict):
    if not users_collection:
        return None
    try:
        result = users_collection.insert_one(user_data)
        return result
    except Exception as e:
        print(f"❌ Error in create_user: {e}")
        return None

def update_user(username: str, update_data: dict):
    if not users_collection:
        return None
    try:
        update_data["updated_at"] = datetime.utcnow()
        result = users_collection.update_one(
            {"username": username}, 
            {"$set": update_data}
        )
        return result
    except Exception as e:
        print(f"❌ Error in update_user: {e}")
        return None

def save_session_data(session_data: dict):
    if not sessions_collection:
        return None
    try:
        result = sessions_collection.insert_one(session_data)
        return result
    except Exception as e:
        print(f"❌ Error in save_session_data: {e}")
        return None

def get_session_data(session_id: str):
    if not sessions_collection:
        return None
    try:
        session = sessions_collection.find_one({"session_id": session_id})
        return session
    except Exception as e:
        print(f"❌ Error in get_session_data: {e}")
        return None

# Enhanced connection test
if client:
    try:
        client.admin.command('ping')
        print("🎯 MongoDB Atlas connection is ACTIVE and WORKING!")
        print("📊 Database: fastapi_app")
        print("🗂️  Collections: users, sessions, premium_data")
        print("🔐 SSL Configuration: tlsAllowInvalidCertificates=True (tlsInsecure REMOVED)")
    except Exception as e:
        print(f"⚠️  MongoDB connection test failed: {e}")
else:
    print("🚨 MongoDB client is None - connection failed completely")
