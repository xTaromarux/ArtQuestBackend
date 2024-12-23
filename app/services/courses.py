from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import tempfile
from uuid import UUID
from typing import Optional
from database import get_db
from typing import List
from models import User_course, Courses, Pictures, Difficulties, Exercises, User_course, Views, Views_data, Views_pictures, Progresses


router = APIRouter()

@router.get("/courses/{user_id}", response_model=List[dict])
def get_courses_by_user_id(user_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves a list of courses assigned to a given user (user_id) along with the user_course_id and stage value from the progresses table.
    """
    # Retrieve related user courses from the user_course table
    user_courses = db.query(User_course).filter(User_course.user_id == user_id).all()

    if not user_courses:
        raise HTTPException(status_code=404, detail="No courses found for the user")

    # Prepare a list of objects containing course details and stage value
    courses = []
    for uc in user_courses:
        # Course download
        course = db.query(Courses).filter(Courses.id == uc.course_id).first()
        if not course:
            continue

        # Retrieve the stage from the progresses table
        progress = db.query(Progresses).filter(Progresses.user_course_id == uc.id).first()
        stage = progress.stage if progress else None

        # Adding course details to the answer
        courses.append({
            "course_id": course.id,
            "title": course.title,
            "short_description": course.short_description,
            "description": course.description,
            "long_description": course.long_description,
            "experience": course.experience,
            "points": course.points,
            "difficulty_id": course.difficulty_id,
            "picture_id": course.picture_id,
            "user_course_id": uc.id,
            "stage": stage
        })

    return courses



@router.get("/course_details/{course_id}", response_model=dict)
def get_course_details(course_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Retrieves course details based on course_id, including title, description, difficulty level and image link.
    """
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    difficulty = db.query(Difficulties).filter(Difficulties.id == course.difficulty_id).first()
    if not difficulty:
        raise HTTPException(status_code=404, detail="Difficulty not found")

    picture_url = str(request.url_for("get_course_picture", course_id=course_id))

    response = {
        "course": {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "short_desscription": course.short_description,
            "long_description": course.long_description
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
    Returns a JPG image of the course based on the course_id.
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


@router.get("/all_courses_details", response_model=List[dict])
def get_all_courses_details(request: Request, db: Session = Depends(get_db)):
    """
    Retrieves details of all courses, including id, title, description, difficulty level and image link.
    """
    courses = db.query(Courses).all()
    response = []
    for course in courses:
        difficulty = db.query(Difficulties).filter(Difficulties.id == course.difficulty_id).first()
        if not difficulty:
            continue

        picture_url = str(request.url_for("get_course_picture", course_id=course.id)) if course.picture_id else None

        course_details = {
            
        "course": {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "short_desscription": course.short_description,
            "long_description": course.long_description
        },
        "difficulty": {
            "level": difficulty.level,
            "color": difficulty.color,
            "experience": difficulty.experience
        },
        "picture_url": picture_url
        }
        response.append(course_details)

    return response


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
    Edits course information in the courses table based on course_id.
    """
    # Downloading an existing course
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Update fields only if passed
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

@router.delete("/courses/{course_id}/delete", response_model=dict)
def delete_course(course_id: UUID, db: Session = Depends(get_db)):
    """
    Deletes the course and all related data based on course_id.
    """
    course = db.query(Courses).filter(Courses.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Deletion of related exercises
    exercises = db.query(Exercises).filter(Exercises.course_id == course_id).all()
    for exercise in exercises:
        # Remove views associated with the exercise
        views = db.query(Views).filter(Views.exercise_id == exercise.id).all()
        for view in views:
            # Deletion of view data
            views_data = db.query(Views_data).filter(Views_data.view_id == view.id).all()
            for view_data in views_data:
                db.delete(view_data)

            # Delete related view images
            views_pictures = db.query(Views_pictures).filter(Views_pictures.view_id == view.id).all()
            for view_picture in views_pictures:
                db.delete(view_picture)

            db.delete(view)

        # Deletion of associated exercise photos
        if exercise.picture_id:
            picture = db.query(Pictures).filter(Pictures.id == exercise.picture_id).first()
            if picture:
                db.delete(picture)

        db.delete(exercise)

    # Delete related course images
    if course.picture_id:
        course_picture = db.query(Pictures).filter(Pictures.id == course.picture_id).first()
        if course_picture:
            db.delete(course_picture)

    # Deleting links in the user_course table
    user_courses = db.query(User_course).filter(User_course.course_id == course_id).all()
    for user_course in user_courses:
        db.delete(user_course)

    # Delete related views for the course
    course_views = db.query(Views).filter(Views.course_id == course_id).all()
    for view in course_views:
        db.delete(view)

    # Course deletion
    db.delete(course)
    db.commit()

    return {"message": "Course and all associated data deleted successfully"}
