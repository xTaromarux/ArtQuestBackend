from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from models.comments import Comments as CommentsModel
from database import get_db
from schemas.Scomments import CommentResponse
from models.posts import Posts as PostsModel
from typing import List 
from models.users import Users

router = APIRouter()

@router.get("/comments/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post_id(post_id: UUID, request: Request, db: Session = Depends(get_db)):
    """
    Pobiera wszystkie komentarze dla danego postu, w tym szczegóły użytkownika (user_id, user_name, login oraz avatar jako link).
    """
    # Pobranie komentarzy przypisanych do danego postu
    comments = db.query(CommentsModel).filter(CommentsModel.post_id == post_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for the given post_id")

    # Przygotowanie odpowiedzi z dodatkowymi danymi użytkownika
    response = []
    for comment in comments:
        user = db.query(Users).filter(Users.id == comment.user_id).first()
        if not user:
            continue
        
        # Generowanie URL do awatara użytkownika
        avatar_url = None
        if user.picture_id:
            avatar_url = str(request.url_for("get_user_picture", user_id=user.id))

        # Dodanie danych do odpowiedzi
        response.append({
            "id": comment.id,
            "description": comment.description,
            "reactions": comment.reactions,
            "date_added": comment.date_added,
            "date_updated": comment.date_updated,
            "user_id": user.id,
            "user_name": user.user_name,
            "login": user.login,
            "avatar_url": avatar_url
        })

    return response

# Dodawanie komentarza
@router.post("/comments/add")
def add_comment(
    description: str = Form(...),
    reactions: int = Form(...),
    user_id: UUID = Form(...),
    post_id: UUID = Form(...),
    db: Session = Depends(get_db)
):
    """
    Dodaje nowy komentarz do podanego postu.
    """
    # Sprawdzenie, czy `post_id` istnieje w tabeli `posts`
    post = db.query(PostsModel).filter(PostsModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Tworzenie nowego komentarza
    new_comment = CommentsModel(
        id=uuid4(),
        description=description,
        reactions=reactions,
        user_id=user_id,
        post_id=post_id,
        date_added=datetime.now(),
        date_updated=datetime.now()
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "id": str(new_comment.id),
        "description": new_comment.description,
        "reactions": new_comment.reactions,
        "user_id": str(new_comment.user_id),
        "post_id": str(new_comment.post_id),
        "date_added": new_comment.date_added,
        "date_updated": new_comment.date_updated
    }


# Edytowanie komentarza
@router.put("/comments/{comment_id}/edit")
def edit_comment(
    comment_id: UUID,
    description: str = Form(None),  # Pole formularza na opis (opcjonalne)
    reactions: int = Form(None),    # Pole formularza na reakcje (opcjonalne)
    db: Session = Depends(get_db)
):
    """
    Edytuje istniejący komentarz na podstawie `comment_id`.
    """
    # Pobranie istniejącego komentarza
    comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Aktualizacja pól komentarza, jeśli zostały podane
    if description is not None:
        comment.description = description
    if reactions is not None:
        comment.reactions = reactions

    comment.date_updated = datetime.utcnow()  # Aktualizacja pola `date_updated`
    db.commit()
    db.refresh(comment)

    return {
        "id": str(comment.id),
        "description": comment.description,
        "reactions": comment.reactions,
        "user_id": str(comment.user_id),
        "post_id": str(comment.post_id),
        "date_added": comment.date_added,
        "date_updated": comment.date_updated,
    }


# Usuwanie komentarza
@router.delete("/comments/{comment_id}/delete")
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Usuwa komentarz na podstawie `comment_id`.
    """
    # Pobranie komentarza do usunięcia
    comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}

@router.get("/comments/{comment_id}/reactions", response_model=int)
def get_comment_reactions(comment_id: UUID, db: Session = Depends(get_db)):
    """
    Pobiera wartość `reactions` dla danego komentarza.
    """
    # Pobranie komentarza z bazy danych
    comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment.reactions

@router.put("/comments/{comment_id}/reactions", response_model=dict)
def update_comment_reactions(
    comment_id: UUID,
    reactions: int,
    db: Session = Depends(get_db)
):
    """
    Aktualizuje wartość `reactions` dla danego komentarza.
    """
    # Pobranie komentarza z bazy danych
    comment = db.query(CommentsModel).filter(CommentsModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Aktualizacja wartości reactions
    comment.reactions = reactions
    comment.date_updated = datetime.utcnow()

    db.commit()
    db.refresh(comment)

    return {"message": "Reactions updated successfully", "reactions": comment.reactions}
