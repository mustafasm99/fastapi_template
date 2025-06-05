from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
import os
from dotenv import load_dotenv
from app.logger.logger import logger

load_dotenv(override=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectSettings(str, Enum):
    production = "production"
    development = "development"
    testing = "testing"


class DatabaseTypes(str, Enum):
    sqlite = "sqlite"
    postgres = "postgres"


class Settings(BaseSettings):
    API_KEY: str
    API_SECRET: str
    PROJECT_NAME: str
    API_VERSION: str

    PROJECT_STATUS: ProjectSettings

    DATABASE_TYPE: str = DatabaseTypes.sqlite

    DATABASE_USERNAME: str | None = None
    DATABASE_PASSWORD: str | None = None
    DATABASE_HOST: str | None = None
    DATABASE_PORT: str | None = None
    DATABASE_NAME: str | None = None
    PROJECT_LOGGER_PATH:str
    MAX_IMAGE_SIZE: int = 1024 * 1024 * 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    MEDIA_PATH: str = "media"

    @property
    def DATABASE_URL(self):
        if self.DATABASE_TYPE == DatabaseTypes.sqlite:
            return "sqlite:///" + BASE_DIR + "\\" + self.DATABASE_NAME
        return f"{self.DATABASE_TYPE}://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"


settings = Settings()

if settings.PROJECT_STATUS == ProjectSettings.development:
    logger.setLevel("DEBUG")
    logger.info(
        f"Project settings loaded: {settings.PROJECT_NAME} - {settings.PROJECT_STATUS}"
    )
    logger.info(f"Database URL: {settings.DATABASE_URL}")
    logger.info(f"API Version: {settings.API_VERSION}")
    logger.info(f"Media Path: {settings.MEDIA_PATH}")
    logger.info(f"Max Image Size: {settings.MAX_IMAGE_SIZE} bytes")
    logger.info(f"API Key: {settings.API_KEY}")
    logger.info(f"API Secret: {settings.API_SECRET}")
    logger.info(f"Database Type: {settings.DATABASE_TYPE}")
else:
    logger.setLevel("INFO")
