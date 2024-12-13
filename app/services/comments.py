from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from models.comments import Comments as CommentsModel
from database import get_db
from schemas.Scomments import Comments
from models.posts import Posts as PostsModel
from typing import List 

router = APIRouter()

@router.get("/comments/{post_id}", response_model=List[Comments])
def get_comments_by_post_id(post_id: UUID, db: Session = Depends(get_db)):
    """
    Pobiera wszystkie komentarze dla danego postu na podstawie `post_id`.
    """
    # Pobranie komentarzy przypisanych do danego postu
    comments = db.query(CommentsModel).filter(CommentsModel.post_id == post_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for the given post_id")

    return comments

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
