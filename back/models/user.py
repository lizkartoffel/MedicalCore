from typing import List, Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from enum import Enum

# Placeholder for BaseModel (replace with actual base class if available)
class BaseModel(SQLModel):
    id: Optional[str] = Field(default=None, primary_key=True)


class UserRole(str, Enum):
    CUSTOMER = "customer"
    DISTRIBUTOR = "distributor"

class User(BaseModel, table=True):
    """Database model for a User."""
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    subscription_active: bool = Field(default=False)
    is_premium: bool = Field(default=False)
    # Single Role (for simpler legacy access)
    role: UserRole = Field(default=UserRole.CUSTOMER)
    # Multiple Roles list (for robust RBAC using JSON storage)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    # sa_column=Column(JSON) tells SQLAlchemy to store the list as JSON.

# --- Schemas for CRUD operations ---

class UserCreate(SQLModel):
    """Schema for user creation (signup)."""
    username: str
    email: str
    password: str  
    full_name: Optional[str] = None
    role: UserRole.CUSTOMER # Used to populate the 'roles' list on creation

class UserRead(SQLModel):
    """Schema for reading basic user details."""
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_premium: bool
    # FIXED: Roles list is crucial for client-side RBAC and is now included.
    roles: List[str] 

class UserUpdate(SQLModel): 
    """Schema for updating user details (requires admin or user self-update)."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    # Allows admin to update the list of roles
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
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    roles: List[str]

# from typing import List, Optional
# from sqlmodel import SQLModel, Field, Column
# from sqlalchemy import JSON
# from models.base import BaseModel
# from enum import Enum


# class UserRole(str, Enum):
#     CUSTOMER = "customer"
#     DISTRIBUTOR = "distributor"

# class User(BaseModel, table=True):

#     username: str = Field(index=True, unique=True, nullable=False)
#     email: str = Field(index=True, unique=True, nullable=False)
#     hashed_password: str = Field(nullable=False)
#     full_name: Optional[str] = None
#     is_active: bool = Field(default=True)
#     subscription_active: bool = Field(default=False)
#     is_premium: bool = Field(default=False)
#     role: UserRole = Field(default=UserRole.CUSTOMER)
#     roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
#     #sa_column=Column(JSON) tells SQLAlchemy to store the list as JSON.

# #-------------------------------------------------------------------------------

# class UserCreate(SQLModel):
#     username: str
#     email: str
#     password: str  
#     full_name: Optional[str] = None
#     role: UserRole

# class UserRead(SQLModel):
#     id: int
#     username: str
#     email: str
#     full_name: Optional[str] = None
#     is_active: bool
#     is_premium: bool
#     # roles: List[str] 

# class UserUpdate(SQLModel): 
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     is_active: Optional[bool] = None
#     roles: Optional[List[str]] = None

# class UserLogin(SQLModel):
#     email: str
#     password: str  # In a real application, ensure this is hashed and handled securely

# class UserPasswordReset(SQLModel):
#     email: str
#     new_password: str  # In a real application, ensure this is hashed and handled securely

# class UserProfile(SQLModel):
#     id: int
#     username: str
#     email: str
#     full_name: Optional[str] = None
#     roles: List[str]