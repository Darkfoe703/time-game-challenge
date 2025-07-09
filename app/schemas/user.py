from pydantic import BaseModel, EmailStr
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    username: str
    email: EmailStr


# properties to receive via POST on registration
class UserCreate(UserBase):
    password: str


# Properties returned via API
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        model_config = {
            "from_attributes": True
        }  # Allows ORM objects to be returned as Pydantic models TODO: OJO con la v2!!!
