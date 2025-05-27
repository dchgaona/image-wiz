from fastapi import HTTPException
from models import UserInDB
from auth.security import verify_password, hash_password
from mongo.database_handler import db
import uuid

async def get_user(username: str) -> UserInDB | None:
    """Retrieve a user by username."""
    user = await db["users"].find_one({"username": username})

async def register_user(username: str, password: str):
    """Register a new user."""
    existing_user = await db["users"].find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed = hash_password(password)
    user = UserInDB(
        _id=str(uuid.uuid4()),
        username=username,
        hashed_password=hashed
    )
    db["users"].insert_one({"_id": user._id, "username": user.username, "hashed_password": user.hashed_password})

async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user