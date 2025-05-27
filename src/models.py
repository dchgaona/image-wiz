from pydantic import BaseModel, Field

class User(BaseModel):
    _id: str
    username: str

class UserInDB(User):
    id: str = Field(alias='_id')
    username: str
    hashed_password: str

    class Config:
        populate_by_name = True
        from_attributes = True

class RegisterReq(BaseModel):
    username: str
    password: str