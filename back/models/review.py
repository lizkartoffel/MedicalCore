from typing import Optional
from sqlmodel import SQLModel
from .base import BaseModel 
from sqlmodel import Field

class Review(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id", nullable=False)  # Foreign key to User model
    product_id: int = Field(foreign_key="product.id", nullable=False)  # Foreign key to Product model
    rating: int = Field(nullable=False)  # Rating given by the user
    comment: Optional[str] = None  # Optional comment by the user

class ReviewCreate(SQLModel):
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

class ReviewRead(SQLModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str] = None

class ReviewUpdate(SQLModel):
    rating: Optional[int] = None
    comment: Optional[str] = None