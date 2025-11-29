from typing import List, Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from models.base import BaseModel
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    DISTRIBUTOR = "distributor"

class User(BaseModel, table=True):

    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    subscription_active: bool = Field(default=False)
    is_premium: bool = Field(default=False)
    role: UserRole = Field(default=UserRole.CUSTOMER)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    #sa_column=Column(JSON) tells SQLAlchemy to store the list as JSON.

#-------------------------------------------------------------------------------

class UserCreate(SQLModel):
    username: str
    email: str
    password: str  
    full_name: Optional[str] = None
    role: UserRole

class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    # roles: List[str] 

class UserUpdate(SQLModel): 
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    roles: Optional[List[str]] = None

class UserLogin(SQLModel):
    email: str
    password: str  # In a real application, ensure this is hashed and handled securely

class UserPasswordReset(SQLModel):
    email: str
    new_password: str  # In a real application, ensure this is hashed and handled securely

class UserProfile(SQLModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    roles: List[str]