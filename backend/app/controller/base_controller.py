from app.db.depend import get_session
from typing import Generic, TypeVar, Type
from sqlmodel import SQLModel, select
from dataclasses import dataclass
from fastapi import HTTPException, status
from datetime import datetime

T = TypeVar("T", bound=SQLModel)


@dataclass
class BaseController(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.session = next(get_session())
        self.model = model

    async def get(self, id):
        try:
            query = select(self.model).where(self.model.id == id)
            return self.session.exec(query).first()
        except Exception:
            return False

    async def create(self, data: T) -> bool | T:
        try:
            self.session.add(data)
            self.session.commit()
            self.session.refresh(
                data
            )  # Refresh the object to ensure it has the latest data
            return data
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating {self.model.__name__}: {str(e)}",
            )

    async def update(self, id: int, data: T) -> bool | T:
        # Fetch the existing object
        query = select(self.model).where(self.model.id == id)
        old_object = self.session.exec(query).first()

        # If the object doesn't exist, return False
        if not old_object:
            return False

        # Update the fields of the old object with the new data
        for key, value in data.dict(exclude_unset=True).items():
            setattr(old_object, key, value)

        # Update the timestamps
        old_object.update_time = datetime.now()

        # Commit the changes to the session
        self.session.add(old_object)
        self.session.commit()

        # Return the updated object
        self.session.refresh(old_object)
        return old_object

    async def delete(self, id):
        try:
            query = select(self.model).where(self.model.id == id)
            object = self.session.exec(query).first()
            self.session.delete(object)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    async def read(self) -> list[T]:
        query = select(self.model)
        return list(self.session.exec(query).all())