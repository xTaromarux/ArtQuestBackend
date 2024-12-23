from database import engine, Base
from models.difficulties import Difficulties
from models.users import Users
from models.posts import Posts
from models.progresses import Progresses
from models.courses import Courses
from models.pictures import Pictures
from sqlalchemy import inspect, text
from sqlalchemy.orm import configure_mappers

# Directly delete dependent `pictures` and `courses` tables using CASCADE
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS pictures CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS courses CASCADE"))

# Refresh database metadata after deleting tables
Base.metadata.reflect(bind=engine)

# Attempt to delete the remaining tables again to make sure the database is cleared
Base.metadata.drop_all(bind=engine, checkfirst=True)
print("The tables have been removed.")

# Debugging relationships in models to confirm their correctness
for cls in [Courses, Progresses, Users, Difficulties]:
    print(f"{cls.__name__} relationships: {inspect(cls).relationships.keys()}")

# Creating tables in the database
Base.metadata.create_all(bind=engine)
print("The tables have been created.")
