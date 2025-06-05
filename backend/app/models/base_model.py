from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class DbBaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: datetime = Field(default_factory=datetime.utcnow)
