import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku fastapidev.env
load_dotenv(dotenv_path="fastapidev.env")

# Utwórz URL bazy danych
DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

# Tworzenie silnika bazy danych
engine = _sql.create_engine(DATABASE_URL)

# Konfiguracja sesji bazy danych
session_local = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklaracja podstawowej klasy modelu
Base = _declarative.declarative_base()

# Funkcja zależności do uzyskiwania sesji bazy danych
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
