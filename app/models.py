from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str


class UserInDB(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: str
    email: str
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
