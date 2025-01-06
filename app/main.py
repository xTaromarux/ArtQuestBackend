import logging
import time
import threading
import uvicorn
from pathlib import Path
import sys
import signal

from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode


# Add project root directory and 'app' to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent))

# Load environment variables
load_dotenv(dotenv_path="fastapidev.env")
load_dotenv(dotenv_path=".env")

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI()


# Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# OAuth keys from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI_GOOGLE = os.getenv("REDIRECT_URI_GOOGLE")
REDIRECT_URI_GITHUB = os.getenv("REDIRECT_URI_GITHUB")

@app.get("/login/{provider}")
async def login(provider: str):
    """
    Handles login by redirecting to the provider's OAuth authorization URL.
    """
    if provider == "google":
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urlencode({
                "client_id": GOOGLE_CLIENT_ID,
                "redirect_uri": REDIRECT_URI_GOOGLE,
                "response_type": "code",
                "scope": "openid email profile",
            })
        )
    elif provider == "github":
        auth_url = (
            "https://github.com/login/oauth/authorize?"
            + urlencode({
                "client_id": GITHUB_CLIENT_ID,
                "redirect_uri": REDIRECT_URI_GITHUB,
                "scope": "user:email",
            })
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    return RedirectResponse(auth_url)

@app.get("/oauth-callback")
async def oauth_callback(provider: str = None, code: str = None):
    """
    Handles OAuth callback to exchange code for access token and fetch user info.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    if provider == "google":
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI_GOOGLE,
            "grant_type": "authorization_code",
            "code": code,
        }
    elif provider == "github":
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI_GITHUB,
            "code": code,
        }
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    headers = {"Accept": "application/json"}
    token_response = requests.post(token_url, data=token_data, headers=headers)
    token_json = token_response.json()

    access_token = token_json.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    if provider == "google":
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    elif provider == "github":
        user_info_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    user_info = user_info_response.json()
    return JSONResponse(user_info)

# Import routers from services
from services import (
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

# Include service routers
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

def log_info(stop_event):
    """
    Periodically logs "It works!" to verify server activity.
    """
    while not stop_event.is_set():
        logger.info("It works!")
        time.sleep(2)

def main():
    """
    Main function to start the FastAPI server and a logging thread.
    """
    stop_event = threading.Event()

    def handle_sigint(signal, frame):
        logger.info("Received SIGINT, shutting down.")
        stop_event.set()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)
    log_thread = threading.Thread(target=log_info, args=(stop_event,))
    log_thread.start()

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        stop_event.set()

if __name__ == "__main__":
    main()
