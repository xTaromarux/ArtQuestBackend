from database import engine, Base
from models.difficulty import Difficulty
from models.users import Users
from models.posts import Posts
from models.progress import Progress
from models.exercises import Exercises
from models.pictures import Pictures
import os
from sqlalchemy.orm import sessionmaker

# Dropping tables in the database
Base.metadata.drop_all(bind=engine)
print("Tables have been dropped.")

# Creating tables in the database
Base.metadata.create_all(bind=engine)
print("Tables have been created.")

# Adding sample data to the Difficulty table
Session = sessionmaker(bind=engine)
session = Session()

sample_difficulties = [
    Difficulty(name="Easy", color="Green", score=1),
    Difficulty(name="Medium", color="Yellow", score=2),
    Difficulty(name="Hard", color="Red", score=3)
]

session.bulk_save_objects(sample_difficulties)
session.commit()
print("Sample data has been added to the Difficulty table.")

