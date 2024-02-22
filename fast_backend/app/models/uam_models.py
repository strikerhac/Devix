from datetime import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date

from app.core.config import Base


#
#
#

# ** UAM Models **

#
#
#


class UamDeviceTable(Base):
    __tablename__ = "uam_device_table"
    uam_id = Column(Integer, primary_key=True, autoincrement=True)
    atom_id = Column(
        Integer,
        ForeignKey("atom_table.atom_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    status = Column(String(50), nullable=False)

    software_type = Column(String(50), nullable=True)
    software_version = Column(String(50), nullable=True)
    patch_version = Column(String(50), nullable=True)
    manufacturer = Column(String(50), nullable=True)
    hw_eos_date = Column(Date, nullable=True)
    hw_eol_date = Column(Date, nullable=True)
    sw_eos_date = Column(Date, nullable=True)
    sw_eol_date = Column(Date, nullable=True)
    rfs_date = Column(Date, nullable=True)
    authentication = Column(String(10), nullable=True)
    serial_number = Column(String(50), nullable=True)
    pn_code = Column(String(50), nullable=True)
    subrack_id_number = Column(String(50), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    hardware_version = Column(String(50), nullable=True)
    max_power = Column(String(50), nullable=True)
    site_type = Column(String(50), nullable=True)
    source = Column(String(50), nullable=True)
    stack = Column(String(50), nullable=True)
    contract_number = Column(String(50), nullable=True)
    contract_expiry = Column(Date, nullable=True)
    uptime = Column(Date, nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BoardTable(Base):
    __tablename__ = "board_table"
    board_id = Column(Integer, primary_key=True, autoincrement=True)
    uam_id = Column(
        Integer,
        ForeignKey("uam_device_table.uam_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    board_name = Column(String(250), nullable=False)
    status = Column(String(50), nullable=False)

    hardware_version = Column(String(50), nullable=True)
    device_slot_id = Column(String(250), nullable=True)
    software_version = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    eos_date = Column(Date, nullable=True)
    eol_date = Column(Date, nullable=True)
    rfs_date = Column(Date, nullable=True)
    pn_code = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SubboardTable(Base):
    __tablename__ = "subboard_table"
    subboard_id = Column(Integer, primary_key=True, autoincrement=True)
    uam_id = Column(
        Integer,
        ForeignKey("uam_device_table.uam_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    subboard_name = Column(String(250), nullable=False)
    status = Column(String(50), nullable=False)

    subboard_type = Column(String(150), nullable=True)
    subrack_id = Column(String(250), nullable=True)
    slot_number = Column(String(250), nullable=True)
    subslot_number = Column(String(250), nullable=True)
    hardware_version = Column(String(50), nullable=True)
    software_version = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)

    manufacture_date = Column(Date, nullable=True)
    eos_date = Column(Date, nullable=True)
    eol_date = Column(Date, nullable=True)
    rfs_date = Column(Date, nullable=True)
    pn_code = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SfpsTable(Base):
    __tablename__ = "sfp_table"
    sfp_id = Column(Integer, primary_key=True, autoincrement=True)
    uam_id = Column(
        Integer,
        ForeignKey("uam_device_table.uam_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    serial_number = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

    media_type = Column(String(50), nullable=True)
    port_name = Column(String(250), nullable=True)
    port_type = Column(String(50), nullable=True)
    connector = Column(String(50), nullable=True)
    mode = Column(String(50), nullable=True)
    speed = Column(String(50), nullable=True)
    wavelength = Column(String(50), nullable=True)
    manufacturer = Column(String(250), nullable=True)
    optical_direction_type = Column(String(50), nullable=True)
    pn_code = Column(String(50), nullable=True)
    eos_date = Column(Date, nullable=True)
    eol_date = Column(Date, nullable=True)
    rfs_date = Column(Date, nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LicenseTable(Base):
    __tablename__ = "license_table"
    license_id = Column(Integer, primary_key=True, autoincrement=True)
    uam_id = Column(
        Integer,
        ForeignKey("uam_device_table.uam_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    license_name = Column(String(250), nullable=False)
    status = Column(String(50), nullable=False)

    license_description = Column(String(250), nullable=True)
    rfs_date = Column(Date, nullable=True)
    activation_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    grace_period = Column(String(10), nullable=True)
    serial_number = Column(String(50), nullable=True)
    capacity = Column(String(50), nullable=True)
    usage = Column(String(50), nullable=True)
    pn_code = Column(String(50), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SntcTable(Base):
    __tablename__ = "sntc_table"
    sntc_id = Column(Integer, primary_key=True, autoincrement=True)
    pn_code = Column(String(50), nullable=False)

    hw_eos_date = Column(Date, nullable=True)
    hw_eol_date = Column(Date, nullable=True)
    sw_eos_date = Column(Date, nullable=True)
    sw_eol_date = Column(Date, nullable=True)
    manufacture_date = Column(Date, nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ApsTable(Base):
    __tablename__ = "aps_table"
    ap_id = Column(Integer, primary_key=True, autoincrement=True)
    uam_id = Column(
        Integer,
        ForeignKey("uam_device_table.uam_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    ap_ip = Column(String(50), nullable=False)

    ap_name = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)
    ap_model = Column(String(50), nullable=True)
    hardware_version = Column(String(50), nullable=True)
    software_version = Column(String(50), nullable=True)
    description = Column(String(200), nullable=True)

    creation_date = Column(DateTime, default=datetime.now())
    modification_date = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
