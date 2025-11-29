from typing import Optional, List
from .base import BaseModel 
from sqlmodel import SQLModel, Field

class Product(BaseModel, table=True):
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = None
    price: float = Field(nullable=False)
    stock_quantity: int = Field(default=0, nullable=False)
    is_active: bool = Field(default=True)
    company_id: Optional[str] = Field(default=None, foreign_key="company.id")
    limit: int = Field(default=10, nullable=False)
    owner_id: str = Field(foreign_key="user.id", nullable=False)
 
 
 
    # added fee if more need to be posted

class ProductCreate(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    company_id: Optional[str] = None
    limit: int = 10  # Default limit for pagination

class ProductRead(SQLModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    is_active: bool
    company_id: Optional[str] = None
    limit: int = 10  # Default limit for pagination

class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    company_id: Optional[str] = None
    limit: Optional[int] = None  # Allow updating the limit for pagination

#-------------------------------------------------------------------------------