from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UsersBase(BaseModel):
    login: str
    mail: str
    user_name: str
    group: Optional[str] = None

class UsersMinimalResponse(BaseModel):
    login: str
    mail: str
    user_name: str

    class Config:
        from_attributes = True

class UsersCreate(UsersBase):
    pass

class Users(UsersBase):
    id: UUID

    class Config:
        from_attributes = True
