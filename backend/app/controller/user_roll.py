from app.models.users.user import UsersRoll , Roll
from app.db.depend import db_connection
from app.models.types.rolls_controller import AssignRollsData
from datetime import datetime
from sqlmodel import select


class RollController:
     def __init__(self , session:db_connection):
          self.session = session
     
     def assign_roll(self , data:AssignRollsData)->bool:
          try:
               new_user_roll = UsersRoll(
                    user_id = data.user_id,
                    roll_id = data.roll_id,
                    create_time= datetime.now(),
               )
               self.session.add(new_user_roll)
               self.session.commit()
               return True
          except Exception:
               return False
     
     def create_roll(self , data:Roll):
          new_roll = Roll(
               name = data.name,
               description = data.description
          )
          self.session.add(new_roll)
          self.session.commit()
          self.session.refresh(new_roll)
     
     def get_rolls(self) -> list[Roll]|None:
          return list(self.session.exec(select(Roll)).all())
     
     def unassign_roll(self , data:AssignRollsData):
          query = select(UsersRoll).where(
               UsersRoll.user_id == data.user_id and UsersRoll.roll_id == data.roll_id
          )
          user_roll = self.session.exec(query).first()
          if user_roll:
               self.session.delete(user_roll)
               self.session.commit()
          return None
     
     def delete_roll(self , data:Roll):
          query = select(Roll).where(Roll.id == data.id)
          roll = self.session.exec(query).first()
          if roll:
               self.session.delete(roll)
               self.session.commit()
          return None