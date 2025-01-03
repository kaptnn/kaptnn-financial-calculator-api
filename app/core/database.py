from typing import Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine

class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(
            db_url,
            echo=False, 
            pool_pre_ping=True  
        )

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()