from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import uuid
import base64

from database import get_db
from models.pictures import Pictures
from schemas.Spictures import Pictures as PictureSchema, PicturesCreate as PictureCreate

router = APIRouter()

def convert_to_base64(image_binary):
    return base64.b64encode(image_binary).decode('utf-8')

@router.get("/pictures", response_model=List[PictureSchema])
def read_pictures(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pictures = db.query(Pictures).offset(skip).limit(limit).all()
    for picture in pictures:
        if picture.picture:
            picture.picture = convert_to_base64(picture.picture)
    return pictures

@router.post("/pictures", response_model=PictureSchema)
async def create_picture(exercise_id: uuid.UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_content = await file.read()
    db_picture = Pictures(
        picture=file_content,
        exercise_id=exercise_id
    )
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    db_picture.picture = convert_to_base64(db_picture.picture)
    return db_picture

@router.get("/pictures/{picture_id}", response_model=PictureSchema)
def read_picture(picture_id: uuid.UUID, db: Session = Depends(get_db)):
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    if picture.picture:
        picture.picture = convert_to_base64(picture.picture)
    return picture
