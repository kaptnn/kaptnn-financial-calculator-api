from fastapi import FastAPI
from loguru import logger
from functools import wraps
from typing import Callable, Any
from dependency_injector.wiring import inject as di_inject
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.services.base_service import BaseService
from app.core.config import configs

def inject(func: Callable[..., Any]) -> Callable[..., Any]:
    @di_inject
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        injected_services = [arg for arg in kwargs.values() if isinstance(arg, BaseService)]
        if len(injected_services) == 0:
            return result
        else:
            try:
                injected_services[-1].close_scoped_session()
            except Exception as e:
                logger.error(e)

            return result
    return wrapper

def register_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=configs.CLIENT_SECRET
    )
    
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_credentials=True,
    )