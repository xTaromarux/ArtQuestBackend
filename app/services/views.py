from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID
from database import get_db
from models.views import Views
from models.views_data import Views_data
from models.views_pictures import Views_pictures
from models.pictures import Pictures
from models.courses import Courses
import tempfile
import os

router = APIRouter()

@router.get("/view_details/{exercise_id}", response_model=dict)
def get_view_details(exercise_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły widoku na podstawie exercise_id, w tym template, ai_part, next_view_id, previous_view_id,
    opisy oraz linki do obrazów.
    """
    view = db.query(Views).filter(Views.exercise_id == exercise_id).first()
    if not view:
        raise HTTPException(status_code=404, detail="View not found")

    descriptions = db.query(Views_data.description).filter(Views_data.view_id == view.id).all()
    descriptions = [desc[0] for desc in descriptions]

    picture_ids = db.query(Views_pictures.picture_id).filter(Views_pictures.view_id == view.id).all()
    picture_urls = [
        str(request.url_for("get_view_picture", picture_id=pic_id[0])) for pic_id in picture_ids
    ]

    response = {
        "template": view.template,
        "ai_part": view.ai_part,
        "next_view_id": view.next_view_id,
        "previous_view_id": view.previous_view_id,
        "descriptions": descriptions,
        "picture_urls": picture_urls
    }
    
    return response

@router.get("/view_picture/{picture_id}", response_class=FileResponse)
def get_view_picture(picture_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz związany z picture_id w formacie JPG.
    """
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")


@router.get("/course_view_details/{exercise_id}", response_model=dict)
def get_course_view_details(exercise_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły kursu na podstawie exercise_id, w tym template, experience, points oraz link do obrazu.
    """
    view = db.query(Views).filter(Views.exercise_id == exercise_id).first()
    if not view:
        raise HTTPException(status_code=404, detail="View not found")

    course = db.query(Courses).filter(Courses.id == view.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    picture_ids = db.query(Views_pictures.picture_id).filter(Views_pictures.view_id == view.id).all()
    picture_urls = [
        str(request.url_for("get_view_picture", picture_id=pic_id[0])) for pic_id in picture_ids
    ]

    response = {
        "template": view.template,
        "experience": course.experience,
        "points": course.points,
        "picture_urls": picture_urls
    }
    
    return response
