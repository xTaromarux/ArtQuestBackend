import uuid as _uuid
import pydantic as _pydantic

class _BaseProgress(_pydantic.BaseModel):
    implementation_stage: int
    picture_id: _uuid.UUID
    exercises_id: _uuid.UUID
    user_id: _uuid.UUID

class Progress(_BaseProgress):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreateProgress(_BaseProgress):
    pass
