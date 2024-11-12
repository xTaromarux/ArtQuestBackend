from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from database import get_db
from models.courses import Courses as CoursesModel
from models.progresses import progresses as progressesModel
from models.pictures import Pictures as PicturesModel
from schemas.Scourses import Courses as CoursesSchema, CoursesCreate
from fastapi.responses import JSONResponse, Response

router = APIRouter()

@router.post("/courses", response_model=CoursesSchema)
def create_course(course: CoursesCreate, db: Session = Depends(get_db)):
    db_course = coursesModel(
        id=uuid.uuid4(),
        title=course.title,
        description=course.description,
        difficulty_id=course.difficulty_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses", response_model=List[CoursesSchema])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(CoursesModel).offset(skip).limit(limit).all()
    return courses

@router.get("/courses/details", response_model=List[dict])
def get_course_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.query(CoursesModel).offset(skip).limit(limit).all()
    course_details = []

    for course in courses:
        progresses = db.query(progressesModel).filter(progressesModel.course_id == course.id).first()
        pictures = db.query(PicturesModel).filter(PicturesModel.course_id == course.id).all()

        course_detail = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "difficulty_id": course.difficulty_id,
            "score": progresses.score if progresses else 0,
            "progresses_description": progresses.description if progresses else "",
            "pictures": [
                {"id": picture.id, "url": f"/api/pictures/{picture.id}"} for picture in pictures
            ] if pictures else []
        }
        course_details.append(course_detail)

    return course_details

@router.get("/pictures/{picture_id}")
def get_picture(picture_id: uuid.UUID, db: Session = Depends(get_db)):
    picture = db.query(PicturesModel).filter(PicturesModel.id == picture_id).first()
    if picture is None:
        raise HTTPException(status_code=404, detail="Picture not found")
    return Response(content=picture.picture, media_type="image/jpeg")
