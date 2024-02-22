from datetime import datetime, date

from app.schema.base_schema import *


class TotalDeviceDashboardResponseSchema(BaseSchema):
    name: str
    value: int | None


class GetAllUAMDeviceResponseSchema(BaseSchema):
    uam_id: int

    atom_id: int
    ip_address: str
    device_name: str
    device_type: str
    site_name: str
    rack_name: str

    # status = Column(String(50), nullable=False)

    software_type: str | None = None
    software_version: str | None = None
    patch_version: str | None = None
    manufacturer: str | None = None

    creation_date: datetime
    modification_date: datetime

    hw_eos_date: datetime | None = None
    hw_eol_date: datetime | None = None
    sw_eos_date: datetime | None = None
    sw_eol_date: datetime | None = None
    rfs_date: datetime | None = None
    contract_expiry: datetime | None = None
    uptime: date | None = None
    manufacture_date: datetime | None = None

    authentication: str | None = None
    serial_number: str | None = None
    pn_code: str | None = None
    subrack_id_number: str | None = None
    hardware_version: str | None = None
    max_power: str | None = None
    site_type: str | None = None
    source: str | None = None
    stack: str | None = None
    contract_number: str | None = None
    status:str | None = None


class EditUamDeviceRequestSchema(BaseSchema):
    atom_id: int
    rack_name: str
    function: str

    ru: int | None = None
    section: str | None = None
    department: str | None = None
    criticality: str | None = None
    virtual: str | None = None

    software_version: str | None = None
    manufacturer: str | None = None
    authentication: str | None = None
    serial_number: str | None = None
    pn_code: str | None = None
    subrack_id_number: str | None = None
    source: str | None = None
    stack: str | None = None
    contract_number: str | None = None
    status: str | None = None


class GetSiteByIpResponseSchema(BaseSchema):
    site_name: str

    creation_date: datetime
    modification_date: datetime
    status: str

    region: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    city: str | None = None


class GetRackByIpResponseSchema(BaseSchema):
    rack_name: str
    site_name: str

    creation_date: datetime
    modification_date: datetime
    status: str

    serial_number: str | None = None
    manufacturer_date: datetime | None = None
    unit_position: str | None = None
    rfs_date: datetime | None = None
    height: int | None = None
    width: int | None = None
    depth: int | None = None

    ru: int | None = None
    pn_code: str | None = None
    rack_model: str | None = None
    floor: str | None = None
