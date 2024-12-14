from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from uuid import uuid4
from models import Pictures  # Upewnij się, że model Pictures jest poprawnie zaimportowany
from database import get_db

router = APIRouter()

@router.post("/pictures/upload", response_model=dict)
def upload_picture(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint do przesyłania zdjęć w formacie JPG i zapisywania ich jako blob w tabeli pictures.
    """
    # Sprawdzenie, czy plik ma odpowiedni format
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPG files are supported.")
    
    # Odczytanie pliku i zapisanie jako blob
    try:
        picture_blob = file.file.read()  # Odczyt danych binarnych z pliku
        picture_entry = Pictures(id=uuid4(), picture=picture_blob)
        
        # Dodanie zdjęcia do bazy danych
        db.add(picture_entry)
        db.commit()
        db.refresh(picture_entry)

        return {"message": "Picture uploaded successfully", "picture_id": str(picture_entry.id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading picture: {str(e)}")
