from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models.difficulty import Difficulty as DifficultyModel
from schemas.Sdifficulty import Difficulty as DifficultySchema, DifficultyCreate

router = APIRouter()


@router.get("/difficulties", response_model=List[DifficultySchema])
def read_difficulties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    difficulties = db.query(DifficultyModel).offset(skip).limit(limit).all()
    return difficulties