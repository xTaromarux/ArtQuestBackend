from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models.difficulties import Difficulties as DifficultiesModel
from schemas.Sdifficulties import Difficulties as DifficultiesSchema, DifficultiesCreate

router = APIRouter()


@router.get("/difficulties", response_model=List[DifficultiesSchema])
def read_difficulties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    difficulties = db.query(DifficultiesModel).offset(skip).limit(limit).all()
    return difficulties