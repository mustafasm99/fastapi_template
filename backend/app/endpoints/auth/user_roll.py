from fastapi import  HTTPException , status , APIRouter
from ..base.base_response import BaseResponse
from app.controller.auth import admin
from app.db.depend import db_connection
from app.controller.user_roll import RollController
from app.models.users.user import Roll
from pydantic import BaseModel


class AssignRollsData(BaseModel):
     user_id:int
     roll_id:int


router = APIRouter()

@router.post("/assign_roll")
async def assign_roll(
     session:db_connection,
     data:AssignRollsData,
     user:admin,
     ):
     roll_controller:RollController = RollController(session=session)
     if roll_controller.assign_roll(
          data=data
          ):
          return BaseResponse(
               message="Roll Assigned",
               data=data
          )
     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Roll not assigned")

@router.post("/unassign_roll")
async def unassign_roll(
     session:db_connection,
     data:AssignRollsData,
     user:admin,
     ):
     roll_controller:RollController = RollController(session=session)
     if roll_controller.unassign_roll(
          data=data
          ):
          return BaseResponse(
               message="Roll Unassigned",
               data=data
          )
     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Roll not unassigned")

@router.post("/create_roll")
async def create_roll(
     session:db_connection,
     data:Roll,
     user:admin,
     ):
     roll_controller:RollController = RollController(session=session)
     roll_controller.create_roll(data=data)
     return BaseResponse(
          message="Roll Created",
          data=data
     )

@router.get("/get_rolls")
async def get_rolls(
     session:db_connection,
     user:admin,
     ):
     roll_controller:RollController = RollController(session=session)
     rolls = roll_controller.get_rolls()
     return BaseResponse(
          message="Rolls",
          data=rolls
     )