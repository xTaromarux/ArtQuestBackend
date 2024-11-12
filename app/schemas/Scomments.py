from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CommentsBase(BaseModel):
    description: str
    reactions: int
    user_id: UUID
    post_id: UUID

    class Config:
        from_attributes = True

class CommentsCreate(CommentsBase):
    pass

class Comments(CommentsBase):
    id: UUID
    date_added: datetime
    date_updated: datetime

    class Config:
        from_attributes = True