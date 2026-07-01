import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://townsq.octadesk.com/login")
    USERNAME: str = os.getenv("USERNAME", "")
    PASSWORD: str = os.getenv("PASSWORD", "")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))


settings = Settings()
