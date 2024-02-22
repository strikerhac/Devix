from datetime import datetime

from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, DateTime

from app.core.config import Base


# 
# 
# # ** NCM Models **
# 
# 
class NcmDeviceTable(Base):
    __tablename__ = "ncm_device_table"
    ncm_device_id = Column(Integer, primary_key=True, autoincrement=True)
    atom_id = Column(Integer,
                     ForeignKey("atom_table.atom_id", ondelete='CASCADE', onupdate='CASCADE'),
                     nullable=False)

    status = Column(String(50), default='InActive', nullable=False)
    config_change_date = Column(DateTime, nullable=True)
    backup_status = Column(Boolean, nullable=True)
    configuration_status = Column(String(60),nullable=True)
    backup_state = Column(String(25),nullable=True)
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


class NCM_History_Table(Base):
    __tablename__ = "ncm_history_table"
    ncm_history_id = Column(Integer, primary_key=True, autoincrement=True)
    ncm_device_id = Column(Integer,
                           ForeignKey("ncm_device_table.ncm_device_id", ondelete='CASCADE',
                                      onupdate='CASCADE'), nullable=False)

    file_name = Column(String(500), nullable=False)
    configuration_date = Column(DateTime, default=datetime.now(), nullable=False)
    deleted_state = Column(Boolean,nullable=True,default = False)
    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class NCM_Alarm_Table(Base):
    __tablename__ = "ncm_alarm_table"

    ncm_alarm_id = Column(Integer, primary_key=True, autoincrement=True)
    ncm_device_id = Column(Integer,
                           ForeignKey("ncm_device_table.ncm_device_id", ondelete='CASCADE',
                                      onupdate='CASCADE'), nullable=False)

    alarm_category = Column(String(50), nullable=False)
    alarm_title = Column(String(200), nullable=False)
    alarm_description = Column(String(500), nullable=False)
    alarm_status = Column(String(50), default='Open', nullable=False)
    mail_status = Column(String(50), default='no', nullable=False)
    resolve_remarks = Column(String(500), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
