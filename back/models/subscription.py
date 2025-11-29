from sqlmodel import Field
from typing import Optional, List
from .base import BaseModel , datetime


# class Subscription(BaseModel, table=True):
#     user_id: int = Field(foreign_key="user.id", nullable=False)  # Foreign key to User model
#     plan: str = Field(index=True, nullable=False)  # Subscription plan name
#     start_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#     end_date: Optional[datetime] = None  # End date of the subscription
#     is_active: bool = Field(default=True, nullable=False)  # Status of the subscription
#     tags: List[str] = Field(default_factory=list)  # List of tags associated with the subscription