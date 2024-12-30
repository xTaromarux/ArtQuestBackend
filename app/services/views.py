from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID
from database import get_db
import tempfile
from models import Views, Views_data, Views_pictures, Pictures, Courses

router = APIRouter()

@router.get("/view_details/{exercise_id}", response_model=dict)
def get_view_details(exercise_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Retrieves view details based on exercise_id, including template, ai_part, next_view_id, previous_view_id,
    descriptions, short descriptions and links to images with their picture_id.
    """
    view = db.query(Views).filter(Views.exercise_id == exercise_id).first()
    if not view:
        raise HTTPException(status_code=404, detail="View not found")

    descriptions_data = db.query(Views_data.description, Views_data.short_description).filter(Views_data.view_id == view.id).all()
    descriptions = [desc[0] for desc in descriptions_data]
    short_descriptions = [desc[1] for desc in descriptions_data if desc[1] is not None]

    picture_data = db.query(Views_pictures.picture_id).filter(Views_pictures.view_id == view.id).all()
    picture_urls = [
        {
            "picture_id": pic_id[0],
            "url": str(request.url_for("get_view_picture", picture_id=pic_id[0]))
        }
        for pic_id in picture_data
    ]

    response = {
        "id":view.id,
        "template": view.template,
        "ai_part": view.ai_part,
        "next_view_id": view.next_view_id,
        "previous_view_id": view.previous_view_id,
        "descriptions": descriptions,
        "short_descriptions": short_descriptions,
        "picture_urls": picture_urls  
    }
    
    return response

@router.get("/view_details_by_id/{id}", response_model=dict)
def get_view_details_by_id(id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Retrieves view details based on view_id, including template, ai_part, next_view_id, previous_view_id,
    descriptions, short descriptions, and links to images with their picture_id.
    """
    # Fetch the view using the provided id
    view = db.query(Views).filter(Views.id == id).first()
    if not view:
        raise HTTPException(status_code=404, detail="View not found")

    # Retrieve descriptions and short descriptions from the related table
    descriptions_data = db.query(Views_data.description, Views_data.short_description).filter(Views_data.view_id == view.id).all()
    descriptions = [desc[0] for desc in descriptions_data]
    short_descriptions = [desc[1] for desc in descriptions_data if desc[1] is not None]

    # Retrieve image data and generate URLs
    picture_data = db.query(Views_pictures.picture_id).filter(Views_pictures.view_id == view.id).all()
    picture_urls = [
        {
            "picture_id": pic_id[0],
            "url": str(request.url_for("get_view_picture", picture_id=pic_id[0]))
        }
        for pic_id in picture_data
    ]

    # Prepare the response
    response = {
        "id": view.id,
        "template": view.template,
        "ai_part": view.ai_part,
        "next_view_id": view.next_view_id,
        "previous_view_id": view.previous_view_id,
        "descriptions": descriptions,
        "short_descriptions": short_descriptions,
        "picture_urls": picture_urls  
    }

    return response

@router.get("/view_picture/{picture_id}", response_class=FileResponse)
def get_view_picture(picture_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the image associated with the picture_id in JPG format.
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
    Retrieves course details based on exercise_id, including template, experience, points and image link.
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
