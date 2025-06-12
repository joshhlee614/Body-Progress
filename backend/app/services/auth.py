from fastapi import HTTPException, status
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_service_key:
    raise ValueError("Missing required environment variables: SUPABASE_URL and/or SUPABASE_SERVICE_KEY")

supabase: Client = create_client(supabase_url, supabase_service_key)

async def verify_token(token: str) -> str:
    """
    Verify the JWT token and return the user ID if valid
    """
    try:
        # verify the token with Supabase
        response = supabase.auth.get_user(token)
        user = getattr(response, 'user', None)
        if not user or not getattr(user, 'id', None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        return user.id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}"
        ) 