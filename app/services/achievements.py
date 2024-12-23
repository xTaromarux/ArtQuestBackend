from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Achievements

router = APIRouter()

@router.get("/achievements", response_model=List[dict])
def get_all_achievements(db: Session = Depends(get_db)):
    """
    Retrieves a list of all achievements from the achievements table.
    """
    # Retrieve all records from the achievements table
    achievements = db.query(Achievements).all()

    # Preparing a response as a dictionary list
    response = [
        {
            "id": achievement.id,
            "experience": achievement.experience,
            "picture_id": achievement.picture_id
        }
        for achievement in achievements
    ]

    return response
