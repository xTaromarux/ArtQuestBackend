from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID
from database import get_db
from typing import Optional
from models import Exercises, Pictures
import tempfile
from typing import List

router = APIRouter()

@router.get("/course_exercises/{course_id}", response_model=List[dict])
def get_course_exercises(course_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Retrieves a list of exercises for a course (course_id), including id, title, done and a link to the image.
    """
    # Downloading exercises associated with a given course_id
    exercises = db.query(Exercises).filter(Exercises.course_id == course_id).all()
    if not exercises:
        raise HTTPException(status_code=404, detail="No exercises found for this course")

    response = []
    for exercise in exercises:

        picture_url = str(request.url_for("get_exercise_picture", exercise_id=exercise.id)) if exercise.picture_id else None


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
    Returns the image associated with the exercise in JPG format based on exercise_id.
    """

    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise or not exercise.picture_id:
        raise HTTPException(status_code=404, detail="Exercise or Picture not found")
    

    picture = db.query(Pictures).filter(Pictures.id == exercise.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")


    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name


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
    Edits exercise information in the exercises table based on exercise_id.
    """

    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")


    if title is not None:
        exercise.title = title
    if done is not None:
        exercise.done = done
    if course_id is not None:
        exercise.course_id = course_id
    if picture_id is not None:
        exercise.picture_id = picture_id


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
