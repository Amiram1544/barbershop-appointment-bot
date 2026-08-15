import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Create .env and set BOT_TOKEN.")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./data/app.db",
)

TIMEZONE = os.getenv("TIMEZONE", "UTC")

BOT_USERNAME = os.getenv("BOT_USERNAME", "")

PENDING_HOLD_MINUTES = int(os.getenv("PENDING_HOLD_MINUTES", "15"))
