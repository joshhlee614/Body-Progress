from fastapi import APIRouter
from app.api.photos.endpoints import router as photos_endpoints

router = APIRouter()
router.include_router(photos_endpoints) 