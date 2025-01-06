from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from uuid import uuid4
from database import get_db
from models import Pictures  


router = APIRouter()

@router.post("/pictures/upload", response_model=dict)
def upload_picture(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to upload images in JPG and PNG format and save them as a blob in the pictures table.
    """
    # Check that the file is in the correct format
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPG and PNG files are supported.")
    

    try:
        picture_blob = file.file.read() 
        picture_entry = Pictures(id=uuid4(), picture=picture_blob)
        

        db.add(picture_entry)
        db.commit()
        db.refresh(picture_entry)

        return {"message": "Picture uploaded successfully", "picture_id": str(picture_entry.id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading picture: {str(e)}")
