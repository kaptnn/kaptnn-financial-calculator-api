from contextlib import AbstractContextManager
from sqlmodel import SQLModel, Session
from typing import Callable, Type, TypeVar

T = TypeVar("T", bound=SQLModel)

class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model
        
    def close_scoped_session(self):
        with self.session_factory() as session:
            session.close()