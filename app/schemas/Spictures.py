import uuid as _uuid
import pydantic as _pydantic

class _BasePictures(_pydantic.BaseModel):
    blob: bytes
    description: str
    date_added: str

class Pictures(_BasePictures):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreatePictures(_BasePictures):
    pass
