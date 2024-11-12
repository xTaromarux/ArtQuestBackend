from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
from typing import List
import uuid

from database import get_db
from models.posts import Posts
from schemas.Sposts import Posts as PostSchema, PostsCreate as PostCreate

router = APIRouter()

@router.post("/posts", response_model=PostSchema)
async def create_post(
    title: str = Form(...),
    description: str = Form(...),
    user_id: uuid.UUID = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    picture = None
    if file:
        picture = await file.read()

    db_post = Posts(
        id=uuid.uuid4(),
        title=title,
        description=description,
        picture=picture,
        user_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.picture_url = f"/posts/{db_post.id}/picture"
    return db_post

@router.get("/posts", response_model=List[PostSchema])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Posts).offset(skip).limit(limit).all()
    for post in posts:
        if post.picture:
            post.picture_url = f"/posts/{post.id}/picture"
    return posts

@router.get("/posts/{post_id}", response_model=PostSchema)
def read_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.picture:
        post.picture_url = f"/posts/{post.id}/picture"
    return post

@router.get("/posts/{post_id}/picture")
def get_post_picture(post_id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if post is None or not post.picture:
        raise HTTPException(status_code=404, detail="Picture not found")
    return Response(content=post.picture, media_type="image/jpeg")

@router.delete("/posts/{post_id}", response_model=PostSchema)
def delete_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return post
