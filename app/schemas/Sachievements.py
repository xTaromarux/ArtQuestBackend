from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AchievementsBase(BaseModel):
    experience: int
    picture_id: UUID

    class Config:
        from_attributes = True

class AchievementsCreate(AchievementsBase):
    pass

class AchievementsUpdate(AchievementsBase):
    pass

class Achievements(AchievementsBase):
    id: UUID

    class Config:
        from_attributes = True
