from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
from sqlalchemy.orm import Session
from models import Pictures, Exercise_feedback, Exercises
from database import get_db
from uuid import UUID, uuid4
from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import tempfile
from app.ai_model.script import process_images

router = APIRouter()

@router.post("/feedback/")
def generate_feedback(
    user_id: UUID = Form(...),
    exercise_id: UUID = Form(...),
    feedback_image: UploadFile = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint, which generates feedback based on the photo uploaded by the user and the photo associated with the exercise_id.
    If feedback already exists for a given user_id and exercise_id, it will be updated.
    """

    # Download related photo from Exercises table
    exercise = db.query(Exercises).filter(Exercises.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if not exercise.picture_id:
        raise HTTPException(status_code=404, detail="No picture associated with the exercise")

    # Get a picture related to exercise.picture_id
    exercise_picture = db.query(Pictures).filter(Pictures.id == exercise.picture_id).first()
    if not exercise_picture:
        raise HTTPException(status_code=404, detail="Exercise picture not found")

    # Check if there is feedback for user_id and exercise_id
    feedback_entry = db.query(Exercise_feedback).filter(
        Exercise_feedback.user_id == user_id,
        Exercise_feedback.exercise_id == exercise_id
    ).first()

    # If feedback exists, update it
    if feedback_entry:
        feedback_picture = db.query(Pictures).filter(Pictures.id == feedback_entry.picture_id).first()
        if feedback_picture:
            # Update an existing photo
            feedback_picture.picture = feedback_image.file.read() 
        else:
            feedback_picture = Pictures(
                id=uuid4(),
                picture=feedback_image.file.read()
            )
            db.add(feedback_picture)
            db.flush()
            feedback_entry.picture_id = feedback_picture.id 

        try:
            message = process_images(exercise_picture.picture, feedback_picture.picture)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

        feedback_entry.message = message
        db.commit()

        return {"message": "Feedback updated successfully", "feedback_id": str(feedback_entry.id)}

    feedback_picture = Pictures(
        id=uuid4(),
        picture=feedback_image.file.read()  
    )
    db.add(feedback_picture)
    db.flush()  

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
    Retrieves details of the feedback, including the message and a link to the image associated with the feedback.
    """
    feedback = (
        db.query(Exercise_feedback)
        .filter(
            Exercise_feedback.exercise_id == exercise_id,
            Exercise_feedback.user_id == user_id
        )
        .first()
    )

    if not feedback:
        raise HTTPException(status_code=404, detail=f"Feedback not found for exercise_id={exercise_id} and user_id={user_id}")

    if not feedback.picture_id:
        raise HTTPException(status_code=404, detail=f"No picture associated with feedback id={feedback.id}")

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
    Returns the image associated with the feedback in JPG format based on the picture_id.
    """
    picture = db.query(Pictures).filter(Pictures.id == picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")