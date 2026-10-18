import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

APP_NAME = "AI Chatbot Assistant"

SECRET_KEY = os.getenv(
    "FLASK_SECRET_KEY",
    "local-development-only-change-this"
)

AI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

MAX_MESSAGE_LENGTH = 4000
CHAT_HISTORY_LIMIT = 1007