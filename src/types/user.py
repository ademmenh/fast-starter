from datetime import datetime
from  pydantic import BaseModel

from src.types.gender import Gender

class User (BaseModel):
    banned: bool
    disactivated: bool

    id: int
    name: str
    lastname: str
    username: str
    date_of_birth: datetime
    email: str
    gender: Gender
