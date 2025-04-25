from typing import AsyncGenerator, Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(
            db_url,
            echo=False, 
            pool_pre_ping=True  
        )
        # self._sessionmaker = sessionmaker(
        #     bind=self._engine,
        #     class_=AsyncSession,
        #     autoflush=False,
        #     expire_on_commit=False,
        # )

    def create_database(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    # async def init_models(self) -> None:
    #     async with self._engine.begin() as conn:
    #         await conn.run_sync(SQLModel.metadata.create_all)

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

    # async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    #     async with self._sessionmaker() as session:
    #         try:
    #             yield session
    #             await session.commit()
    #         except Exception:
    #             await session.rollback()
    #             raise
    #         finally:
    #             session.expunge_all()
    #             session.close()