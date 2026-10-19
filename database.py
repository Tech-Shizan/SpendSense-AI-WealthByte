import os
from dotenv import load_dotenv

# Explicitly load environment variables at the very top
load_dotenv()
basedir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(basedir, ".env"), override=True)

MONGO_URI = os.getenv("MONGO_URI")
print('MONGO_URI Loaded:', bool(os.getenv('MONGO_URI')))

import uuid
from datetime import datetime, timezone
from pymongo import MongoClient
from logic import mask_sensitive_data

client = None
db = None
chat_collection = None
last_uri = None

def get_collection():
    """Lazily initializes and returns the chat_history MongoDB collection."""
    global client, db, chat_collection, last_uri
    
    uri = os.getenv("MONGO_URI") or MONGO_URI
    if not uri:
        print("Warning: MONGO_URI is not set in environment or .env file.")
        return None
    
    if chat_collection is not None and last_uri == uri:
        return chat_collection
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client["SpendSenseDB"]
        chat_collection = db["chat_history"]
        last_uri = uri
        return chat_collection
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None


def create_session(title: str, masked_bill_data: str = None):
    """
    Inserts a new session document with fields:
    session_id, title, pinned, masked_bill_data, chat_messages, and created_at.
    Ensures all text is PII-masked before saving.
    Returns session_id on success, or None on failure (does not return fake UUID).
    """
    col = get_collection()
    if col is None:
        print("MongoDB error: Collection is not available.")
        return None
        
    session_id = str(uuid.uuid4())
    
    # Strictly enforce PII masking
    safe_title = mask_sensitive_data(title) if title else "New Chat"
    safe_bill_data = mask_sensitive_data(masked_bill_data) if masked_bill_data else None

    doc = {
        "session_id": session_id,
        "title": safe_title,
        "pinned": False,
        "masked_bill_data": safe_bill_data,
        "chat_messages": [],
        "created_at": datetime.now(timezone.utc)
    }

    try:
        result = col.insert_one(doc)
        if result and result.acknowledged:
            return session_id
        return None
    except Exception as e:
        print(f"Error creating session in MongoDB: {e}")
        return None


def get_sidebar_history():
    """
    Retrieves all sessions, sorted by pinned (True first) then created_at (descending).
    Returns a list of dictionaries with '_id' excluded.
    Returns None on failure/error (does not return [] on error).
    """
    col = get_collection()
    if col is None:
        print("MongoDB error: Collection is not available.")
        return None
    
    try:
        cursor = col.find({}, {"_id": 0}).sort([("pinned", -1), ("created_at", -1)])
        history = []
        for doc in cursor:
            # Map 'session_id' to 'id' for seamless UI compatibility
            doc["id"] = doc.get("session_id")
            history.append(doc)
        return history
    except Exception as e:
        print(f"Error retrieving sidebar history from MongoDB: {e}")
        return None


def toggle_pin(session_id: str, current_status: bool) -> bool:
    """Updates the pinned status of a specific session to the opposite of current_status."""
    col = get_collection()
    if col is None or not session_id:
        return False

    try:
        new_status = not bool(current_status)
        col.update_one(
            {"session_id": session_id},
            {"$set": {"pinned": new_status}}
        )
        return True
    except Exception as e:
        print(f"Error toggling pin status in MongoDB: {e}")
        return False


def delete_session(session_id: str) -> bool:
    """Deletes a specific session from the database."""
    col = get_collection()
    if col is None or not session_id:
        return False

    try:
        col.delete_one({"session_id": session_id})
        return True
    except Exception as e:
        print(f"Error deleting session from MongoDB: {e}")
        return False


def add_chat_message(session_id: str, role: str, text: str) -> bool:
    """
    Appends a new message object {role, text, timestamp} to the chat_messages array.
    Ensures message text is PII-masked before persistence.
    Returns True if successful, False otherwise.
    """
    col = get_collection()
    if col is None or not session_id:
        return False

    try:
        # Strictly enforce PII masking on every message stored
        safe_text = mask_sensitive_data(text) if text else ""
        msg_obj = {
            "role": role,
            "text": safe_text,
            "timestamp": datetime.now(timezone.utc)
        }
        res = col.update_one(
            {"session_id": session_id},
            {"$push": {"chat_messages": msg_obj}}
        )
        return bool(res and res.acknowledged)
    except Exception as e:
        print(f"Error adding chat message to MongoDB: {e}")
        return False


def get_session(session_id: str):
    """Retrieves a single session document by session_id."""
    col = get_collection()
    if col is None or not session_id:
        return None

    try:
        return col.find_one({"session_id": session_id}, {"_id": 0})
    except Exception as e:
        print(f"Error fetching session from MongoDB: {e}")
        return None
