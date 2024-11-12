import os
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    project_name: str = "art_quest"
    app_name: str = "art_quest"
    db_host: str = os.getenv('db_host')
    db_port: int = 5432
    db_name: str = os.getenv('db_name')
    db_user: str = os.getenv('db_user')
    db_pass: str = os.getenv('db_pass')
    postgres_user: str = os.getenv('postgres_user')
    postgres_pass: str = os.getenv('postgres_pass')
    db_url: str = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    class Config:
        env_file = ".env"
