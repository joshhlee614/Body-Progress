from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters')
        return v

    @field_validator('full_name')
    @classmethod
    def full_name_min_length(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('full name must be at least 2 characters')
        return v

class UserResponse(UserBase):
    id: UUID

    class Config:
        from_attributes = True 