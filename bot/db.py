"""
Database module for the NinjaTranslate bot.
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
from datetime import datetime
from config import config

# Initialize MongoDB client
client = AsyncIOMotorClient(config.mongo_uri)
db = client[config.mongo_db]

# Collections
users_collection = db.users

async def init_db():
    """
    Initialize database, create indexes if needed.
    """
    try:
        # Create indexes
        await users_collection.create_index("user_id", unique=True)
        logging.info("Database initialized successfully")
    except PyMongoError as e:
        logging.error(f"Database initialization error: {e}")

async def save_user(user_id: int, username: str, first_name: str, last_name: str, ui_lang: str):
    """
    Save or update user in database.
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        first_name: User's first name
        last_name: User's last name
        ui_lang: Selected interface language
    """
    try:
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "ui_lang": ui_lang,
            "last_activity": datetime.now()
        }
        
        # Update user data if exists, or insert new document
        await users_collection.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )
        
        logging.info(f"User data saved: {user_id}, {username}")
    except PyMongoError as e:
        logging.error(f"Error saving user to database: {e}")

async def get_user(user_id: int):
    """
    Get user data from database.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        User data or None if not found
    """
    try:
        return await users_collection.find_one({"user_id": user_id})
    except PyMongoError as e:
        logging.error(f"Error fetching user from database: {e}")
        return None

async def update_user_language(user_id: int, ui_lang: str):
    """
    Update user's interface language.
    
    Args:
        user_id: Telegram user ID
        ui_lang: New interface language
    """
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "ui_lang": ui_lang,
                    "last_activity": datetime.now()
                }
            }
        )
        logging.info(f"User language updated: {user_id}, {ui_lang}")
    except PyMongoError as e:
        logging.error(f"Error updating user language: {e}")

async def get_stats():
    """
    Get basic usage statistics.
    
    Returns:
        Dictionary with statistics
    """
    try:
        total_users = await users_collection.count_documents({})
        english_ui = await users_collection.count_documents({"ui_lang": "en"})
        arabic_ui = await users_collection.count_documents({"ui_lang": "ar"})
        
        return {
            "total_users": total_users,
            "english_ui": english_ui,
            "arabic_ui": arabic_ui
        }
    except PyMongoError as e:
        logging.error(f"Error getting statistics: {e}")
        return {
            "total_users": 0,
            "english_ui": 0,
            "arabic_ui": 0
        } 