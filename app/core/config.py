from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_TITLE: str = "FastAPI Application"
    APP_VERSION: str = "0.1.0"

    class Config:
        env_file = ".env"


settings = Settings()
