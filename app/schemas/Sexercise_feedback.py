from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ExerciseFeedbackBase(BaseModel):
    message: str
    user_id: UUID
    exercise_id: UUID
    picture_id: Optional[UUID]  
    
class ExerciseFeedbackCreate(ExerciseFeedbackBase):
    pass

class ExerciseFeedback(ExerciseFeedbackBase):
    id: UUID
