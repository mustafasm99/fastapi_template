from sqlmodel import Session
from app.db.engin import engin
from fastapi import Depends
from typing import Annotated


def get_session():
     
     with Session(engin) as session:
          try:
               yield session
          except:
               session.rollback()
               raise
          finally:
               session.close()
          
db_connection = Annotated[Session, Depends(get_session)]

"""
     Create in depend to inject the session into 
     All the endpoints that need database connection.

"""