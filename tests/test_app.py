from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from app import app
from database import Base, get_db
from models import ExecutionStatistics

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    command.upgrade(config, "head")
    db = TestingSessionLocal()

    test_data = [
        ExecutionStatistics(
            tenant_name="ULVEGR",
            task_id="validate_schema",
            start_date_time=datetime.strptime("2024-08-20 11:38:46.702", "%Y-%m-%d %H:%M:%S.%f"),
            duration=1.05,
            warehouse_size="Small",
            number_of_campaigns=31,
            number_of_customers=22320370,
        ),
        ExecutionStatistics(
            tenant_name="ULVEGR",
            task_id="count_plan_ids_to_execute",
            start_date_time=datetime.strptime("2024-08-20 11:38:51.490", "%Y-%m-%d %H:%M:%S.%f"),
            duration=5.01,
            warehouse_size="Medium",
            number_of_campaigns=50,
            number_of_customers=20000000,
        ),
        ExecutionStatistics(
            tenant_name="ULVEGR",
            task_id="prepare_stream_constraint",
            start_date_time=datetime.strptime("2024-08-20 11:39:07.889", "%Y-%m-%d %H:%M:%S.%f"),
            duration=25.5,
            warehouse_size="Large",
            number_of_campaigns=100,
            number_of_customers=30000000,
        ),
    ]
    db.add_all(test_data)
    db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


def test_select_warehouse(setup_database):
    request_data = [
        {
            "tenant_name": "ULVEGR",
            "task_id": "validate_schema",
            "start_date_time": "2024-08-20T11:38:46.702Z",
            "duration": 1.05,
            "warehouse_size": "X-Small",
            "number_of_campaigns": 31,
            "number_of_customers": 22320370,
        },
        {
            "tenant_name": "ULVEGR",
            "task_id": "count_plan_ids_to_execute",
            "start_date_time": "2024-08-20T11:38:51.490Z",
            "duration": 5.01,
            "warehouse_size": "X-Small",
            "number_of_campaigns": 50,
            "number_of_customers": 20000000,
        },
        {
            "tenant_name": "ULVEGR",
            "task_id": "prepare_stream_constraint",
            "start_date_time": "2024-08-20T11:39:07.889Z",
            "duration": 25.5,
            "warehouse_size": "X-Small",
            "number_of_campaigns": 100,
            "number_of_customers": 30000000,
        },
    ]

    response = client.post("/select_warehouse", json=request_data)
    assert response.status_code == 200
    expected_response = [
        {"task_id": "validate_schema", "selected_warehouse": "Small"},
        {"task_id": "count_plan_ids_to_execute", "selected_warehouse": "Medium"},
        {"task_id": "prepare_stream_constraint", "selected_warehouse": "Large"},
    ]
    assert response.json() == expected_response
