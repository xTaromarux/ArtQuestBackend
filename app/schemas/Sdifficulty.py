import uuid as _uuid
import pydantic as _pydantic

class _BaseDifficulty(_pydantic.BaseModel):
    name: str
    color: str
    score: int

class Difficulty(_BaseDifficulty):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreateDifficulty(_BaseDifficulty):
    pass
