from fastapi import APIRouter, Depends
from models import UserCreate, UserLogin
from db.session import supabase
from core.security import get_current_user

"""This module handles user authentication routes such as signup and login using Supabase.
"""
    # if not cred:
    #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="missing or invalid token")
    # token = cred.credentials.strip()
    # if token.lower().startswith("bearer "):
    #     token = token[7:].strip() #check if the token starts with "Bearer " and remove it to get the actual token value.

    # response = supabase.auth.get_user(token)
    # if not response:
    #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="invalid token or user not found")
    
    # return {"email": response.user.email, "id": response.user.id}

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(data: UserCreate):
    response = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password,
    })
    return response

@router.post("/login")
async def login(data: UserLogin):
    response = supabase.auth.sign_in_with_password({
        "email": data.email,
        "password": data.password,
    })
    return response

@router.get("/me")
async def read_current_user(user = Depends(get_current_user)):
    return user