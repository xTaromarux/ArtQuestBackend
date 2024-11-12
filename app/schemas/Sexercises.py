import uuid as _uuid
import pydantic as _pydantic

class _BaseExercises(_pydantic.BaseModel):
    state: str
    description: str
    title: int
    picture_id: _uuid.UUID
    difficulty_id: _uuid.UUID

class Exercises(_BaseExercises):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreateExercises(_BaseExercises):
    pass
