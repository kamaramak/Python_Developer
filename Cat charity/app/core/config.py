from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "Сервис пожертвований."
    description: str = "Сервис дает возможность внести пожертование в фонд."
    database_url: str | None = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = "user@test.ru"
    first_superuser_password: Optional[str] = "123123123"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
