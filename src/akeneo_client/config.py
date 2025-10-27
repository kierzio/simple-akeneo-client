from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("AKENEO_BASE_URL", "")
    client_id: str = os.getenv("AKENEO_CLIENT_ID", "")
    client_secret: str = os.getenv("AKENEO_CLIENT_SECRET", "")
    username: str = os.getenv("AKENEO_USERNAME", "")
    password: str = os.getenv("AKENEO_PASSWORD", "")

def get_settings() -> "Settings":
    s = Settings()
    missing = [k for k, v in s.__dict__.items() if not v]
    if missing:
        # Defer strictness to CLI commands; they can validate and error cleanly.
        pass
    return s
