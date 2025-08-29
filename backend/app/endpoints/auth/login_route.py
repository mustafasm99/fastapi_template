from fastapi import  HTTPException , status , APIRouter , Form
from app.models.types.auth_types import LoginForm , UserCreate , Change_password , SetNewPassword
from ..base.base_response import BaseResponse , TokenResponse
from app.controller.auth import authentication , user , admin
from app.db.depend import db_connection


router = APIRouter()

@router.post("/login")
async def login(
     session:db_connection,
     username:str = Form(...),
     password:str = Form(...),
     )->TokenResponse:
     login_form:LoginForm = LoginForm(
          username=username,
          password=password
     )
     token = authentication.login(
          data=login_form,
          session=session
     )
     if token:
          return TokenResponse(
               token_type="Bearer",
               access_token=token
          )
     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")

@router.post("/register")
async def register(
     session:db_connection,
     data:UserCreate,
     ):
     Newuser = authentication.CreateUser(data=data,session=session)
     return Newuser

@router.post("/change_password")
async def change_password(
     session:db_connection,
     user:user,
     data:Change_password
     ):
     authentication.change_password(
          data=data,
          user_id=user.id,
          session=session,
     )
     return BaseResponse(
          message="Password Changed",
          data=None
     )

@router.post("/set-new-password")
async def set_new_password(
     session:db_connection,
     data:SetNewPassword,
     user:admin,
     ):
     authentication.reset_password(
          session=session,
          data=data,
     )
     return BaseResponse(
          message="Password Changed",
          data=None
     )