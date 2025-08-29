from app.db.depend import get_session  # type: ignore
from typing import Generic, TypeVar, Type
from sqlmodel import SQLModel, select
from dataclasses import dataclass
from fastapi import HTTPException, status
from datetime import datetime
from app.endpoints.base.pagination import (  # typing: ignore
    PaginationResponse,
)  # typing: ignore
from sqlmodel import func, Session
from app.logger.logger import logger  # type: ignore

T = TypeVar("T", bound=SQLModel)


@dataclass
class BaseController(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T], session: Session = next(get_session())):
        self.session = next(get_session())
        self.model = model
        logger.info(f"Initialized BaseController with model: {self.model.__name__}")

    async def get(self, id):
        try:
            logger.info(f"Fetching {self.model.__name__} with ID: {id}")
            query = select(self.model).where(self.model.id == id)
            return self.session.exec(query).first()
        except Exception:
            return False

    async def create(self, data: T) -> bool | T:
        try:
            logger.info(f"Fetching {self.model.__name__} with ID: {id}")
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
        logger.info(f"Updating {self.model.__name__} with ID: {id}")
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
            logger.info(f"Deleting {self.model.__name__} with ID: {id}")
            query = select(self.model).where(self.model.id == id)
            object = self.session.exec(query).first()
            self.session.delete(object)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            return False

    async def read(self, page: int, per_page: int) -> PaginationResponse[T]:
        logger.info(
            f"Reading {self.model.__name__} with pagination: page={page}, per_page={per_page}"
        )
        offset = (page - 1) * per_page
        query = select(self.model)
        total = self.session.exec(select(func.count()).select_from(query)).one()
        data = self.session.exec(query.offset(offset).limit(per_page)).all()
        return PaginationResponse[T](
            data=data,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(
                total // per_page + (1 if total % per_page > 0 else 0)
            ),  # Calculate total pages
        )
