from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import uuid4

class BaseModel(SQLModel):
    # id: str = Field(default_factory=uuid4, primary_key=True)
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
