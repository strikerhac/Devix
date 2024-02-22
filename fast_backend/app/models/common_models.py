from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.core.config import Base


class FailedDevicesTable(Base):
    __tablename__ = 'failed_devices_table'
    failure_id = Column(Integer, primary_key=True)
    ip_address = Column(String(50), nullable=False)
    device_type = Column(String(50), nullable=False)
    date = Column(DateTime, default=datetime.now(), nullable=False)
    failure_reason = Column(String(2000), nullable=False)
    module = Column(String(50), nullable=False)
