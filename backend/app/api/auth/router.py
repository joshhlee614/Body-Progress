from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import LoginRequest, TokenResponse
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_service_key:
    raise ValueError("Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_service_key)

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })
        
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        return TokenResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: Request):
    try:
        # Get the refresh token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        refresh_token = auth_header.split(" ")[1]
        
        response = supabase.auth.refresh_session(refresh_token)
        
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
            
        return TokenResponse(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token,
            user_id=response.user.id
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 