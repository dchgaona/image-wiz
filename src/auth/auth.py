from fastapi import HTTPException
from models import UserInDB
from auth.security import verify_password, hash_password
from mongo.database_handler import db
import uuid

async def get_user(username: str) -> UserInDB | None:
    """Retrieve a user by username."""
    user_dict = await db["users"].find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)
    return None

async def register_user(username: str, password: str):
    """Register a new user."""
    existing_user = await db["users"].find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed = await hash_password(password)

    user_data = {
        "_id": str(uuid.uuid4()),
        "username": username,
        "hashed_password": hashed
    }
    
    user = UserInDB(**user_data)
    
    result = await db["users"].insert_one(user_data)
    return user

async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = await get_user(username)
    if not user or not await verify_password(password, user.hashed_password):
        return None
    return user