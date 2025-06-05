from pydantic import BaseModel


class AssignRollsData(BaseModel):
     user_id:int
     roll_id:int