from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UsersBase(BaseModel):
    login: str
    mail: str
    user_name: str
    group: Optional[str] = None

class UsersMinimalResponse(BaseModel):
    id: UUID
    login: str
    mail: str
    user_name: str

class UsersCreate(UsersBase):
    pass

class Users(UsersBase):
    id: UUID
