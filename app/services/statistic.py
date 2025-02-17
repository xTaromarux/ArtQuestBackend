from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from models.statistics import Statistics as StatisticsModel
from models.users import Users
from schemas.Sstatistics import Statistics
from database import get_db

router = APIRouter()

@router.post("/statistics/create", response_model=Statistics)
def create_statistics(
    experience: int = Form(...),
    level: int = Form(...),
    courses: int = Form(...),
    start_strike: datetime = Form(...),
    end_strike: datetime = Form(...),
    user_id: UUID = Form(...),
    db: Session = Depends(get_db)
):
    """
    Creates a new entry in the statistics table based on the data provided.
    """
    # Checking whether the user exists
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    # Checking whether statistics for user_id already exist
    existing_statistics = db.query(StatisticsModel).filter(StatisticsModel.user_id == user_id).first()
    if existing_statistics:
        raise HTTPException(status_code=400, detail="Statistics for this user already exist")

    new_statistics = StatisticsModel(
        id=uuid4(),
        experience=experience,
        level=level,
        courses=courses,
        start_strike=start_strike,
        end_strike=end_strike,
        user_id=user_id
    )

    db.add(new_statistics)
    db.commit()
    db.refresh(new_statistics)

    return {
        "id": new_statistics.id,
        "experience": new_statistics.experience,
        "level": new_statistics.level,
        "courses": new_statistics.courses,
        "start_strike": new_statistics.start_strike,
        "end_strike": new_statistics.end_strike,
        "user_id": new_statistics.user_id,
    }


@router.put("/statistics/{user_id}/edit", response_model=Statistics)
def update_statistics(
    user_id: UUID,
    experience: Optional[int] = Form(None),
    level: Optional[int] = Form(None),
    courses: Optional[int] = Form(None),
    start_strike: Optional[datetime] = Form(None),
    end_strike: Optional[datetime] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Edits an existing entry in the statistics table based on user_id.
    """

    statistics = db.query(StatisticsModel).filter(StatisticsModel.user_id == user_id).first()
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics for this user not found")
    
    # Update fields only if passed
    if experience is not None:
        statistics.experience = experience
    if level is not None:
        statistics.level = level
    if courses is not None:
        statistics.courses = courses
    if start_strike is not None:
        statistics.start_strike = start_strike
    if end_strike is not None:
        statistics.end_strike = end_strike

    db.commit()
    db.refresh(statistics)

    return statistics
