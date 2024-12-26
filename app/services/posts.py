from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from uuid import UUID, uuid4
from datetime import datetime
from database import get_db
import tempfile
from typing import List
from models import Posts, Pictures, Users
from schemas.Sposts import PostDetailsResponse, PostsBase


router = APIRouter()

@router.get("/user_picture/{user_id}", response_class=FileResponse)
def get_user_picture(user_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the image associated with the user in JPG format based on user_id.
    """
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user or not user.picture_id:
        raise HTTPException(status_code=404, detail="User or picture not found")

    picture = db.query(Pictures).filter(Pictures.id == user.picture_id).first()
    if not picture or not picture.picture:
        raise HTTPException(status_code=404, detail="Picture not found")

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_jpg:
        temp_jpg.write(picture.picture)
        temp_jpg_path = temp_jpg.name

    return FileResponse(temp_jpg_path, media_type="image/jpeg")

@router.get("/post_picture/{post_id}", response_class=FileResponse)
def get_post_picture(post_id: UUID, db: Session = Depends(get_db)):
    """
    Returns the image associated with the post in JPG format based on the post_id.
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
    Retrieves post details, including description, dates, reactions, link to post image and link to user image.
    """

    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user = db.query(Users).filter(Users.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    picture_url = None
    if post.picture_id:
        picture_url = str(request.url_for("get_post_picture", post_id=post_id))

    user_picture_url = None
    if user.picture_id:
        user_picture_url = str(request.url_for("get_user_picture", user_id=user.id))
    print(f"user.picture_id: {user.picture_id}, user_picture_url: {user_picture_url}")  # Debugowanie

    response = {
        "id": post.id,
        "description": post.description,
        "date_added": post.date_added,
        "date_updated": post.date_updated,
        "reactions": post.reactions,
        "picture_url": picture_url,
        "user_name": user.user_name,
        "login": user.login,
        "user_picture_url": user_picture_url  
    }

    print(response)  
    return response


@router.get("/posts", response_model=List[PostDetailsResponse])
def get_posts(request: Request, db: Session = Depends(get_db)):
    """
    Returns a list of up to 50 posts, including description, dates, reactions and a link to the image and user information.
    """
    posts = db.query(Posts).limit(50).all()

    response = []
    for post in posts:

        user = db.query(Users).filter(Users.id == post.user_id).first()
        if not user:
            continue

        picture_url = None
        if post.picture_id:
            picture_url = str(request.url_for("get_post_picture", post_id=post.id))

        user_picture_url = None
        if user.picture_id:
            user_picture_url = str(request.url_for("get_user_picture", user_id=user.id))  # Poprawiono tutaj!

        response.append({
            "id": post.id,
            "description": post.description,
            "date_added": post.date_added,
            "date_updated": post.date_updated,
            "reactions": post.reactions,
            "picture_url": picture_url, 
            "user_picture_url": user_picture_url, 
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
    Adds a new post with an optional image.
    """
    # If an image has been uploaded, save it to the Pictures table
    picture_id = None
    if picture:
        # Convert image to binary format
        image_data = await picture.read()
        
        new_picture = Pictures(id=uuid4(), picture=image_data)
        db.add(new_picture)
        db.flush()
        picture_id = new_picture.id

    # Adding a new post to the Posts table
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
    
    # Returning the ID of a newly created post
    return new_post.id

@router.put("/post/{post_id}/edit_description", response_model=PostDetailsResponse)
def update_post_description(
    post_id: UUID,
    description: str,
    db: Session = Depends(get_db)
):
    """
    Edits the post description based on the post_id and updates the `date_updated` field.
    """

    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.description = description
    post.date_updated = datetime.utcnow()

    db.commit()
    db.refresh(post)

    response = PostDetailsResponse(
        id=post.id,
        description=post.description,
        date_added=post.date_added,
        date_updated=post.date_updated,
        reactions=post.reactions,
        picture_url=None, 
        user_name=post.user.user_name,
        login=post.user.login
    )
    return response

@router.delete("/post/{post_id}", response_model=dict)
def delete_post(post_id: UUID, db: Session = Depends(get_db)):
    """
    Deletes the post and the photo assigned to it based on the post_id.
    """
    post = db.query(Posts).filter(Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.picture_id:
        picture = db.query(Pictures).filter(Pictures.id == post.picture_id).first()
        if picture:
            db.delete(picture)

    db.delete(post)
    db.commit()
    
    return {"message": "Post and associated picture deleted successfully"}

@router.put("/posts/{post_id}/edit_reactions", response_model=PostsBase)
def update_post_reactions(
    post_id: UUID,
    reactions: int = Form(...),  
    db: Session = Depends(get_db)
):
    """
    Edits reactions in the posts table based on post_id.
    """
    # Downloading a post based on post_id
    post = db.query(Posts).filter(Posts.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update the reactions field and update date
    post.reactions = reactions
    post.date_updated = datetime.utcnow() 

    db.commit()
    db.refresh(post)

    # Returning an updated post
    return {
        "id": post.id,
        "description": post.description,
        "reactions": post.reactions,
        "date_updated": post.date_updated
    }