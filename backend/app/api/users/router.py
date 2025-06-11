from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_service_key:
    raise ValueError("Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_service_key)

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create user in Supabase Auth
        auth_response = supabase.auth.admin.create_user({
            "email": user_data.email,
            "password": "temp_password_123",  # Temporary password
            "email_confirm": True
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to create user in Supabase")
        
        # Create user in our database
        db_user = User(
            id=auth_response.user.id,
            email=user_data.email,
            full_name=user_data.full_name
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        return UserResponse(
            id=db_user.id,
            email=db_user.email,
            full_name=db_user.full_name
        )
        
    except Exception as e:
        # If user was created in Supabase but failed in our DB, clean up
        if 'auth_response' in locals() and auth_response.user:
            try:
                supabase.auth.admin.delete_user(auth_response.user.id)
            except:
                pass
        raise HTTPException(status_code=400, detail=str(e)) 