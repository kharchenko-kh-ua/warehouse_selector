from os import getenv

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from app import app
from database import Base, get_db

TEST_DATABASE_URL = getenv("DATABASE_URL", "postgresql://user:password@db/dbname")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
