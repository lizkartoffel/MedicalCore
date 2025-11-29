from sqlmodel import Field
from typing import Optional, List
from .base import BaseModel 

# class Listing(BaseModel, table=True):

#     title: str = Field(index=True, nullable=False)
#     description: Optional[str] = None
#     price: float = Field(nullable=False)
#     is_active: bool = Field(default=True)
#     owner_id: int = Field(foreign_key="users.id", nullable=False)  # Foreign key to User model