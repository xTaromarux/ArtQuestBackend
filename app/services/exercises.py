from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from database import get_db
from models.exercises import Exercises as ExercisesModel
from models.progress import Progress as ProgressModel
from models.pictures import Pictures as PicturesModel
from schemas.Sexercises import Exercises as ExerciseSchema, ExercisesCreate
from fastapi.responses import JSONResponse, Response

router = APIRouter()

@router.post("/exercises", response_model=ExerciseSchema)
def create_exercise(exercise: ExercisesCreate, db: Session = Depends(get_db)):
    db_exercise = ExercisesModel(
        id=uuid.uuid4(),
        title=exercise.title,
        description=exercise.description,
        aipart=exercise.aipart,
        colSpan=exercise.colSpan,
        rowSpan=exercise.rowSpan,
        cols=exercise.cols,
        rows=exercise.rows,
        difficulty_id=exercise.difficulty_id
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/exercises", response_model=List[ExerciseSchema])
def read_exercises(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    exercises = db.query(ExercisesModel).offset(skip).limit(limit).all()
    return exercises

@router.get("/exercises/details", response_model=List[dict])
def get_exercise_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    exercises = db.query(ExercisesModel).offset(skip).limit(limit).all()
    exercise_details = []

    for exercise in exercises:
        progress = db.query(ProgressModel).filter(ProgressModel.exercise_id == exercise.id).first()
        pictures = db.query(PicturesModel).filter(PicturesModel.exercise_id == exercise.id).all()

        exercise_detail = {
            "id": exercise.id,
            "title": exercise.title,
            "description": exercise.description,
            "aipart": exercise.aipart,
            "colSpan": exercise.colSpan,
            "rowSpan": exercise.rowSpan,
            "cols": exercise.cols,
            "rows": exercise.rows,
            "difficulty_id": exercise.difficulty_id,
            "score": progress.score if progress else 0,
            "progress_description": progress.description if progress else "",
            "pictures": [
                {"id": picture.id, "url": f"/api/pictures/{picture.id}"} for picture in pictures
            ] if pictures else []
        }
        exercise_details.append(exercise_detail)

    return exercise_details

@router.get("/pictures/{picture_id}")
def get_picture(picture_id: uuid.UUID, db: Session = Depends(get_db)):
    picture = db.query(PicturesModel).filter(PicturesModel.id == picture_id).first()
    if picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    return Response(content=picture.picture, media_type="image/jpeg")
