from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models.progress import Progress as ProgressModel
from schemas.Sprogress import Progress as ProgressSchema, ProgressCreate

router = APIRouter()

@router.post("/progress", response_model=ProgressSchema)
def create_progress(progress: ProgressCreate, db: Session = Depends(get_db)):
    db_progress = ProgressModel(
        id=uuid.uuid4(),
        score=progress.score,
        description=progress.description,
        user_id=progress.user_id,
        exercise_id=progress.exercise_id
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.get("/progress", response_model=List[ProgressSchema])
def read_progress(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    progress_records = db.query(ProgressModel).offset(skip).limit(limit).all()
    return progress_records

@router.get("/progress/{progress_id}", response_model=ProgressSchema)
def read_progress_by_id(progress_id: uuid.UUID, db: Session = Depends(get_db)):
    progress = db.query(ProgressModel).filter(ProgressModel.id == progress_id).first()
    if progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress

@router.delete("/progress/{progress_id}", response_model=ProgressSchema)
def delete_progress(progress_id: uuid.UUID, db: Session = Depends(get_db)):
    progress = db.query(ProgressModel).filter(ProgressModel.id == progress_id).first()
    if progress is None:
        raise HTTPException(status_code=404, detail="Progress not found")
    db.delete(progress)
    db.commit()
    return progress
