from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models.progresses import Progresses as ProgressesModel
from schemas.Sprogresses import progresses as progressesSchema, progressesCreate

router = APIRouter()

@router.post("/progresses", response_model=progressesSchema)
def create_progresses(progresses: progressesCreate, db: Session = Depends(get_db)):
    db_progresses = ProgressesModel(
        id=uuid.uuid4(),
        score=progresses.score,
        description=progresses.description,
        user_id=progresses.user_id,
        course_id=progresses.course_id
    )
    db.add(db_progresses)
    db.commit()
    db.refresh(db_progresses)
    return db_progresses

@router.get("/progresses", response_model=List[ProgressesSchema])
def read_progresses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    progresses_records = db.query(progressesModel).offset(skip).limit(limit).all()
    return progresses_records

@router.get("/progresses/{progresses_id}", response_model=ProgressesSchema)
def read_progresses_by_id(progresses_id: uuid.UUID, db: Session = Depends(get_db)):
    progresses = db.query(progressesModel).filter(progressesModel.id == progresses_id).first()
    if progresses is None:
        raise HTTPException(status_code=404, detail="progresses not found")
    return progresses

@router.delete("/progresses/{progresses_id}", response_model=progressesSchema)
def delete_progresses(progresses_id: uuid.UUID, db: Session = Depends(get_db)):
    progresses = db.query(progressesModel).filter(progressesModel.id == progresseses_id).first()
    if progresses is None:
        raise HTTPException(status_code=404, detail="progresses not found")
    db.delete(progresses)
    db.commit()
    return progresses
