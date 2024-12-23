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

# Add project root directory to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Add directory 'app' to Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Loading environment variables without displaying information
load_dotenv(dotenv_path="fastapidev.env")

# Login configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Importing routers from modules
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

# Adding routes to the FastAPI application
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

# Logging function
def log_info(stop_event):
    while not stop_event.is_set():
        logger.info("It works!")
        time.sleep(2)

# Main function running FastAPI and logging
def main():
    stop_event = threading.Event()

    def handle_sigint(signal, frame):
        logger.info("Received SIGINT, shutting down.")
        stop_event.set()
        sys.exit(0)

    # Interrupt signal handling
    signal.signal(signal.SIGINT, handle_sigint)

    # Running logging in a separate thread
    log_thread = threading.Thread(target=log_info, args=(stop_event,))
    log_thread.start()

    # Launching the FastAPI application
    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
    finally:
        stop_event.set()

if __name__ == "__main__":
    main()
