import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = {'schema': 'public'}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('public.users.id'), nullable=False)
    photo_url = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)

    # relationship to user - using string reference to avoid circular import
    user = relationship("User", back_populates="photos", lazy="selectin") 