from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID
from typing import Optional
from database import get_db
from models.user_course import User_course
from models.courses import Courses
from models.pictures import Pictures
from models.difficulties import Difficulties
import tempfile
import os

router = APIRouter()

@router.get("/courses/{user_id}", response_model=list[dict])
def get_courses_by_user_id(user_id: UUID, db: Session = Depends(get_db)):
    """
    Pobiera listę kursów przypisanych do danego użytkownika (user_id) wraz z user_course_id.
    """
    # Pobranie powiązanych kursów użytkownika z tabeli user_course
    user_courses = db.query(User_course).filter(User_course.user_id == user_id).all()

    if not user_courses:
        raise HTTPException(status_code=404, detail="No courses found for the user")

    # Przygotowanie listy obiektów zawierających course_id i user_course_id
    courses = [{"course_id": uc.course_id, "user_course_id": uc.id} for uc in user_courses]

    return courses


@router.get("/course_details/{course_id}", response_model=dict)
def get_course_details(course_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły kursu na podstawie course_id, w tym tytuł, opis, poziom trudności oraz link do obrazu.
    """
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    difficulty = db.query(Difficulties).filter(Difficulties.id == course.difficulty_id).first()
    if not difficulty:
        raise HTTPException(status_code=404, detail="Difficulty not found")

    picture_url = str(request.url_for("get_course_picture", course_id=course_id))  # Konwersja URL na string

    response = {
        "course": {
            "id": course.id,
            "title": course.title,
            "description": course.description
        },
        "difficulty": {
            "level": difficulty.level,
            "color": difficulty.color,
            "experience": difficulty.experience
        },
        "picture_url": picture_url
    }
    
    return response


@router.get("/course_picture/{course_id}", response_class=FileResponse)
def get_course_picture(course_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz kursu w formacie JPG na podstawie course_id.
    """
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course or not course.picture_id:
        raise HTTPException(status_code=404, detail="Course or Picture not found")
    
    picture = db.query(Pictures).filter(Pictures.id == course.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")


@router.get("/all_courses_details", response_model=list[dict])
def get_all_courses_details(request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły wszystkich kursów, w tym id, title, description, poziom trudności oraz link do obrazu.
    """
    courses = db.query(Courses).all()
    response = []
    for course in courses:
        difficulty = db.query(Difficulties).filter(Difficulties.id == course.difficulty_id).first()
        if not difficulty:
            continue

        picture_url = str(request.url_for("get_course_picture", course_id=course.id)) if course.picture_id else None

        course_details = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "difficulty_level": difficulty.level,
            "picture_url": picture_url
        }
        response.append(course_details)

    return response


@router.get("/course_details_by_id/{course_id}", response_model=dict)
def get_course_details_by_id(course_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły pojedynczego kursu na podstawie course_id, w tym id, title, description, poziom trudności oraz link do obrazu.
    """
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    difficulty = db.query(Difficulties).filter(Difficulties.id == course.difficulty_id).first()
    if not difficulty:
        raise HTTPException(status_code=404, detail="Difficulty not found")

    picture_url = str(request.url_for("get_course_picture", course_id=course.id)) if course.picture_id else None

    course_details = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "difficulty_level": difficulty.level,
        "picture_url": picture_url
    }

    return course_details

@router.put("/courses/{course_id}/edit", response_model=dict)
def update_course(
    course_id: UUID,
    title: Optional[str] = Form(None),
    short_description: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    experience: Optional[int] = Form(None),
    points: Optional[int] = Form(None),
    difficulty_id: Optional[UUID] = Form(None),
    picture_id: Optional[UUID] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Edytuje informacje o kursie w tabeli courses na podstawie course_id.
    """
    # Pobranie istniejącego kursu
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Aktualizacja pól tylko jeśli zostały przekazane
    if title is not None:
        course.title = title
    if short_description is not None:
        course.short_description = short_description
    if description is not None:
        course.description = description
    if experience is not None:
        course.experience = experience
    if points is not None:
        course.points = points
    if difficulty_id is not None:
        course.difficulty_id = difficulty_id
    if picture_id is not None:
        course.picture_id = picture_id

    # Zapisanie zmian w bazie danych
    db.commit()
    db.refresh(course)

    return {
        "message": "Course updated successfully",
        "course_id": str(course.id),
        "updated_fields": {
            "title": title,
            "short_description": short_description,
            "description": description,
            "experience": experience,
            "points": points,
            "difficulty_id": difficulty_id,
            "picture_id": picture_id
        }
    }