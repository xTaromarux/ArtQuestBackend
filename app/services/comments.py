from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from database import get_db
from typing import List 
from schemas.Scomments import CommentResponse
from models import Posts, Users, Comments


router = APIRouter()

@router.get("/comments/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post_id(post_id: UUID, request: Request, db: Session = Depends(get_db)):

    """
    Retrieves all comments for a given post, including user details (user_id, user_name, login and avatar as a link).
    """
    # Retrieval of comments assigned to a post
    comments = db.query(Comments).filter(Comments.post_id == post_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for the given post_id")

    # Preparation of a response with additional user data
    response = []
    for comment in comments:
        user = db.query(Users).filter(Users.id == comment.user_id).first()
        if not user:
            continue
        
        # Generation of a URL to a user's avatar
        avatar_url = None
        if user.picture_id:
            avatar_url = str(request.url_for("get_user_picture", user_id=user.id))

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

# Adding a comment
@router.post("/comments/add")
def add_comment(
    description: str = Form(...),
    reactions: int = Form(...),
    user_id: UUID = Form(...),
    post_id: UUID = Form(...),
    db: Session = Depends(get_db)
):
    """
    Adds a new comment to the given post.
    """
    # Check if `post_id` exists in the `posts` table
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create a new comment
    new_comment = Comments(
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


# Editing a comment
@router.put("/comments/{comment_id}/edit")
def edit_comment(
    comment_id: UUID,
    description: str = Form(None),  
    reactions: int = Form(None),   
    db: Session = Depends(get_db)
):
    """
    Edits an existing comment based on `comment_id`.
    """
    # Downloading an existing comment
    comment = db.query(Comments).filter(Comments.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Update comment fields if specified
    if description is not None:
        comment.description = description
    if reactions is not None:
        comment.reactions = reactions

    comment.date_updated = datetime.utcnow()  # Update of `date_updated` field
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


# Deleting a comment
@router.delete("/comments/{comment_id}/delete")
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Deletes a comment based on `comment_id`.
    """
    # Downloading a comment for deletion
    comment = db.query(Comments).filter(Comments.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted successfully"}

@router.get("/comments/{comment_id}/reactions", response_model=int)
def get_comment_reactions(comment_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieves the `reactions` value for a given comment.
    """
    # Downloading a comment from the database
    comment = db.query(Comments).filter(Comments.id == comment_id).first()
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
    Updates the `reactions` value for a given comment.
    """
    # Downloading a comment from the database
    comment = db.query(Comments).filter(Comments.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Update reactions values
    comment.reactions = reactions
    comment.date_updated = datetime.utcnow()

    db.commit()
    db.refresh(comment)

    return {"message": "Reactions updated successfully", "reactions": comment.reactions}
