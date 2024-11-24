from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from models.progresses import Progresses as ProgressesModel
from database import get_db
from schemas.Sprogresses import Progresses
from models.user_course import User_course


router = APIRouter()

@router.post("/progresses/create")
def create_progress(
    user_course_id: UUID = Form(...),  # Pobiera user_course_id jako pole formularza
    stage: int = Form(...),           # Pobiera stage jako pole formularza
    db: Session = Depends(get_db)
):
    """
    Tworzy nowy wpis w tabeli progresses na podstawie user_course_id i stage.
    """
    # Sprawdzenie, czy user_course_id istnieje w tabeli User_course
    user_course = db.query(User_course).filter(User_course.id == user_course_id).first()
    if not user_course:
        raise HTTPException(status_code=404, detail="User_course not found")

    # Tworzenie nowego wpisu w tabeli Progresses
    new_progress = ProgressesModel(
        id=uuid4(),
        stage=stage,
        user_course_id=user_course_id
    )

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)

    return {
        "id": str(new_progress.id),
        "stage": new_progress.stage,
        "user_course_id": str(new_progress.user_course_id),
    }
@router.put("/progresses/{user_course_id}/edit_stage", response_model=Progresses)
def update_stage_by_user_course_id(user_course_id: UUID, stage: int, db: Session = Depends(get_db)):
    """
    Edytuje wartość `stage` w tabeli `progresses` na podstawie `user_course_id`.
    """
    # Pobranie rekordu progresses na podstawie user_course_id
    progress = db.query(ProgressesModel).filter(ProgressesModel.user_course_id == user_course_id).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")

    # Aktualizacja wartości stage
    progress.stage = stage

    db.commit()
    db.refresh(progress)

    return progress
