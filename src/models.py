from pydantic import BaseModel

class User(BaseModel):
    _id: str
    username: str

class UserInDB(User):
    hashed_password: str

class RegisterReq(BaseModel):
    username: str
    password: str