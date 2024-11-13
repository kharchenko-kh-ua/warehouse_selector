from os import getenv
from typing import List

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database import get_db
from models import ExecutionStatistics

DATABASE_URI = getenv("DATABASE_URL", "postgresql://user:password@db/dbname")
engine = create_engine(DATABASE_URI)

app = FastAPI()


class ExecutionStat(BaseModel):
    tenant_name: str
    task_id: str
    start_date_time: str
    duration: float
    warehouse_size: str
    number_of_campaigns: int
    number_of_customers: int


class WarehouseSelectionResponse(BaseModel):
    task_id: str
    selected_warehouse: str


def choose_warehouse(record: ExecutionStat, db: Session) -> str:
    small_max = (
        db.query(ExecutionStatistics)
        .filter(ExecutionStatistics.warehouse_size == "Small")
        .order_by(ExecutionStatistics.duration.desc())
        .first()
    )
    medium_max = (
        db.query(ExecutionStatistics)
        .filter(ExecutionStatistics.warehouse_size == "Medium")
        .order_by(ExecutionStatistics.duration.desc())
        .first()
    )

    if not small_max or not medium_max:
        return record.warehouse_size
    if record.duration <= small_max.duration:
        return "Small"
    elif record.duration <= medium_max.duration:
        return "Medium"
    else:
        return "Large"


@app.post("/select_warehouse", response_model=List[WarehouseSelectionResponse])
def select_warehouse(data: List[ExecutionStat], db: Session = Depends(get_db)):
    response = []
    for record in data:
        selected_warehouse = choose_warehouse(record, db)
        response.append({"task_id": record.task_id, "selected_warehouse": selected_warehouse})
    return response
