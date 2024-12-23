from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone
from typing import Optional
import pytz

from database import get_db
from models.users import Users
from models.pictures import Pictures
from models.posts import Posts
from models.user_achievements import User_achievements
from models.user_course import User_course
from models.statistics import Statistics
from models.user_achievements import User_achievements
from models.achievements import Achievements
from models.exercise_feedback import Exercise_feedback
from models.comments import Comments
from schemas.Susers import Users as UsersMinimalResponse


router = APIRouter()

def convert_image_to_binary(upload_file: UploadFile) -> bytes:
    """
    Konwertuje przesłany plik obrazu na dane binarne.
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
    Tworzy nowego użytkownika, ustawiając `created_date` w stałej strefie czasowej UTC+1.
    """
    # Ustawienie czasu na UTC+1
    utc_plus_one = timezone(timedelta(hours=1))
    current_time = datetime.now(utc_plus_one)

    # Utworzenie nowego użytkownika
    user = Users(
        id=uuid4(),
        login=login,
        mail=mail,
        user_name=user_name,
        group=group,
        created_date=current_time
    )

    # Jeśli przekazano obraz, zapisz go w tabeli pictures
    if picture:
        user_picture = Pictures(id=uuid4(), picture=convert_image_to_binary(picture))
        db.add(user_picture)
        db.flush()  # Zapisuje obraz i generuje jego ID
        user.picture_id = user_picture.id  # Przypisanie ID obrazu do użytkownika

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

    # Aktualizacja pól użytkownika
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

    # Ręczne tworzenie odpowiedzi
    return UsersMinimalResponse(
        id=user.id,
        login=user.login,
        mail=user.mail,
        user_name=user.user_name
    )


@router.delete("/user/{user_id}", response_model=dict)

def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Usuwa wszystkie informacje dotyczące użytkownika na podstawie user_id, w tym powiązane zdjęcie,
    posty, kursy, osiągnięcia, statystyki, komentarze i exercise_feedback.
    """
    # Pobranie użytkownika z bazy danych
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Sprawdzenie, czy użytkownik ma powiązane zdjęcie i jego usunięcie
    if user.picture_id:
        picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
        if picture:
            db.delete(picture)
    
    # Usunięcie wszystkich postów użytkownika
    user_posts = db.query(Posts).filter(Posts.user_id == user_id).all()
    for post in user_posts:
        db.delete(post)
    
    # Usunięcie wszystkich powiązanych wierszy w tabeli user_course
    user_courses = db.query(User_course).filter(User_course.user_id == user_id).all()
    for user_course in user_courses:
        db.delete(user_course)

    # Usunięcie wszystkich powiązanych wierszy w tabeli user_achievements
    user_achievements = db.query(User_achievements).filter(User_achievements.user_id == user_id).all()
    for achievement in user_achievements:
        db.delete(achievement)

    # Usunięcie statystyk użytkownika
    user_statistics = db.query(Statistics).filter(Statistics.user_id == user_id).first()
    if user_statistics:
        db.delete(user_statistics)

    # Usunięcie wszystkich powiązanych wierszy w tabeli exercise_feedback
    user_feedbacks = db.query(Exercise_feedback).filter(Exercise_feedback.user_id == user_id).all()
    for feedback in user_feedbacks:
        # Usunięcie powiązanego zdjęcia, jeśli istnieje
        if feedback.picture_id:
            feedback_picture = db.query(Pictures).filter(Pictures.id == feedback.picture_id).first()
            if feedback_picture:
                db.delete(feedback_picture)
        db.delete(feedback)

    # Usunięcie wszystkich komentarzy użytkownika
    user_comments = db.query(Comments).filter(Comments.user_id == user_id).all()
    for comment in user_comments:
        db.delete(comment)

    # Usunięcie użytkownika
    db.delete(user)
    db.commit()
    
    return {"message": "User, associated picture, posts, user_course entries, user_achievements, statistics, comments, and exercise_feedback entries deleted successfully"}

@router.get("/user/{user_id}/details", response_model=dict)
def get_user_details(user_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły użytkownika, w tym statystyki, osiągnięcia i link do obrazu powiązanego z użytkownikiem.
    """
    # Pobranie użytkownika
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Pobranie statystyk użytkownika
    statistics = db.query(Statistics).filter(Statistics.user_id == user_id).first()
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics not found")

    # Pobranie osiągnięć użytkownika z tabeli user_achievements i achievements
    user_achievements = (
        db.query(Achievements.experience, Achievements.picture_id)
        .join(User_achievements, User_achievements.achievement_id == Achievements.id)
        .filter(User_achievements.user_id == user_id)
        .all()
    )

    # Przygotowanie listy osiągnięć z linkami do obrazów
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

    # Pobranie linku do obrazu użytkownika, jeśli istnieje
    picture_url = None
    if user.picture_id:
        picture_url = str(request.url_for("get_picture_by_id", picture_id=user.picture_id))

    # Przygotowanie odpowiedzi
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
    Pobiera obraz z tabeli pictures jako plik JPG na podstawie picture_id.
    """
    # Pobranie obrazu z bazy danych
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")
    
    # Zapis obrazu tymczasowo jako plik JPG
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_file.write(picture.picture)
        temp_file_path = temp_file.name

    # Zwrócenie pliku obrazu jako odpowiedź
    return FileResponse(temp_file_path, media_type="image/jpeg")