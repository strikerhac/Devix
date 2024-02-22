from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, DateTime, Date
from datetime import datetime

from app.core.config import Base


class SiteTable(Base):
    __tablename__ = "site_table"
    site_id = Column(Integer, primary_key=True, autoincrement=True)

    site_name = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

    region_name = Column(String(50), nullable=True, default="N/A")
    latitude = Column(String(70), nullable=True, default="0")
    longitude = Column(String(70), nullable=True, default="0")
    city = Column(String(50), nullable=True, default="N/A")

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data


class RackTable(Base):
    __tablename__ = "rack_table"

    rack_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(
        Integer,
        ForeignKey("site_table.site_id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    rack_name = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

    serial_number = Column(String(50), nullable=True)
    manufacture_date = Column(DateTime,nullable=True)
    unit_position = Column(String(20), nullable=True)#default="N/A"
    ru = Column(Integer, nullable=True, default=0)
    rfs_date = Column(DateTime,nullable=True)
    height = Column(Integer, nullable=True, default=0)
    width = Column(Integer, nullable=True, default=0)
    depth = Column(Integer, nullable=True, default=0)
    pn_code = Column(String(50), nullable=True )
    rack_model = Column(String(50), nullable=True )
    floor = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = str(value)
        return data
