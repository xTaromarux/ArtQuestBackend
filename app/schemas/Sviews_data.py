from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ViewsDataBase(BaseModel):
    description: str
    view_id: UUID

    class Config:
        from_attributes = True

class ViewsDataCreate(ViewsDataBase):
    pass

class ViewsDataUpdate(ViewsDataBase):
    pass

class ViewsData(ViewsDataBase):
    id: UUID

    class Config:
        from_attributes = True
