from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class CommentsBase(BaseModel):
    description: str
    reactions: int
    user_id: UUID
    post_id: UUID

class Comments(CommentsBase):
    id: UUID
    date_added: datetime
    date_updated: datetime

class CommentResponse(BaseModel):
    id: UUID
    description: str
    reactions: int
    date_added: datetime
    date_updated: datetime
    user_id: UUID
    user_name: str
    login: str
    avatar_url: Optional[str] = None
