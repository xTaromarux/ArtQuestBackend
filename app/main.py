import logging
import time
import threading
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
import sys
import signal
from fastapi.middleware.cors import CORSMiddleware

# Dodaj katalog główny projektu do ścieżki Pythona
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Dodaj katalog 'app' do ścieżki Pythona
sys.path.append(str(Path(__file__).resolve().parent))

# Ładowanie zmiennych środowiskowych bez wyświetlania informacji
load_dotenv(dotenv_path="fastapidev.env")

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tworzenie instancji FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwala na wszystkie pochodzenia
    allow_credentials=True,
    allow_methods=["*"],  # Pozwala na wszystkie metody HTTP
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki
)

# Importowanie routerów z modułów
from app.services import (
    users as user_service,
    posts as post_service,
    courses as course_service,
    views as views_service,
    progresses as progresses_service,
    comments as comments_service,
    exercises as exercises_service,
    statistic as statistic_service,
    exercise_feedback as exercise_feedback_service,
    pictures as pictures_service,
    achievements as achievements_service
)

# Dodawanie tras do aplikacji FastAPI
app.include_router(user_service.router, prefix="/api")
app.include_router(post_service.router, prefix="/api")
app.include_router(course_service.router, prefix="/api")
app.include_router(exercises_service.router, prefix="/api")
app.include_router(views_service.router, prefix="/api")
app.include_router(progresses_service.router, prefix="/api")
app.include_router(comments_service.router, prefix="/api")
app.include_router(statistic_service.router, prefix="/api")
app.include_router(exercise_feedback_service.router, prefix="/api")
app.include_router(pictures_service.router, prefix="/api")
app.include_router(achievements_service.router, prefix="/api")
# Trasa testowa
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Funkcja logowania
def log_info(stop_event):
    while not stop_event.is_set():
        logger.info("It works!")
        time.sleep(2)

# Główna funkcja uruchamiająca FastAPI i logowanie
def main():
    stop_event = threading.Event()

    def handle_sigint(signal, frame):
        logger.info("Received SIGINT, shutting down.")
        stop_event.set()
        sys.exit(0)

    # Obsługa sygnału przerwania
    signal.signal(signal.SIGINT, handle_sigint)

    # Uruchomienie logowania w osobnym wątku
    log_thread = threading.Thread(target=log_info, args=(stop_event,))
    log_thread.start()

    # Uruchomienie aplikacji FastAPI
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
    finally:
        stop_event.set()

if __name__ == "__main__":
    main()
