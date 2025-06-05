from pydantic import BaseModel

class LoginForm(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
     email:str
     password:str
     name:str



class Change_password(BaseModel):
     old_password:str
     new_password:str
     confirm_password:str
     
class SetNewPassword(Change_password):
    user_id:int