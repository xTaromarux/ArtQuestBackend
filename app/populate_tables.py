import uuid
from sqlalchemy.orm import Session
from database import engine, get_db
from models.difficulty import Difficulty
from models.users import Users
from models.posts import Posts
from models.progress import Progress
from models.exercises import Exercises
from models.pictures import Pictures
import os

# Function to add sample data
def add_sample_data(db: Session):
    # Add sample difficulties
    difficulties = [
        Difficulty(name="Easy", color="Green", score=1),
        Difficulty(name="Medium", color="Yellow", score=2),
        Difficulty(name="Hard", color="Red", score=3),
        Difficulty(name="Very Hard", color="Purple", score=4),
        Difficulty(name="Extreme", color="Black", score=5),
    ]
    db.add_all(difficulties)
    db.flush()  # Ensure difficulties have IDs

    # Add sample users with avatars
    avatar_files = ["example_zero.jpg", "example_one.jpg", "example_two.jpg", "example_three.jpg"]
    users = []
    for i in range(1, 6):
        with open(os.path.join("/db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            avatar_data = image_file.read()
        users.append(Users(login=f"user{i}", password="password", mail=f"user{i}@example.com", group=None, name=f"User {i}", avatar=avatar_data))
    db.add_all(users)
    db.flush()  # Ensure users have IDs

    # Add sample exercises with additional fields
    exercises = [
        Exercises(title=f"Exercise {i}", description="Description", aipart="AI Part", colSpan=2, rowSpan=3, cols=4, rows=5, difficulty_id=difficulties[i % len(difficulties)].id)
        for i in range(1, 6)
    ]
    db.add_all(exercises)
    db.flush()  # Ensure exercises have IDs

    # Add sample pictures for exercises
    pictures = []
    for i, exercise in enumerate(exercises):
        with open(os.path.join("/db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            image_data = image_file.read()
        pictures.append(Pictures(picture=image_data, exercise_id=exercise.id))
    
    db.add_all(pictures)

    # Add sample posts with pictures
    posts = []
    for i in range(1, 6):
        with open(os.path.join("/db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            picture_data = image_file.read()
        posts.append(Posts(title=f"Post {i}", description="Description", picture=picture_data, user_id=users[i % len(users)].id))
    db.add_all(posts)
    db.flush()  # Ensure posts have IDs

    # Add sample progress
    progress_records = [
        Progress(user_id=users[i % len(users)].id, exercise_id=exercises[i % len(exercises)].id, score=i * 10, description="Progress description")
        for i in range(1, 6)
    ]
    db.add_all(progress_records)

    db.commit()

# Main function to create tables and add sample data
def main():
    from database import Base
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Add sample data
    db = next(get_db())
    add_sample_data(db)
    print("Sample data added successfully.")

if __name__ == "__main__":
    main()
