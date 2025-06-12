from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.models.user import UserCreate, UserResponse
from app.services.supabase import supabase

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    print(f"Received user_data: {user_data}")  # debug print
    try:
        # Create user in Supabase Auth
        auth_response = supabase.auth.admin.create_user({
            "email": user_data.email,
            "password": "temp_password_123",  # Temporary password
            "email_confirm": True
        })
        # ... existing code ...
    except Exception as e:
        # Handle exceptions and return appropriate response
        return {"error": str(e)}

    return {"message": "User registration successful"} 