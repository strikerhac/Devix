from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime

from app.core.config import Base


class Monitoring_Credentails_Table(Base):
    __tablename__ = "monitoring_credentials_table"
    monitoring_credentials_id = Column(
        Integer, primary_key=True, autoincrement=True
    )

    profile_name = Column(String(250), nullable=False)
    category = Column(String(100), nullable=False)

    description = Column(String(250), nullable=True)
    snmp_read_community = Column(String(50), nullable=True)
    snmp_port = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    encryption_password = Column(String(100), nullable=True)
    authentication_method = Column(String(50), nullable=True)
    encryption_method = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Monitoring_Devices_Table(Base):
    __tablename__ = "monitoring_devices_table"
    monitoring_device_id = Column(Integer, primary_key=True, autoincrement=True)
    atom_id = Column(
        Integer,
        ForeignKey("atom_table.atom_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    source = Column(String(50), nullable=True)
    active = Column(String(50), nullable=True)
    ping_status = Column(String(40), nullable=True)
    snmp_status = Column(String(40), nullable=True)
    active_id = Column(String(80), nullable=True)
    device_heatmap = Column(String(40), nullable=True)

    monitoring_credentials_id = Column(
        Integer,
        ForeignKey(
            "monitoring_credentials_table.monitoring_credentials_id",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Monitoring_Alerts_Table(Base):
    __tablename__ = "monitoring_alerts_table"
    monitoring_alert_id = Column(Integer, primary_key=True, autoincrement=True)
    monitoring_device_id = Column(
        Integer,
        ForeignKey(
            "monitoring_devices_table.monitoring_device_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    description = Column(String(2000), nullable=True)
    alert_type = Column(String(50), nullable=True)
    category = Column(String(50), nullable=True)
    alert_status = Column(String(50), nullable=True)
    mail_status = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Alert_Cpu_Threshold_Table(Base):
    __tablename__ = "alert_cpu_threshold_table"

    id = Column(Integer, primary_key=True, autoincrement=True)

    ip_address = Column(String(100), nullable=False)
    low_threshold = Column(Integer, nullable=True)
    medium_threshold = Column(Integer, nullable=True)
    critical_threshold = Column(Integer, nullable=True)
    pause_min = Column(Integer, nullable=True)
    alert_active = Column(String(20), default='Active', nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Alert_Memory_Threshold_Table(Base):
    __tablename__ = "alert_memory_threshold_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(100), nullable=False)
    low_threshold = Column(Integer, nullable=True)
    medium_threshold = Column(Integer, nullable=True)
    critical_threshold = Column(Integer, nullable=True)
    pause_min = Column(Integer, nullable=True)
    alert_active = Column(String(20), default='Active', nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
