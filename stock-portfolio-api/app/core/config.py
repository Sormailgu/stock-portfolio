import os
import logging

class Settings:
    PROJECT_NAME: str = "Stock Portfolio API"
    API_PREFIX: str = "/api"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ALLOWED_ORIGINS = ["*"]  # For CORS, update as needed
    LOG_LEVEL: int = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "data/stocks.csv")
    # Example: Database URL (if you add a database later)
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()