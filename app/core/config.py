import os
from typing import List
from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings 

load_dotenv()

class Configs(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI")
    API_PREFIX: str = "/api/v1"
    
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOAD_DIR_ROOT: str = "./storages"
    
    KEY: str = os.getenv("KEY", "secret")

    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    DB: str = os.getenv("DB", "mysql")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
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

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXP: str = os.getenv("ACCESS_TOKEN_EXP", "1d")
    JWT_REFRESH_TOKEN_EXP: str = os.getenv("REFRESH_TOKEN_EXP", "7d")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    CORS_ORIGINS: List[str] = (
        os.getenv("CORS_ALLOWED_HOSTS", "*").split(",") if os.getenv("CORS_ALLOWED_HOSTS") != "*" else ["*"]
    )

    APPLICATION_ID: str = os.getenv("APPLICATION_ID", "your_application_id")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "your_client_secret")
    TENANT_ID: str = os.getenv("TENANT_ID", "your_tenant_id")
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    MS_GRAPH_BASE_URL: str = "https://graph.microsoft.com/v1.0"
    TOKEN_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"

    NGROK_AUTHTOKEN: str = os.getenv("NGROK_AUTHTOKEN", "secret")
    NGROK_DOMAIN: str = os.getenv('NGROK_DOMAIN', "http://localhost:8000")

    SUPER_ADMIN_NAME: str = os.getenv("SUPER_ADMIN_NAME", "Super Admin")
    SUPER_ADMIN_EMAIL: str = os.getenv("SUPER_ADMIN_EMAIL", "superadmin@gmail.com")
    SUPER_ADMIN_PASSWORD: str = os.getenv("SUPER_ADMIN_PASSWORD", "Password123!")
    SUPER_ADMIN_COMPANY_NAME: str = os.getenv("SUPER_ADMIN_COMPANY_NAME", "Super Admin Company")

class LocalConfig(Configs):
    pass

class ProductionConfig(Configs):
    DEBUG: bool = False

def get_config():
    env = os.getenv('ENV', 'development').lower()
    config_type = {      
        'development': LocalConfig(),
        'prod': ProductionConfig(),
        'production': ProductionConfig(),
    }
    return config_type[env]

configs: Configs = get_config()

