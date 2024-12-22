from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.achievements import Achievements

router = APIRouter()

@router.get("/achievements", response_model=List[dict])
def get_all_achievements(db: Session = Depends(get_db)):
    """
    Pobiera listę wszystkich osiągnięć z tabeli achievements.
    """
    # Pobranie wszystkich rekordów z tabeli achievements
    achievements = db.query(Achievements).all()

    # Przygotowanie odpowiedzi jako lista słowników
    response = [
        {
            "id": achievement.id,
            "experience": achievement.experience,
            "picture_id": achievement.picture_id
        }
        for achievement in achievements
    ]

    return response
