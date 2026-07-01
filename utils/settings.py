import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://townsq.octadesk.com/login")
    USERNAME: str = os.getenv("USERNAME", "")
    PASSWORD: str = os.getenv("PASSWORD", "")
    BROWSER: str = os.getenv("BROWSER", "chromium")
    HEADLESS: bool = _to_bool(os.getenv("HEADLESS"), True)
    TIMEOUT: int = _to_int(os.getenv("TIMEOUT"), 30000)


settings = Settings()