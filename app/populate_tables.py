import uuid
from sqlalchemy.orm import Session
from database import engine, get_db
from models.difficulties import Difficulties
from models.users import Users
from models.posts import Posts
from models.progresses import progresses
from models.courses import Courses
from models.pictures import Pictures
import os

# Function to add sample data
def add_sample_data(db: Session):
    # Add sample difficulties
    difficulties = [
        Difficulties(level= 1, color="Green", experience=1),
        Difficulties(level= 2, color="Yellow", experience=2),
        Difficulties(level= 3, color="Red", experience=3),
        Difficulties(level= 4, color="Purple", experience=4),
        Difficulties(level= 5, color="Black", experience=5),
    ]
    db.add_all(difficulties)
    db.flush()  # Ensure difficulties have IDs

    # Add sample users with avatars
    avatar_files = ["example_zero.jpg", "example_one.jpg", "example_two.jpg", "example_three.jpg"]
    users = []
    for i in range(1, 6):
        with open(os.path.join("./db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            avatar_data = image_file.read()
        users.append(Users(login=f"user{i}", password="password", mail=f"user{i}@example.com", group=None, name=f"User {i}", avatar=avatar_data))
    db.add_all(users)
    db.flush()  # Ensure users have IDs

    # Add sample courses with additional fields
    courses = [
        Courses(title=f"course {i}", description="Description", difficulty_id=difficulties[i % len(difficulties)].id)
        for i in range(1, 6)
    ]
    db.add_all(courses)
    db.flush()  # Ensure courses have IDs

    # Add sample pictures for courses
    pictures = []
    for i, course in enumerate(courses):
        with open(os.path.join("./db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            image_data = image_file.read()
        pictures.append(Pictures(picture=image_data))
    
    db.add_all(pictures)

    # Add sample posts with pictures
    posts = []
    for i in range(1, 6):
        with open(os.path.join("./db_scripts/images/example_excercise_pictures", avatar_files[i % len(avatar_files)]), "rb") as image_file:
            picture_data = image_file.read()
        posts.append(Posts(title=f"Post {i}", description="Description", picture=picture_data, user_id=users[i % len(users)].id))
    db.add_all(posts)
    db.flush()  # Ensure posts have IDs

    # Add sample progresses
    progresses_records = [
        progresses(user_id=users[i % len(users)].id, course_id=courses[i % len(courses)].id, score=i * 10, description="progresses description")
        for i in range(1, 6)
    ]
    db.add_all(progresses_records)

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
