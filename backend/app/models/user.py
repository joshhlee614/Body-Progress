from sqlalchemy import Column, String, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'auth'}  # use Supabase's auth schema

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    is_sso_user = Column(Boolean, nullable=False, default=False)
    is_anonymous = Column(Boolean, nullable=False, default=False) 