from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.photo import Photo
from app.models.user import User
from app.schemas.photo import PhotoCreate, PhotoResponse
from app.services.database import get_db
from app.services.auth import verify_token

router = APIRouter()
security = HTTPBearer()

@router.post("/upload", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_photo(
    photo: PhotoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    # verify token and get user
    user_id = await verify_token(credentials.credentials)
    if str(user_id) != str(photo.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload photos for this user"
        )
    
    # verify user exists
    user = await db.get(User, photo.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # create photo entry
        db_photo = Photo(
            user_id=photo.user_id,
            photo_url=str(photo.photo_url),  # convert HttpUrl to string
            notes=photo.notes
        )
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)
        
        return db_photo
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload photo: {str(e)}"
        )

@router.get("/{user_id}", response_model=List[PhotoResponse])
async def get_user_photos(
    user_id: UUID,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    # verify token
    await verify_token(credentials.credentials)
    
    # verify user exists
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # get all photos for user
    result = await db.execute(select(Photo).where(Photo.user_id == user_id))
    photos = result.scalars().all()
    return photos 