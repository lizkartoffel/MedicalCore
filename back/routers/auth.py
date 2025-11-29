from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any

# Core security and utility functions are imported from the security layer
from core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
) 

# Data models
from models.user import User, UserCreate, UserLogin
from db.session import get_session

"""
This module defines the authentication endpoints for user signup, login, 
and token-based profile retrieval (/me). It relies on the security layer 
for password hashing and JWT management.
"""

router = APIRouter(prefix="/auth", tags=["auth"])

def _get_user_response_data(user: User) -> Dict[str, Any]:
    """Helper function to format user data for response bodies."""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "roles": user.roles,
        "is_active": user.is_active,
        "subscription_active": user.subscription_active,
        "is_premium": user.is_premium,
    }

@router.post("/signup")
async def signup(data: UserCreate, session: Session = Depends(get_session)):
    """
    Registers a new user after checking for unique email and username.
    Returns the newly created user's data and a fresh JWT token.
    """
    
    # Check for existing email
    existing_user_email = session.exec(
        select(User).where(User.email == data.email)
    ).first()
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check for existing username
    existing_username = session.exec(
        select(User).where(User.username == data.username)
    ).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user instance
    hashed_password = get_password_hash(data.password)
    
    new_user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        role=data.role,
        is_active=True,
        hashed_password=hashed_password, 
        # Set the roles list based on the initial primary role
        roles=[data.role.value] 
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Generate token
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {
        "message": "User created successfully",
        "user": _get_user_response_data(new_user),
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(data: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticates user credentials. 
    Returns the user data and a JWT token on success.
    """
    
    # Find user by email
    user = session.exec(select(User).where(User.email == data.email)).first()
    
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Generate token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "message": "Login successful",
        "user": _get_user_response_data(user),
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    """
    Retrieves the current authenticated user's profile using the JWT.
    """
    return _get_user_response_data(user)


@router.post("/logout")
async def logout():
    """
    Handles client-side token removal. 
    Does not require server-side state or JWT validation.
    """
    return {
        "message": "Logged out successfully. The client must discard the stored JWT token."
    }
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlmodel import Session, select
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from typing import Optional

# from models import User, UserCreate, UserLogin
# from db.session import get_session

# """This module handles user authentication routes such as signup and login using JWT tokens.
# No Supabase - pure FastAPI authentication.
# """

# router = APIRouter(prefix="/auth", tags=["auth"])
# security = HTTPBearer()

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # JWT settings
# SECRET_KEY = "your-secret-key-change-this-in-production-use-env-variable"  # Change this!
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against its hash"""
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     """Hash a password"""
#     return pwd_context.hash(password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     """Create a JWT access token"""
#     to_encode = data.copy()
    
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     session: Session = Depends(get_session)
# ) -> User:
#     """Get the current authenticated user from JWT token"""
    
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         token = credentials.credentials
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
        
#         if email is None:
#             raise credentials_exception
            
#     except JWTError:
#         raise credentials_exception
    
#     # Get user from database
#     user = session.exec(select(User).where(User.email == email)).first()
    
#     if user is None:
#         raise credentials_exception
    
#     return user


# @router.post("/signup")
# async def signup(data: UserCreate, session: Session = Depends(get_session)):
#     """Register a new user"""
    
#     # Check if user already exists
#     existing_user = session.exec(
#         select(User).where(User.email == data.email)
#     ).first()
    
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     # Check if username is taken
#     existing_username = session.exec(
#         select(User).where(User.username == data.username)
#     ).first()
    
#     if existing_username:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username already taken"
#         )
    
#     # Create new user
#     hashed_password = get_password_hash(data.password)
    
#     new_user = User(
#         username=data.username,
#         email=data.email,
#         full_name=data.full_name,
#         role=data.role,
#         is_active=True
#     )
    
#     # Store hashed password (add password field to User model)
#     # For now, we'll store it as a custom attribute
#     new_user.hashed_password = hashed_password
    
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
    
#     # Create access token
#     access_token = create_access_token(data={"sub": new_user.email})
    
#     return {
#         "message": "User created successfully",
#         "user": {
#             "id": new_user.id,
#             "username": new_user.username,
#             "email": new_user.email,
#             "full_name": new_user.full_name,
#             "role": new_user.role
#         },
#         "access_token": access_token,
#         "token_type": "bearer"
#     }


# @router.post("/login")
# async def login(data: UserLogin, session: Session = Depends(get_session)):
#     """Login user and return JWT token"""
    
#     # Find user by email
#     user = session.exec(select(User).where(User.email == data.email)).first()
    
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password"
#         )
    
#     # Verify password
#     if not hasattr(user, 'hashed_password'):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Account not properly configured"
#         )
    
#     if not verify_password(data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password"
#         )
    
#     # Check if user is active
#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Account is disabled"
#         )
    
#     # Create access token
#     access_token = create_access_token(data={"sub": user.email})
    
#     return {
#         "message": "Login successful",
#         "user": {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "full_name": user.full_name,
#             "role": user.role
#         },
#         "access_token": access_token,
#         "token_type": "bearer"
#     }


# @router.get("/me")
# async def read_current_user(user: User = Depends(get_current_user)):
#     """Get current user information"""
#     return {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "full_name": user.full_name,
#         "role": user.role,
#         "is_active": user.is_active,
#         "subscription_active": user.subscription_active,
#         "is_premium": user.is_premium
#     }


# @router.post("/logout")
# async def logout():
#     """Logout user (client-side token removal)"""
#     return {
#         "message": "Logged out successfully. Please remove the token from client storage."
#     }
# from fastapi import APIRouter, Depends
# from models import UserCreate, UserLogin
# from db.session import supabase
# from core.security import get_current_user

# """This module handles user authentication routes such as signup and login using Supabase.
# """
#     # if not cred:
#     #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="missing or invalid token")
#     # token = cred.credentials.strip()
#     # if token.lower().startswith("bearer "):
#     #     token = token[7:].strip() #check if the token starts with "Bearer " and remove it to get the actual token value.

#     # response = supabase.auth.get_user(token)
#     # if not response:
#     #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="invalid token or user not found")
    
#     # return {"email": response.user.email, "id": response.user.id}

# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/signup")
# async def signup(data: UserCreate):
#     response = supabase.auth.sign_up({
#         "email": data.email,
#         "password": data.password,
#     })
#     return response

# @router.post("/login")
# async def login(data: UserLogin):
#     response = supabase.auth.sign_in_with_password({
#         "email": data.email,
#         "password": data.password,
#     })
#     return response

# @router.get("/me")
# async def read_current_user(user = Depends(get_current_user)):
#     return user