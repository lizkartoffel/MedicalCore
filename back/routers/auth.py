from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from models import User, UserCreate, UserLogin
from db.session import get_session

"""This module handles user authentication routes such as signup and login using JWT tokens.
No Supabase - pure FastAPI authentication.
"""

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-change-this-in-production-use-env-variable"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """Get the current authenticated user from JWT token"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = session.exec(select(User).where(User.email == email)).first()
    
    if user is None:
        raise credentials_exception
    
    return user


@router.post("/signup")
async def signup(data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username is taken
    existing_username = session.exec(
        select(User).where(User.username == data.username)
    ).first()
    
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_password = get_password_hash(data.password)
    
    new_user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        role=data.role,
        is_active=True
    )
    
    # Store hashed password (add password field to User model)
    # For now, we'll store it as a custom attribute
    new_user.hashed_password = hashed_password
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(data: UserLogin, session: Session = Depends(get_session)):
    """Login user and return JWT token"""
    
    # Find user by email
    user = session.exec(select(User).where(User.email == data.email)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not hasattr(user, 'hashed_password'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not properly configured"
        )
    
    if not verify_password(data.password, user.hashed_password):
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
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        },
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
async def read_current_user(user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "subscription_active": user.subscription_active,
        "is_premium": user.is_premium
    }


@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {
        "message": "Logged out successfully. Please remove the token from client storage."
    }
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