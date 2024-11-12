from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import Settings

engine = create_engine(Settings.db_url)
session_local = sessionmaker(autoflush=False, bind=engine)
base = declarative_base()



