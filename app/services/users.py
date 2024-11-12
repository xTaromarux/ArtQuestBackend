import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from typing import List
from models.users import Users
from models.posts import Posts
from schemas.Susers import Users as UserSchema, UsersCreate
from database import get_db
from typing import Optional

router = APIRouter()

@router.post("/users", response_model=UserSchema)
async def create_user(
    login: str,
    mail: str,
    name: str,
    password: str,
    group: Optional[str] = None,
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Check if the login already exists
    existing_user = db.query(Users).filter(Users.login == login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already registered")

    avatar_binary = None
    if avatar:
        avatar_binary = await avatar.read()

    db_user = Users(
        id=uuid.uuid4(),
        login=login,
        password=password,
        mail=mail,
        group=group,
        name=name,
        avatar=avatar_binary
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.avatar_url = f"/users/{db_user.id}/avatar"
    return db_user

@router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.avatar:
        user.avatar_url = f"/users/{user.id}/avatar"
    return user

@router.get("/users/{user_id}/avatar")
def get_user_avatar(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None or not user.avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return Response(content=user.avatar, media_type="image/jpeg")

@router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return user

@router.get("/tweets", response_model=List[dict])
def get_tweets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Posts).offset(skip).limit(limit).all()
    tweets = []
    for post in posts:
        user = db.query(Users).filter(Users.id == post.user_id).first()

        tweet = {
            "id": post.id,
            "user": {
                "id": user.id,
                "login": user.login,
                "name": user.name,
                "avatar_url": f"/users/{user.id}/avatar" if user.avatar else None,
            },
            "Date_added": post.date_added,
            "Title": post.title,
            "Description": post.description,
            "image_url": f"/posts/{post.id}/picture" if post.picture else None
        }
        tweets.append(tweet)
    return tweets
