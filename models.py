# models.py
from sqlalchemy import TIMESTAMP, Column, Float, Integer, MetaData, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExecutionStatistics(Base):
    __tablename__ = "EXECUTION_STATISTICS"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_name = Column(String, nullable=False)
    task_id = Column(String, nullable=False)
    start_date_time = Column(TIMESTAMP, nullable=False)
    duration = Column(Float, nullable=False)
    warehouse_size = Column(String(20), nullable=True)
    number_of_campaigns = Column(Integer, nullable=True)
    number_of_customers = Column(Integer, nullable=True)
