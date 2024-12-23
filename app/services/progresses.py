from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from models import Progresses, User_course
from database import get_db
from schemas.Sprogresses import Progresses


router = APIRouter()

@router.post("/progresses/create")
def create_progress(
    user_course_id: UUID = Form(...), 
    stage: int = Form(...), 
    db: Session = Depends(get_db)
):
    """
    Creates a new entry in the progresses table based on user_course_id and stage.
    """
    user_course = db.query(User_course).filter(User_course.id == user_course_id).first()
    if not user_course:
        raise HTTPException(status_code=404, detail="User_course not found")

    # Create a new entry in the Progresses table
    new_progress = Progresses(
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
    Edits the `stage` value in the `progresses` table based on the `user_course_id`.
    """
    progress = db.query(Progresses).filter(Progresses.user_course_id == user_course_id).first()

    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")

    progress.stage = stage

    db.commit()
    db.refresh(progress)

    return progress
