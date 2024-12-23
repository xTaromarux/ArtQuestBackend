from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AchievementsBase(BaseModel):
    experience: int
    picture_id: Optional[UUID] 

class Achievements(AchievementsBase):
    id: UUID
