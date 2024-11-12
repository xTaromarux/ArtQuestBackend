import uuid as _uuid
import pydantic as _pydantic
import datetime as _dt

class _BaseUsers(_pydantic.BaseModel):
    group: str
    mail: str
    login: str
    password: str
    date_added: _dt.date
    date_updated: _dt.date

class Users(_BaseUsers):
    id: _uuid.UUID

    class Config:
        orm_mode = True

class CreateUsers(_BaseUsers):
    pass
