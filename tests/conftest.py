import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.core.database import Database
from app.core.config import configs

test_db = Database(configs.DB_URI)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    test_db.create_database()
    yield

@pytest.fixture(scope="function")
def session() -> Session: # type: ignore
    with test_db.session() as session:
        yield session

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
