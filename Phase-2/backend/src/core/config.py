from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    database_url: str = "sqlite:///./todo_app.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # JWT settings (for compatibility)
    jwt_secret_key: str = "your-shared-secret-key-here-replace-with-a-real-secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 1440  # 24 hours (1440 minutes)
    jwt_expected_audience: str = "todo-users"
    # Better Auth settings
    better_auth_secret: str = "your_super_secret_1234567890"

    class Config:
        env_file = ".env"


settings = Settings()