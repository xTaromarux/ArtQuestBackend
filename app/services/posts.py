from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID, uuid4
from datetime import datetime
from database import get_db
from models.posts import Posts
from models.pictures import Pictures
from models.users import Users
from schemas.Sposts import PostDetailsResponse, PostsUpdate
import tempfile
import os
from typing import List

router = APIRouter()

@router.get("/user_picture/{user_id}", response_class=FileResponse)
def get_user_picture(user_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz powiązany z użytkownikiem w formacie JPG na podstawie user_id.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user or not user.picture_id:
        raise HTTPException(status_code=404, detail="User or picture not found")

    picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    # Zapisanie obrazu tymczasowo w formacie JPG
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")

@router.get("/post_picture/{post_id}", response_class=FileResponse)
def get_post_picture(post_id: UUID, db: Session = Depends(get_db)):
    """
    Zwraca obraz powiązany z postem w formacie JPG na podstawie post_id.
    """
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post or not post.picture_id:
        raise HTTPException(status_code=404, detail="Post or Picture not found")
    
    picture = db.query(Pictures).filter(Pictures.id == post.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")

@router.get("/post_details/{post_id}", response_model=PostDetailsResponse)
def get_post_details(post_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera szczegóły posta, w tym opis, daty, reakcje, link do obrazu posta oraz link do obrazu użytkownika.
    """
    # Pobranie posta
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Pobranie użytkownika
    user = db.query(Users).filter(Users.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generowanie linku do obrazu posta
    picture_url = None
    if post.picture_id:
        picture_url = str(request.url_for("get_post_picture", post_id=post_id))

    # Generowanie linku do obrazu użytkownika
    user_picture_url = None
    if user.picture_id:
        user_picture_url = str(request.url_for("get_user_picture", user_id=user.id))
    print(f"user.picture_id: {user.picture_id}, user_picture_url: {user_picture_url}")  # Debugowanie

    # Przygotowanie odpowiedzi
    response = {
        "id": post.id,
        "description": post.description,
        "date_added": post.date_added,
        "date_updated": post.date_updated,
        "reactions": post.reactions,
        "picture_url": picture_url,
        "user_name": user.user_name,
        "login": user.login,
        "user_picture_url": user_picture_url  # Dodany link do zdjęcia użytkownika
    }

    print(response)  # Debugowanie odpowiedzi
    return response


@router.get("/posts", response_model=List[PostDetailsResponse])
def get_posts(request: Request, db: Session = Depends(get_db)):
    """
    Zwraca listę maksymalnie 50 postów, w tym opis, daty, reakcje oraz link do obrazu i informacje o użytkowniku.
    """
    posts = db.query(Posts).limit(50).all()

    response = []
    for post in posts:
        # Pobranie użytkownika powiązanego z postem
        user = db.query(Users).filter(Users.id == post.user_id).first()
        if not user:
            continue

        # Generowanie URL do obrazu posta
        picture_url = None
        if post.picture_id:
            picture_url = str(request.url_for("get_post_picture", post_id=post.id))

        # Generowanie URL do obrazu użytkownika
        user_picture_url = None
        if user.picture_id:
            user_picture_url = str(request.url_for("get_user_picture", user_id=user.id))  # Poprawiono tutaj!

        # Przygotowanie odpowiedzi
        response.append({
            "id": post.id,
            "description": post.description,
            "date_added": post.date_added,
            "date_updated": post.date_updated,
            "reactions": post.reactions,
            "picture_url": picture_url,  # Link do obrazu posta
            "user_picture_url": user_picture_url, # Link do obrazu użytkownika
            "user_name": user.user_name,
            "login": user.login

        })
    print(response)
    return response



@router.post("/add_post", response_model=UUID)
async def add_post(
    description: str = Form(...),
    reactions: int = Form(0),
    user_id: UUID = Form(...),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Dodaje nowy post z opcjonalnym obrazem.
    """
    # Jeśli obraz został przesłany, zapisz go w tabeli Pictures
    picture_id = None
    if picture:
        # Konwertowanie obrazu do formatu binarnego
        image_data = await picture.read()
        
        # Zapis obrazu w tabeli Pictures
        new_picture = Pictures(id=uuid4(), picture=image_data)
        db.add(new_picture)
        db.flush()  # Upewnij się, że nowe ID jest dostępne
        picture_id = new_picture.id

    # Dodawanie nowego posta do tabeli Posts
    new_post = Posts(
        id=uuid4(),
        description=description,
        reactions=reactions,
        date_added=datetime.utcnow(),
        user_id=user_id,
        picture_id=picture_id
    )
    db.add(new_post)
    db.commit()
    
    # Zwracanie ID nowo utworzonego posta
    return new_post.id

@router.put("/post/{post_id}/edit_description", response_model=PostDetailsResponse)
def update_post_description(
    post_id: UUID,
    description: str,  # Akceptuje tylko pole `description`
    db: Session = Depends(get_db)
):
    """
    Edytuje opis postu (description) na podstawie post_id i aktualizuje pole `date_updated`.
    """
    # Pobranie postu z bazy danych
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Aktualizacja pola description i date_updated
    post.description = description
    post.date_updated = datetime.utcnow()  # Aktualizacja daty na bieżącą datę i czas

    db.commit()
    db.refresh(post)

    # Przygotowanie odpowiedzi
    response = PostDetailsResponse(
        id=post.id,
        description=post.description,
        date_added=post.date_added,
        date_updated=post.date_updated,
        reactions=post.reactions,
        picture_url=None,  # Można dodać link do obrazu, jeśli jest endpoint obsługujący obrazy
        user_name=post.user.user_name,
        login=post.user.login
    )
    return response

@router.delete("/post/{post_id}", response_model=dict)
def delete_post(post_id: UUID, db: Session = Depends(get_db)):
    """
    Usuwa post oraz przypisane do niego zdjęcie na podstawie post_id.
    """
    # Pobranie postu z bazy danych
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Sprawdzenie, czy post ma przypisane zdjęcie i jego usunięcie
    if post.picture_id:
        picture = db.query(Pictures).filter(Pictures.id == post.picture_id).first()
        if picture:
            db.delete(picture)

    # Usunięcie postu
    db.delete(post)
    db.commit()
    
    return {"message": "Post and associated picture deleted successfully"}

