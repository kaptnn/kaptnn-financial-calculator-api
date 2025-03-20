from loguru import logger
from functools import wraps
from typing import Callable, Any
from dependency_injector.wiring import inject as di_inject
from app.services.base_service import BaseService

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