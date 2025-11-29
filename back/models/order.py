from sqlmodel import Field
from typing import Optional, List
from .base import BaseModel 

# class Order(BaseModel, table=True):
    
#     order_number: str = Field(index=True, unique=True, nullable=False)
#     user_id: int = Field(foreign_key="user.id", nullable=False)  # Foreign key to User
#     product_ids: List[int] = Field(default_factory=list)  # List of product IDs in the order
#     total_amount: float = Field(nullable=False)
#     status: str = Field(default="pending")  # e.g., pending, shipped, delivered, cancelled
#     shipping_address: Optional[str] = None
#     billing_address: Optional[str] = None