import uuid
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, get_db
from models.users import Users
from models.courses import Courses
from models.pictures import Pictures
from models.difficulties import Difficulties
from models.user_course import User_course
from models.posts import Posts
from models.exercises import Exercises
from models.views import Views
from models.views_pictures import Views_pictures
from models.views_data import Views_data
from models.statistics import Statistics
from models.achievements import Achievements
from models.user_achievements import User_achievements
from models.comments import Comments
from models.exercise_feedback import Exercise_feedback

# Function to convert images to binary
def convert_image_to_binary(image_path):
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return None
    with open(image_path, "rb") as image_file:
        return image_file.read()

# Function to add sample data
def add_sample_data(db: Session):
    # Define relative path to image directory
    image_dir = os.path.join(os.path.dirname(__file__), "../db_scripts/images/example_excercise_pictures")
    
    if not os.path.exists(image_dir):
        print(f"Directory not found: {image_dir}")
        return

    image_files = ["example_one.jpg", "example_two.jpg", "example_three.jpg", "example_zero.jpg"]

    # Load images as binary data
    pictures = [
        Pictures(id=uuid.uuid4(), picture=convert_image_to_binary(os.path.join(image_dir, img)))
        for img in image_files
    ]
    
    pictures = [pic for pic in pictures if pic.picture is not None]
    db.add_all(pictures)
    db.flush()

    # Add sample users
    users_data = [
        {
            "login": "user1",
            "mail": "user1@example.com",
            "group": "group1",
            "user_name": "User One",
            "created_date": datetime.now(),
            "picture_id": pictures[0].id if len(pictures) > 0 else None
        },
        {
            "login": "user2",
            "mail": "user2@example.com",
            "group": "group2",
            "user_name": "User Two",
            "created_date": datetime.now(),
            "picture_id": pictures[1].id if len(pictures) > 1 else None
        },
        {
            "login": "user3",
            "mail": "user3@example.com",
            "group": "group1",
            "user_name": "User Three",
            "created_date": datetime.now(),
            "picture_id": pictures[2].id if len(pictures) > 2 else None
        },
    ]
    users = [Users(**user_data) for user_data in users_data]
    db.add_all(users)
    db.flush()

    # Add sample difficulties
    difficulties = [
        Difficulties(id=uuid.uuid4(), level=1, color="Green", experience=10),
        Difficulties(id=uuid.uuid4(), level=2, color="Yellow", experience=20),
        Difficulties(id=uuid.uuid4(), level=3, color="Red", experience=30),
    ]
    db.add_all(difficulties)
    db.flush()

    # Add sample courses
    courses = [
        Courses(
            id=uuid.uuid4(), title="Python Basics", short_description="Intro to Python", 
            description="Learn the basics of Python programming.", experience=100, points=50,
            difficulty_id=difficulties[0].id, picture_id=pictures[0].id if len(pictures) > 0 else None
        ),
        Courses(
            id=uuid.uuid4(), title="Data Science", short_description="Data Science with Python",
            description="Introduction to data science concepts using Python.", experience=200, points=80,
            difficulty_id=difficulties[1].id, picture_id=pictures[1].id if len(pictures) > 1 else None
        ),
        Courses(
            id=uuid.uuid4(), title="Web Development", short_description="Full-stack Web Dev",
            description="Learn to build full-stack applications.", experience=150, points=60,
            difficulty_id=difficulties[2].id, picture_id=pictures[2].id if len(pictures) > 2 else None
        ),
    ]
    db.add_all(courses)
    db.flush()

    # Link users to courses
    user_courses = [
        User_course(id=uuid.uuid4(), course_id=courses[0].id, user_id=users[0].id),
        User_course(id=uuid.uuid4(), course_id=courses[1].id, user_id=users[1].id),
        User_course(id=uuid.uuid4(), course_id=courses[2].id, user_id=users[2].id),
    ]
    db.add_all(user_courses)

    # Add sample posts with pictures
    posts_data = [
        {
            "description": "Exploring Python Basics!",
            "reactions": 5,
            "date_added": datetime.now(),
            "date_updated": datetime.now(),
            "user_id": users[0].id,
            "picture_id": pictures[0].id if len(pictures) > 0 else None
        },
        {
            "description": "Getting started with Data Science.",
            "reactions": 10,
            "date_added": datetime.now(),
            "date_updated": datetime.now(),
            "user_id": users[1].id,
            "picture_id": pictures[1].id if len(pictures) > 1 else None
        },
        {
            "description": "Web development is fun!",
            "reactions": 7,
            "date_added": datetime.now(),
            "date_updated": datetime.now(),
            "user_id": users[2].id,
            "picture_id": pictures[2].id if len(pictures) > 2 else None
        },
    ]
    posts = [Posts(**post_data) for post_data in posts_data]
    db.add_all(posts)

    # Add sample exercises with pictures
    exercises_data = [
        {
            "title": "Exercise 1 - Python Basics",
            "done": False,
            "course_id": courses[0].id,
            "picture_id": pictures[0].id if len(pictures) > 0 else None
        },
        {
            "title": "Exercise 2 - Data Science Intro",
            "done": True,
            "course_id": courses[1].id,
            "picture_id": pictures[1].id if len(pictures) > 1 else None
        },
        {
            "title": "Exercise 3 - Web Dev Setup",
            "done": False,
            "course_id": courses[2].id,
            "picture_id": pictures[2].id if len(pictures) > 2 else None
        },
    ]
    exercises = [Exercises(id=uuid.uuid4(), **exercise_data) for exercise_data in exercises_data]
    db.add_all(exercises)
    db.flush()

    # Add sample views
    views_data = [
        Views(
            id=uuid.uuid4(),
            template=1,
            ai_part=True,
            next_view_id=None,
            previous_view_id=None,
            exercise_id=exercises[0].id,
            course_id=courses[0].id
        ),
        Views(
            id=uuid.uuid4(),
            template=2,
            ai_part=False,
            next_view_id=None,
            previous_view_id=None,
            exercise_id=exercises[1].id,
            course_id=courses[1].id
        )
    ]
    db.add_all(views_data)
    db.flush()

    # Add sample views_data with short_description for each view
    views_details = [
        Views_data(
            id=uuid.uuid4(),
            short_description="Python Basics Short Description",
            description="This is a detailed view of Exercise 1 for Python Basics",
            view_id=views_data[0].id
        ),
        Views_data(
            id=uuid.uuid4(),
            short_description="Data Science Intro Short Description",
            description="This is another detailed view for the Data Science Intro Exercise",
            view_id=views_data[1].id
        ),
    ]
    db.add_all(views_details)

    # Add sample views_pictures for each view
    views_pictures_data = [
        Views_pictures(
            id=uuid.uuid4(),
            view_id=views_data[0].id,
            picture_id=pictures[0].id
        ),
        Views_pictures(
            id=uuid.uuid4(),
            view_id=views_data[1].id,
            picture_id=pictures[1].id
        )
    ]
    db.add_all(views_pictures_data)

    # Add sample statistics for each user
    statistics_data = [
        Statistics(
            id=uuid.uuid4(),
            experience=150,
            level=3,
            courses=2,
            start_strike=datetime.now() - timedelta(days=10),
            end_strike=datetime.now(),
            user_id=users[0].id
        ),
        Statistics(
            id=uuid.uuid4(),
            experience=200,
            level=4,
            courses=3,
            start_strike=datetime.now() - timedelta(days=20),
            end_strike=datetime.now(),
            user_id=users[1].id
        ),
    ]
    db.add_all(statistics_data)

    # Add sample achievements
    achievements_data = [
        Achievements(
            id=uuid.uuid4(),
            experience=50,
            picture_id=pictures[2].id if len(pictures) > 2 else None
        ),
        Achievements(
            id=uuid.uuid4(),
            experience=30,
            picture_id=pictures[3].id if len(pictures) > 3 else None
        ),
    ]
    db.add_all(achievements_data)
    db.flush()

    # Link achievements to users
    user_achievements_data = [
        User_achievements(id=uuid.uuid4(), user_id=users[0].id, achievement_id=achievements_data[0].id),
        User_achievements(id=uuid.uuid4(), user_id=users[1].id, achievement_id=achievements_data[1].id)
    ]
    db.add_all(user_achievements_data)

    # Add sample difficulties
    difficulties = [
        Difficulties(id=uuid.uuid4(), level=1, color="Green", experience=10),
        Difficulties(id=uuid.uuid4(), level=2, color="Yellow", experience=20),
        Difficulties(id=uuid.uuid4(), level=3, color="Red", experience=30),
    ]
    db.add_all(difficulties)
    db.flush()

    # Add sample courses
 # Add sample courses
    courses = [
        Courses(
            id=uuid.uuid4(), 
            title="Python Basics", 
            short_description="Intro to Python", 
            description="Learn the basics of Python programming.", 
            long_description="This course covers fundamental concepts of Python programming such as variables, loops, functions, and object-oriented programming. By the end of the course, you'll be able to write basic Python scripts and understand core programming principles.",
            experience=100, 
            points=50,
            difficulty_id=difficulties[0].id, 
            picture_id=pictures[0].id if len(pictures) > 0 else None
        ),
        Courses(
            id=uuid.uuid4(), 
            title="Data Science", 
            short_description="Data Science with Python", 
            description="Introduction to data science concepts using Python.", 
            long_description="Dive into the world of data science with this introductory course. Learn how to manipulate data using libraries like Pandas, perform exploratory data analysis, and visualize data with Matplotlib and Seaborn.",
            experience=200, 
            points=80,
            difficulty_id=difficulties[1].id, 
            picture_id=pictures[1].id if len(pictures) > 1 else None
        ),
        Courses(
            id=uuid.uuid4(), 
            title="Web Development", 
            short_description="Full-stack Web Dev", 
            description="Learn to build full-stack applications.", 
            long_description="This comprehensive course will teach you how to develop full-stack web applications. You'll learn frontend development with HTML, CSS, and JavaScript, as well as backend development with frameworks like Flask or Django.",
            experience=150, 
            points=60,
            difficulty_id=difficulties[2].id, 
            picture_id=pictures[2].id if len(pictures) > 2 else None
        ),
    ]
    db.add_all(courses)
    db.flush()

    # Add sample exercises
    exercises_data = [
        {
            "title": "Exercise 1 - Python Basics",
            "done": False,
            "position": 15,
            "course_id": courses[0].id,
            "picture_id": pictures[0].id if len(pictures) > 0 else None
        },
        {
            "title": "Exercise 2 - Data Science Intro",
            "done": True,
            "position": 52,
            "course_id": courses[1].id,
            "picture_id": pictures[1].id if len(pictures) > 1 else None
        },
        {
            "title": "Exercise 3 - Web Dev Setup",
            "done": False,
            "position": 72,
            "course_id": courses[2].id,
            "picture_id": pictures[2].id if len(pictures) > 2 else None
        },
    ]
    exercises = [Exercises(id=uuid.uuid4(), **exercise_data) for exercise_data in exercises_data]
    db.add_all(exercises)
    db.flush()

    # Add exercise feedback
    feedback_data = [
        Exercise_feedback(
            id=uuid.uuid4(),
            message="Great start, keep improving!",
            user_id=users[0].id,
            exercise_id=exercises[0].id,
            picture_id=pictures[0].id if len(pictures) > 0 else None
        ),
        Exercise_feedback(
            id=uuid.uuid4(),
            message="Impressive progress!",
            user_id=users[1].id,
            exercise_id=exercises[1].id,
            picture_id=pictures[1].id if len(pictures) > 1 else None
        ),
    ]
    db.add_all(feedback_data)

    # Add comments
    comments_data = [
        Comments(
            id=uuid.uuid4(),
            description="I love this course!",
            reactions=10,
            user_id=users[0].id,
            post_id=None  # Add post_id here when posts are created
        ),
        Comments(
            id=uuid.uuid4(),
            description="Fantastic introduction.",
            reactions=5,
            user_id=users[1].id,
            post_id=None  # Add post_id here when posts are created
        ),
    ]
    db.add_all(comments_data)


    db.commit()
    print("Sample data added successfully.")

# Main function to create tables and add sample data
def main():
    from database import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Add sample data
    db = next(get_db())
    add_sample_data(db)
    print("Sample data added successfully.")

if __name__ == "__main__":
    main()
