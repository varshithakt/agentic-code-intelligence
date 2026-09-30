"""Environment-backed application configuration."""
import os
from dataclasses import dataclass

@dataclass
class Settings:
    database_path: str
    log_level: str
    allowed_origins: tuple
    session_ttl: int

def load_settings():
    raw_origins=os.getenv("ALLOWED_ORIGINS","http://localhost:8000")
    try: ttl=max(60,min(int(os.getenv("SESSION_TTL","3600")),86400))
    except ValueError: ttl=3600
    return Settings(os.getenv("DATABASE_PATH","data/users.db"),os.getenv("LOG_LEVEL","INFO").upper(),tuple(x.strip() for x in raw_origins.split(",") if x.strip()),ttl)
