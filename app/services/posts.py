from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import base64
from PIL import Image
import io

from database import get_db
from models.posts import Posts
from schemas.Sposts import Posts as PostSchema, PostsCreate as PostCreate, PostsUpdate as PostUpdate

router = APIRouter()

def convert_to_jpg_and_base64(image_binary):
    image = Image.open(io.BytesIO(image_binary))
    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        return base64.b64encode(output.getvalue()).decode("utf-8")

@router.put("/posts/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: uuid.UUID,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_post = db.query(Posts).filter(Posts.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if title:
        db_post.title = title
    if description:
        db_post.description = description
    if file:
        file_content = await file.read()
        db_post.picture = file_content
    
    db.commit()
    db.refresh(db_post)
    
    if db_post.picture:
        db_post.picture = convert_to_jpg_and_base64(db_post.picture)
    
    return db_post
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
