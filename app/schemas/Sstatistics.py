from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class StatisticsBase(BaseModel):
    experience: int
    level: int
    courses: int
    start_strike: datetime
    end_strike: datetime
    user_id: UUID

    class Config:
        from_attributes = True

class StatisticsCreate(StatisticsBase):
    pass

class Statistics(StatisticsBase):
    id: UUID

    class Config:
        from_attributes = True
