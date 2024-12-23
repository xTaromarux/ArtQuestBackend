from pydantic import BaseModel
from uuid import UUID

class DifficultiesBase(BaseModel):
    level: int
    color: str
    experience: int

class DifficultiesCreate(DifficultiesBase):
    pass

class Difficulties(DifficultiesBase):
    id: UUID
