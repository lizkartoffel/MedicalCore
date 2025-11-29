from sqlmodel import Field
from typing import Optional, List
from .base import BaseModel 

class Company(BaseModel, table=True):
    
    name: str = Field(index=True, unique=True, nullable=False)
    description: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None