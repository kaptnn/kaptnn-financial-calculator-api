from contextlib import AbstractContextManager
from typing import Any, Callable, Type, TypeVar
from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)

class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model: Type[T]) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_options(self, schema: Type[T])->Any:
        with self.session_factory() as session:
            statement = select(self.model)
            result = session.exec(statement).all()

            data = [self.model.from_orm(item) for item in result]

            return {
                "data": data,
                "message": "Data retrieved successfully"
            }
        
    def close_scoped_session(self):
        with self.session_factory() as session:
            session.close()