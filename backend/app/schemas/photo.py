from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class PhotoBase(BaseModel):
    photo_url: HttpUrl  # validate that it's a proper URL
    notes: Optional[str] = None

    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v is not None and len(v.strip()) == 0:
            return None
        return v

class PhotoCreate(PhotoBase):
    user_id: UUID

class PhotoResponse(PhotoBase):
    id: UUID
    user_id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True 