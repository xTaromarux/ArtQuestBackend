from pydantic import BaseModel
from uuid import UUID

class UserAchievementsBase(BaseModel):
    user_id: UUID
    achievement_id: UUID

class UserAchievementsCreate(UserAchievementsBase):
    pass

class UserAchievementsResponse(UserAchievementsBase):
    id: UUID

    class Config:
        orm_mode = True
