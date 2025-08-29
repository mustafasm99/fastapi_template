from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.models.types.auth_types import LoginForm, UserCreate , SetNewPassword , Change_password
from jose import JWTError, jwt
from datetime import timedelta, datetime
from app.core.settings import settings
from app.models.users.user import User
from app.db.depend import db_connection
from sqlmodel import Session, select
from typing import Annotated
from passlib.context import CryptContext


class Auth:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    token = Annotated[str, Depends(oauth2_scheme)]
    def get_hash_password(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict)->str:
        to_encode = data.copy()
        expire_date = datetime.utcnow() + timedelta(days=500)
        # Get user rolls from database
        to_encode.update(
            {
                "exp": expire_date,
            },
        )
        encode_jwt = jwt.encode(to_encode, settings.API_SECRET, algorithm="HS256")
        return encode_jwt

    def get_current_user(
        self, session: db_connection, token: token
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.API_SECRET, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            print("====================> JWTError")
            raise credentials_exception
        query = select(User).where(User.email == username)
        user = session.exec(query).first()
        if not user:
            raise credentials_exception
        return user

    def get_admin_user(self , session:db_connection , token:token) -> User:
        user = self.get_current_user(session=session, token=token)
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return user
    def login(self, data: LoginForm, session: Session) -> str|None:
        query = select(User).where(User.email == data.username)
        user = session.exec(query).first()

        if user and self.verify_password(
            plain_password=data.password, hashed_password=user.password
        ):
          token = self.create_access_token({
               "sub":user.email,
               "name":user.name,
               "id":user.id,
               "roll":[
                    data.roll.name
                    for data in 
                    user.users_roll          
               ]
          })
          return token
        return None

    def CreateUser(self, data: UserCreate, session: Session) -> User:
        user = User(
            email=data.email,
            password=self.get_hash_password(data.password),
            name=data.name,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def change_password(
        self,
        session: Session,
        data:Change_password,
        user_id:int
    )->bool:
        query = select(User).where(User.id == user_id)
        user = session.exec(query).first()
        if user and self.verify_password(
            plain_password=data.old_password, hashed_password=user.password
        ):
            user.password = self.get_hash_password(data.new_password)
            session.add(user)
            session.commit()
            return True
        return False
    
    def reset_password(
        self,
        session: Session,
        data:SetNewPassword,
    )->bool:
        query = select(User).where(User.id == data.user_id)
        user = session.exec(query).first()
        if user:
            user.password = self.get_hash_password(data.new_password)
            session.add(user)
            session.commit()
            return True
        return False

authentication = Auth()


user = Annotated[User, Depends(authentication.get_current_user)]
admin = Annotated[User, Depends(authentication.get_admin_user)]