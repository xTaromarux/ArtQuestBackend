from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StatisticsBase(BaseModel):
    experience: int
    level: int
    courses: int
    start_strike: datetime
    end_strike: datetime
    user_id: UUID

class StatisticsCreate(StatisticsBase):
    pass

class Statistics(StatisticsBase):
    id: UUID
