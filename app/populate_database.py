import uuid
import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Users, Courses, Pictures, Difficulties, User_course, Posts, Exercise_feedback
from models import Exercises, Views, Views_pictures, Views_data, Statistics, Achievements, User_achievements, Comments, Progresses

def read_csv(file_path):
    try:
        return pd.read_csv(file_path, converters={"id": lambda x: uuid.UUID(x)})
    except UnicodeDecodeError:
        # Try a fallback encoding if UTF-8 fails
        return pd.read_csv(file_path, encoding="latin1", converters={"id": lambda x: uuid.UUID(x)})

def add_data_from_csv(db: Session):
    # Load data from CSV files
    pictures = read_csv('app/data/csv/pictures.csv')
    users = read_csv('app/data/csv/users.csv')
    difficulties = read_csv('app/data/csv/difficulties.csv')
    courses = read_csv('app/data/csv/courses.csv')
    user_course = read_csv('app/data/csv/user_course.csv')
    posts = read_csv('app/data/csv/posts.csv')
    exercises = read_csv('app/data/csv/exercises.csv')
    views = read_csv('app/data/csv/views.csv')
    views_data = read_csv('app/data/csv/views_data.csv')
    views_pictures = read_csv('app/data/csv/views_pictures.csv')
    statistics = read_csv('app/data/csv/statistics.csv')
    achievements = read_csv('app/data/csv/achievements.csv')
    exercise_feedback = read_csv('app/data/csv/exercise_feedback.csv')
    comments = read_csv('app/data/csv/comments.csv')
    progresses = read_csv('app/data/csv/progresses.csv')

    # Insert pictures
    for _, row in pictures.iterrows():
        with open(f"app/data/pictures/{row['picture']}", "rb") as img_file:
            db.add(Pictures(id=row['id'], picture=img_file.read()))
    db.flush()

# Insert users
    for _, row in users.iterrows():
        db.add(Users(
            id=row['id'],
            login=row['login'],
            mail=row['mail'],
            group=row['group'] if pd.notna(row['group']) else None,
            user_name=row['user_name'],
            created_date=datetime.fromisoformat(row['created_date']),
            picture_id=row['picture_id'] if pd.notna(row['picture_id']) else None  # Obsługa NaN
        ))
    db.flush()


    # Insert difficulties
    for _, row in difficulties.iterrows():
        db.add(Difficulties(
            id=row['id'], level=row['level'], color=row['color'], experience=row['experience']
        ))
    db.flush()

    # Insert courses
    for _, row in courses.iterrows():
        db.add(Courses(
            id=row['id'], title=row['title'], short_description=row['short_description'],
            description=row['description'], experience=row['experience'],
            points=row['points'], difficulty_id=row['difficulty_id'], picture_id=row['picture_id']
        ))
    db.flush()

    # Insert user courses
    for _, row in user_course.iterrows():
        db.add(User_course(
            id=row['id'], course_id=row['course_id'], user_id=row['user_id']
        ))
    db.flush()

# Insert posts
    for _, row in posts.iterrows():
        if pd.notna(row['picture_id']):
            # Sprawdź, czy picture_id istnieje w tabeli Pictures
            picture_exists = db.query(Pictures).filter_by(id=row['picture_id']).first()
            if not picture_exists:
                print(f"Skipping post with ID {row['id']} because picture_id {row['picture_id']} does not exist.")
                continue

        db.add(Posts(
            id=row['id'],
            description=row['description'],
            reactions=row['reactions'],
            date_added=datetime.fromisoformat(row['date_added']),
            date_updated=datetime.fromisoformat(row['date_updated']),
            user_id=row['user_id'],
            picture_id=row['picture_id'] if pd.notna(row['picture_id']) else None
        ))
    db.flush()


    # Insert exercises
    for _, row in exercises.iterrows():
        db.add(Exercises(
            id=row['id'], title=row['title'], done=row['done'],
            course_id=row['course_id'], picture_id=row['picture_id']
        ))
    db.flush()

    # Insert views
    for _, row in views.iterrows():
        db.add(Views(
            id=row['id'],
            template=row['template'],
            ai_part=row['ai_part'],
            next_view_id=row['next_view_id'] if pd.notna(row['next_view_id']) else None,
            previous_view_id=row['previous_view_id'] if pd.notna(row['previous_view_id']) else None,
            exercise_id=row['exercise_id'],
            course_id=row['course_id']
        ))
    db.flush()


    # Insert views data
    for _, row in views_data.iterrows():
        db.add(Views_data(
            id=row['id'], short_description=row['short_description'],
            description=row['description'], view_id=row['view_id']
        ))
    db.flush()

    # Insert views pictures
    for _, row in views_pictures.iterrows():
        db.add(Views_pictures(
            id=row['id'], view_id=row['view_id'], picture_id=row['picture_id']
        ))
    db.flush()

    # Insert statistics
    for _, row in statistics.iterrows():
        db.add(Statistics(
            id=row['id'], experience=row['experience'], level=row['level'], courses=row['courses'],
            start_strike=datetime.fromisoformat(row['start_strike']),
            end_strike=datetime.fromisoformat(row['end_strike']), user_id=row['user_id']
        ))
    db.flush()

    # Insert achievements
    for _, row in achievements.iterrows():
        db.add(Achievements(
            id=row['id'], experience=row['experience'], picture_id=row['picture_id']
        ))
    db.flush()

    # Insert exercise feedback
    for _, row in exercise_feedback.iterrows():
        db.add(Exercise_feedback(
            id=row['id'], message=row['message'], user_id=row['user_id'],
            exercise_id=row['exercise_id'], picture_id=row['picture_id']
        ))
    db.flush()

    # Insert comments
    for _, row in comments.iterrows():
        db.add(Comments(
            id=row['id'],
            description=row['description'],
            reactions=row['reactions'],
            user_id=row['user_id'],
            post_id=row['post_id'] if pd.notna(row['post_id']) else None
        ))
    db.flush()


    # Insert progresses
    for _, row in progresses.iterrows():
        db.add(Progresses(
            id=row['id'], user_course_id=row['user_course_id'], stage=row['stage']
        ))
    db.commit()

    print("CSV data added successfully.")

# Main function to recreate tables and load CSV data
def main():
    from database import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Add data from CSV
    db = next(get_db())
    add_data_from_csv(db)
    print("Database initialized with CSV data.")

if __name__ == "__main__":
    main()
