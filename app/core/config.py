import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings 

load_dotenv()

class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    API_PREFIX: str = "/api/v1"
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    KEY: str = os.getenv("KEY", "secret")

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    DB: str = os.getenv("DB", "mysql")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "FastAPI")

    ENV_DATABASE_MAPPER: dict = {
        "development": DB_NAME,
        "stage": f"{DB_NAME}_stage",
        "testing": f"{DB_NAME}_test",
        "production": DB_NAME,
    }

    DB_ENGINE_MAPPER: dict = {
        "mysql": "mysql+pymysql",
    }

    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "mysql+pymysql")
    DB_URI: str = (
        f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ENV_DATABASE_MAPPER[ENV]}"
    )

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "true").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "false").lower() == "true"
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "true").lower() == "true"
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "true").lower() == "true"

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXP: str = os.getenv("ACCESS_TOKEN_EXP", "1d")
    JWT_REFRESH_TOKEN_EXP: str = os.getenv("REFRESH_TOKEN_EXP", "7d")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    CORS_ORIGINS: List[str] = (
        os.getenv("CORS_ALLOWED_HOSTS", "*").split(",") if os.getenv("CORS_ALLOWED_HOSTS") != "*" else ["*"]
    )

    APPLICATION_ID: str = os.getenv("APPLICATION_ID", "your_application_id")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "your_client_secret")
    TENANT_ID: str = os.getenv("TENANT_ID")
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    MS_GRAPH_BASE_URL: str = "https://graph.microsoft.com/v1.0"
    TOKEN_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    class Config:
        case_sensitive = True

class TestConfigs(Configs):
    ENV: str = "testing"

configs: Configs = Configs() if Configs().ENV != "testing" else TestConfigs()

