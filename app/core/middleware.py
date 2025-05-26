from fastapi import FastAPI, Request
from loguru import logger
from functools import wraps
from typing import Callable, Any
from dependency_injector.wiring import inject as di_inject
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.base_service import BaseService
from app.core.config import configs

def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @di_inject
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)

        for value in kwargs.values():
            if isinstance(value, BaseService):        
                try:
                    value.close_scoped_session()
                except Exception as exc:
                    logger.error('Failed to close scoped session: {}', exc)
            
        return result
    return wrapper

def register_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=configs.CLIENT_SECRET
    )

    origins = [
        "http://localhost:3000"
    ]
    
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )