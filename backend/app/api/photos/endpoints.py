from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.models.photo import Photo
from app.models.user import User
from app.schemas.photo import PhotoCreate, PhotoResponse
from app.services.database import get_db

router = APIRouter()

@router.post("/upload", response_model=PhotoResponse)
async def upload_photo(photo: PhotoCreate, db: AsyncSession = Depends(get_db)):
    # verify user exists
    user = await db.get(User, photo.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # create photo entry
    db_photo = Photo(
        user_id=photo.user_id,
        photo_url=photo.photo_url,
        notes=photo.notes
    )
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    
    return db_photo

@router.get("/{user_id}", response_model=List[PhotoResponse])
async def get_user_photos(user_id: UUID, db: AsyncSession = Depends(get_db)):
    # verify user exists
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # get all photos for user
    result = await db.execute(select(Photo).where(Photo.user_id == user_id))
    photos = result.scalars().all()
    return photos 