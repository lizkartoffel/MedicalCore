from typing import List, Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from enum import Enum
from .base import BaseModel


class UserRole(str, Enum):
    CUSTOMER = "customer"
    DISTRIBUTOR = "distributor"
    ADMIN = "admin"  # 💡 Recommended: Add ADMIN role for management


class User(BaseModel, table=True):
    """Database model for a User."""
    
    # 🐛 FIX 1: Set ID as Optional[int] and Primary Key
    # Assuming BaseModel doesn't handle the primary key 'id' field
    id: Optional[int] = Field(default=None, primary_key=True) 

    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    subscription_active: bool = Field(default=False)
    is_premium: bool = Field(default=False)
    
    # Single Role
    role: UserRole = Field(default=UserRole.CUSTOMER)
    
    # Multiple Roles list (for robust RBAC using JSON storage)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))


# --- Schemas for CRUD operations ---

class UserCreate(SQLModel):
    """Schema for user creation (signup)."""
    username: str
    email: str
    password: str  
    full_name: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserRead(SQLModel):
    """Schema for reading basic user details."""
    # 🐛 FIX 2: Change id type from str to int
    id: int 
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_premium: bool
    roles: List[str]


class UserUpdate(SQLModel): 
    """Schema for updating user details (requires admin or user self-update)."""
    # NOTE: You may want to restrict role/roles updates to ADMIN only in your router logic.
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str 


class UserPasswordReset(SQLModel):
    """Schema for password reset requests."""
    email: str
    new_password: str 


class UserProfile(SQLModel):
    """Schema for displaying a full user profile."""
    # 🐛 FIX 3: Change id type from str to int
    id: int 
    username: str
    email: str
    full_name: Optional[str] = None
    roles: List[str]

# --- OLD CODE FOR REFERENCE ---


#     from typing import List, Optional
# from sqlmodel import SQLModel, Field, Column
# from sqlalchemy import JSON
# from enum import Enum
# from .base import BaseModel


# class UserRole(str, Enum):
#     CUSTOMER = "customer"
#     DISTRIBUTOR = "distributor"


# class User(BaseModel, table=True):
#     """Database model for a User."""
#     username: str = Field(index=True, unique=True, nullable=False)
#     email: str = Field(index=True, unique=True, nullable=False)
#     hashed_password: str = Field(nullable=False)
#     full_name: Optional[str] = None
#     is_active: bool = Field(default=True)
#     subscription_active: bool = Field(default=False)
#     is_premium: bool = Field(default=False)
#     # Single Role (for simpler legacy access)
#     role: UserRole = Field(default=UserRole.CUSTOMER)
#     # Multiple Roles list (for robust RBAC using JSON storage)
#     roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))


# # --- Schemas for CRUD operations ---

# class UserCreate(SQLModel):
#     """Schema for user creation (signup)."""
#     username: str
#     email: str
#     password: str  
#     full_name: Optional[str] = None
#     role: UserRole = UserRole.CUSTOMER  # FIXED: This was the syntax error!


# class UserRead(SQLModel):
#     """Schema for reading basic user details."""
#     id: str
#     username: str
#     email: str
#     full_name: Optional[str] = None
#     is_active: bool
#     is_premium: bool
#     roles: List[str]


# class UserUpdate(SQLModel): 
#     """Schema for updating user details (requires admin or user self-update)."""
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     is_active: Optional[bool] = None
#     roles: Optional[List[str]] = None


# class UserLogin(SQLModel):
#     """Schema for user login."""
#     email: str
#     password: str 


# class UserPasswordReset(SQLModel):
#     """Schema for password reset requests."""
#     email: str
#     new_password: str 


# class UserProfile(SQLModel):
#     """Schema for displaying a full user profile."""
#     id: str
#     username: str
#     email: str
#     full_name: Optional[str] = None
#     roles: List[str]