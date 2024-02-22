from sqlalchemy import ForeignKey, Column, Boolean, Integer, String, DateTime, Date
from datetime import datetime

from app.core.config import Base


class AutoDiscoveryTable(Base):
    __tablename__ = "auto_discovery_table"
    discovery_id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(50), nullable=False)
    subnet = Column(String(50), nullable=False)
    os_type = Column(String(500), nullable=True)
    make_model = Column(String(500), nullable=True)
    function = Column(String(500), nullable=True)
    vendor = Column(String(500), nullable=True)
    snmp_status = Column(String(50), nullable=True)
    snmp_version = Column(String(50), nullable=True)
    ssh_status = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AutoDiscoveryNetworkTable(Base):
    __tablename__ = "auto_discovery_network_table"
    network_id = Column(Integer, primary_key=True, autoincrement=True)
    network_name = Column(String(50), nullable=False)
    subnet = Column(String(50), nullable=False)
    no_of_devices = Column(Integer, default=0, nullable=True)
    scan_status = Column(String(50), default="InActive", nullable=False)
    excluded_ip_range = Column(String(200), default="0", nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SNMP_CREDENTIALS_TABLE(Base):
    __tablename__ = 'snmp_credentials_table'
    credentials_id = Column(Integer, primary_key=True)
    category = Column(String(100))
    credentials = Column(String(100),nullable=True)
    profile_name = Column(String(250),nullable=True)
    description = Column(String(250),nullable=True)
    ip_address = Column(String(50),nullable=True)
    snmp_read_community = Column(String(50),nullable=True)
    snmp_port = Column(String(100),nullable=True)
    username = Column(String(100),nullable=True)
    password = Column(String(100),nullable=True)
    encryption_password = Column(String(100),nullable=True)
    authentication_method = Column(String(50),nullable=True)
    encryption_method = Column(String(50),nullable=True)
    date = Column(DateTime, default=datetime.now())
    creation_date = Column(DateTime,default=datetime.now())
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}