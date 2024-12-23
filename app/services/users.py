from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from typing import Optional
from database import get_db
import tempfile
from models import Users, Pictures, Posts, User_achievements, User_course, Statistics, User_achievements, Achievements, Exercise_feedback, Comments
from schemas.Susers import Users as UsersMinimalResponse

router = APIRouter()

def convert_image_to_binary(upload_file: UploadFile) -> bytes:
    """
    Converts the uploaded image file into binary data.
    """
    try:
        return upload_file.file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@router.post("/user/create", response_model=UsersMinimalResponse)
async def create_user(
    login: str,
    mail: str,
    user_name: str,
    group: Optional[str] = None,
    picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Creates a new user by setting `created_date` in the fixed time zone UTC+1.
    """
    utc_plus_one = timezone(timedelta(hours=1))
    current_time = datetime.now(utc_plus_one)

    # Creation of a new user
    user = Users(
        id=uuid4(),
        login=login,
        mail=mail,
        user_name=user_name,
        group=group,
        created_date=current_time
    )

    if picture:
        user_picture = Pictures(id=uuid4(), picture=convert_image_to_binary(picture))
        db.add(user_picture)
        db.flush()
        user.picture_id = user_picture.id

    db.add(user)
    db.commit()
    db.refresh(user)

    return UsersMinimalResponse(
        id=user.id,
        login=user.login,
        mail=user.mail,
        user_name=user.user_name
    )

@router.put("/user/update/{user_id}", response_model=UsersMinimalResponse)
async def update_user(
    user_id: UUID,
    login: Optional[str] = None,
    mail: Optional[str] = None,
    user_name: Optional[str] = None,
    group: Optional[str] = None,
    picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if login:
        user.login = login
    if mail:
        user.mail = mail
    if user_name:
        user.user_name = user_name
    if group:
        user.group = group
    if picture:
        user_picture = Pictures(id=uuid4(), picture=picture.file.read())
        db.add(user_picture)
        db.flush()
        user.picture_id = user_picture.id

    db.commit()
    db.refresh(user)

    return UsersMinimalResponse(
        id=user.id,
        login=user.login,
        mail=user.mail,
        user_name=user.user_name
    )


@router.delete("/user/{user_id}", response_model=dict)

def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Deletes all user information based on user_id, including related photo,
    posts, courses, achievements, statistics, comments and exercise_feedback.
    """
    # Downloading a user from the database
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Checking whether the user has an associated photo and deleting it
    if user.picture_id:
        picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
        if picture:
            db.delete(picture)
    
    user_posts = db.query(Posts).filter(Posts.user_id == user_id).all()
    for post in user_posts:
        db.delete(post)
    
    user_courses = db.query(User_course).filter(User_course.user_id == user_id).all()
    for user_course in user_courses:
        db.delete(user_course)

    user_achievements = db.query(User_achievements).filter(User_achievements.user_id == user_id).all()
    for achievement in user_achievements:
        db.delete(achievement)

    user_statistics = db.query(Statistics).filter(Statistics.user_id == user_id).first()
    if user_statistics:
        db.delete(user_statistics)

    user_feedbacks = db.query(Exercise_feedback).filter(Exercise_feedback.user_id == user_id).all()
    for feedback in user_feedbacks:

        if feedback.picture_id:
            feedback_picture = db.query(Pictures).filter(Pictures.id == feedback.picture_id).first()
            if feedback_picture:
                db.delete(feedback_picture)
        db.delete(feedback)

    user_comments = db.query(Comments).filter(Comments.user_id == user_id).all()
    for comment in user_comments:
        db.delete(comment)

    db.delete(user)
    db.commit()
    
    return {"message": "User, associated picture, posts, user_course entries, user_achievements, statistics, comments, and exercise_feedback entries deleted successfully"}

@router.get("/user/{user_id}/details", response_model=dict)
def get_user_details(user_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Retrieves user details, including statistics, achievements and a link to the image associated with the user.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    statistics = db.query(Statistics).filter(Statistics.user_id == user_id).first()
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics not found")
    
    # Retrieve user achievements from the user_achievements and achievements table
    user_achievements = (
        db.query(Achievements.experience, Achievements.picture_id)
        .join(User_achievements, User_achievements.achievement_id == Achievements.id)
        .filter(User_achievements.user_id == user_id)
        .all()
    )

    achievements = []
    for achievement in user_achievements:
        picture_url = (
            str(request.url_for("get_picture_by_id", picture_id=achievement.picture_id))
            if achievement.picture_id else None
        )
        achievements.append({
            "experience": achievement.experience,
            "picture_url": picture_url
        })

    picture_url = None
    if user.picture_id:
        picture_url = str(request.url_for("get_picture_by_id", picture_id=user.picture_id))

    response = {
        "user": {
            "login": user.login,
            "mail": user.mail,
            "user_name": user.user_name,
            "created_date": user.created_date,
            "picture_url": picture_url
        },
        "statistics": {
            "experience": statistics.experience,
            "level": statistics.level,
            "courses": statistics.courses,
            "start_strike": statistics.start_strike,
            "end_strike": statistics.end_strike
        },
        "achievements": achievements
    }
    
    return response


@router.get("/picture/{picture_id}", response_class=FileResponse, name="get_picture_by_id")
def get_picture_by_id(picture_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves an image from the pictures table as a JPG file based on picture_id.
    """
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(picture.picture)
        temp_file_path = temp_file.name

    return FileResponse(temp_file_path, media_type="image/jpeg")