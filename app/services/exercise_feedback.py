from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from models import Pictures, Exercise_feedback, Exercises
from database import get_db
from uuid import UUID, uuid4
from io import BytesIO
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import tempfile
from schemas.Sexercise_feedback import ExerciseFeedbackBase

# Import Twojej funkcji do przetwarzania obrazów
from app.ai_model.script import process_images  # Upewnij się, że funkcja `process_images` jest poprawnie zaimportowana.

router = APIRouter()

@router.post("/feedback/")
def generate_feedback(
    user_id: UUID = Form(...),
    exercise_id: UUID = Form(...),
    feedback_image: UploadFile = None,  # Przesyłane zdjęcie użytkownika
    db: Session = Depends(get_db)
):
    """
    Endpoint, który generuje feedback na podstawie zdjęcia przesłanego przez użytkownika i zdjęcia powiązanego z exercise_id.
    Jeśli feedback już istnieje dla danego user_id i exercise_id, zostanie zaktualizowany.
    """

    # Pobierz powiązane zdjęcie z tabeli Exercises
    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if not exercise.picture_id:
        raise HTTPException(status_code=404, detail="No picture associated with the exercise")

    # Pobierz zdjęcie powiązane z exercise.picture_id
    exercise_picture = db.query(Pictures).filter(Pictures.id == exercise.picture_id).first()
    if not exercise_picture:
        raise HTTPException(status_code=404, detail="Exercise picture not found")

    # Sprawdź, czy istnieje feedback dla user_id i exercise_id
    feedback_entry = db.query(Exercise_feedback).filter(
        Exercise_feedback.user_id == user_id,
        Exercise_feedback.exercise_id == exercise_id
    ).first()

    # Jeśli istnieje feedback, zaktualizuj go
    if feedback_entry:
        feedback_picture = db.query(Pictures).filter(Pictures.id == feedback_entry.picture_id).first()
        if feedback_picture:
            # Zaktualizuj istniejące zdjęcie
            feedback_picture.picture = feedback_image.file.read()  # Przechowujemy jako blob w bazie danych
        else:
            # Jeśli zdjęcie nie istnieje, utwórz nowe
            feedback_picture = Pictures(
                id=uuid4(),
                picture=feedback_image.file.read()  # Przechowujemy jako blob w bazie danych
            )
            db.add(feedback_picture)
            db.flush()
            feedback_entry.picture_id = feedback_picture.id  # Powiąż nowe zdjęcie z feedbackiem

        # Przetwarzaj obrazy jako dane binarne
        try:
            message = process_images(exercise_picture.picture, feedback_picture.picture)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

        # Zaktualizuj wiadomość w istniejącym feedbacku
        feedback_entry.message = message
        db.commit()

        return {"message": "Feedback updated successfully", "feedback_id": str(feedback_entry.id)}

    # Jeśli feedback nie istnieje, utwórz nowy
    feedback_picture = Pictures(
        id=uuid4(),
        picture=feedback_image.file.read()  # Przechowujemy jako blob w bazie danych
    )
    db.add(feedback_picture)
    db.flush()  # Upewnij się, że nowe ID jest dostępne

    # Przetwarzaj obrazy jako dane binarne
    try:
        message = process_images(exercise_picture.picture, feedback_picture.picture)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

    feedback_entry = Exercise_feedback(
        id=uuid4(),
        message=message,
        user_id=user_id,
        picture_id=feedback_picture.id,
        exercise_id=exercise_id
    )
    db.add(feedback_entry)
    db.commit()

    return {"message": "Feedback created successfully", "feedback_id": str(feedback_entry.id)}

@router.get("/feedback_details/{exercise_id}/{user_id}", response_model=dict)
def get_feedback_details(exercise_id: UUID, user_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły feedbacku, w tym wiadomość i link do obrazu powiązanego z feedbackiem.
    """
    # Pobierz feedback
    feedback = (
        db.query(Exercise_feedback)
        .filter(
            Exercise_feedback.exercise_id == exercise_id,
            Exercise_feedback.user_id == user_id
        )
        .first()
    )

    # Jeśli feedback nie istnieje
    if not feedback:
        raise HTTPException(status_code=404, detail=f"Feedback not found for exercise_id={exercise_id} and user_id={user_id}")

    # Jeśli feedback nie ma powiązanego obrazu
    if not feedback.picture_id:
        raise HTTPException(status_code=404, detail=f"No picture associated with feedback id={feedback.id}")

    # Sprawdź, czy istnieje endpoint dla obrazu
    try:
        picture_url = str(request.url_for("get_feedback_picture", picture_id=feedback.picture_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating picture URL: {str(e)}")

    return {
        "message": feedback.message,
        "picture_url": picture_url
    }



@router.get("/feedback_picture/{picture_id}", response_class=FileResponse)
def get_feedback_picture(picture_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz powiązany z feedbackiem w formacie JPG na podstawie picture_id.
    """
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")