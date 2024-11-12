from pydantic import BaseModel
from uuid import UUID

class DifficultyBase(BaseModel):
    name: str
    color: str
    score: int

    class Config:
        from_attributes = True

class DifficultyCreate(DifficultyBase):
    pass

class Difficulty(DifficultyBase):
    id: UUID

    class Config:
        from_attributes = True
