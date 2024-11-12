import uuid as _uuid
import pydantic as _pydantic

class _BasePosts(_pydantic.BaseModel):
    title: str
    description: str
    state: str
    date_added: str
    date_updated: str
    picture_id: _uuid.UUID
    user_id: _uuid.UUID

class Posts(_BasePosts):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreatePosts(_BasePosts):
    pass
