import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from dotenv import load_dotenv

# Load environment variables from fastapidev.env file
load_dotenv(dotenv_path="fastapidev.env")

# Create a database URL
DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

# Creating a database engine
engine = _sql.create_engine(DATABASE_URL)

# Database session configuration
session_local = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaration of basic model class
Base = _declarative.declarative_base()

# Dependency function to get database sessions
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
