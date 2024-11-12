from database import Base, engine
from models.exercises import Exercises
from models.difficulty import Difficulty
from models.pictures import Pictures
from models.users import Users
from models.progress import Progress
from models.posts import Posts


def create_models():
    Base.metadata.create_all(bind=engine)