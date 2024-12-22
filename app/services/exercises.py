from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID
from database import get_db
from typing import Optional
from models.exercises import Exercises
from models.pictures import Pictures
import tempfile
import os
from typing import List

router = APIRouter()

@router.get("/course_exercises/{course_id}", response_model=List[dict])
def get_course_exercises(course_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera listę ćwiczeń dla danego kursu (course_id), w tym id, title, done oraz link do obrazu.
    """
    # Pobranie ćwiczeń powiązanych z danym course_id
    exercises = db.query(Exercises).filter(Exercises.course_id == course_id).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found for this course")

    response = []
    for exercise in exercises:
        # Tworzenie linku do obrazu ćwiczenia, jeśli jest powiązany z obrazem
        picture_url = str(request.url_for("get_exercise_picture", exercise_id=exercise.id)) if exercise.picture_id else None

        # Przygotowanie szczegółów ćwiczenia
        exercise_details = {
            "id": exercise.id,
            "title": exercise.title,
            "done": exercise.done,
            "position": exercise.position,
            "picture_url": picture_url
        }
        response.append(exercise_details)

    return response


@router.get("/exercise_picture/{exercise_id}", response_class=FileResponse)
def get_exercise_picture(exercise_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz powiązany z ćwiczeniem w formacie JPG na podstawie exercise_id.
    """
    # Pobranie ćwiczenia i sprawdzenie, czy jest powiązane z obrazem
    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise or not exercise.picture_id:
        raise HTTPException(status_code=404, detail="Exercise or Picture not found")
    
    # Pobranie obrazu na podstawie picture_id
    picture = db.query(Pictures).filter(Pictures.id == exercise.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    # Zapis obrazu binarnego jako plik tymczasowy JPG
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    # Zwróć obraz jako plik JPG
    return FileResponse(temp_jpg_path, media_type="image/jpeg")


@router.put("/exercises/{exercise_id}/edit", response_model=dict)
def update_exercise(
    exercise_id: UUID,
    title: Optional[str] = Form(None),
    done: Optional[bool] = Form(None),
    course_id: Optional[UUID] = Form(None),
    picture_id: Optional[UUID] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Edytuje informacje o ćwiczeniu w tabeli exercises na podstawie exercise_id.
    """
    # Pobranie istniejącego ćwiczenia
    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Aktualizacja pól tylko jeśli zostały przekazane
    if title is not None:
        exercise.title = title
    if done is not None:
        exercise.done = done
    if course_id is not None:
        exercise.course_id = course_id
    if picture_id is not None:
        exercise.picture_id = picture_id

    # Zapisanie zmian w bazie danych
    db.commit()
    db.refresh(exercise)

    return {
        "message": "Exercise updated successfully",
        "exercise_id": str(exercise.id),
        "updated_fields": {
            "title": title,
            "done": done,
            "course_id": course_id,
            "picture_id": picture_id,
        },
    }
