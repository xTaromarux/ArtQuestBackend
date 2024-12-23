from pydantic import BaseModel
from uuid import UUID

class ViewsDataBase(BaseModel):
    description: str
    short_description: str
    view_id: UUID

class ViewsDataCreate(ViewsDataBase):
    pass

class ViewsData(ViewsDataBase):
    id: UUID
