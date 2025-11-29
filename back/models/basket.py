from sqlmodel import Field
from typing import Optional, List   
from .base import BaseModel

# class Basket(BaseModel, table=True):
#     user_id: int = Field(foreign_key="user.id", nullable=False)  # Foreign key to User model
#     product_ids: List[int] = Field(default_factory=list)  # List of product IDs in the basket
#     is_active: bool = Field(default=True, nullable=False)  # Status of the basket
#     tags: List[str] = Field(default_factory=list)  # List of tags associated with the basket