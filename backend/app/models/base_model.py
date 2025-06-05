from sqlmodel import DateTime, Field, Column, Integer , SQLModel
from datetime import datetime


class DbBaseModel(SQLModel):
    id: int = Field(
        sa_column=Column(Integer, primary_key=True, index=True, autoincrement=True)
    )
    create_time: datetime = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
        )
    )
    update_time: datetime = Field(
            sa_column=Column(
               DateTime,
               default=datetime.utcnow,
               onupdate=datetime.utcnow,
            )
      )