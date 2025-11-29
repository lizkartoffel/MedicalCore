from sqlmodel import Field
from typing import Optional, List
from .base import BaseModel 

# class Category(BaseModel, table=True):
#     """Category model representing product categories."""
#     name: str = Field(index=True, unique=True, nullable=False)
#     description: Optional[str] = None
#     parent_id: Optional[int] = Field(default=None, foreign_key="category.id")  # Self-referential foreign key for sub-categories
