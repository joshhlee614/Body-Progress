from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    created_at: datetime
    is_sso_user: bool = False
    is_anonymous: bool = False

    class Config:
        from_attributes = True 