from datetime import datetime

from app.schema.base_schema import *


class AddBoardRequestSchema(BaseSchema):
    device_name: str
    board_name: str

    device_slot_id: str | None = None
    software_version: str | None = None
    hardware_version: str | None = None
    serial_number: str
    manufacturer_date: datetime | None = None
    status: str
    eos_date: datetime | None = None
    eol_date: datetime | None = None
    rfs_date: datetime | None = None
    pn_code: str


class GetBoardResponseSchema(BaseSchema):
    board_id:int
    board_name: str
    device_name: str
    serial_number: str
    pn_code: str
    status: str
    device_slot_id: str | None = None
    software_version: str | None = None
    hardware_version: str | None = None
    manufacture_date: datetime | None = None
    eos_date: datetime | None = None
    eol_date: datetime | None = None
    creation_date: datetime
    modification_date: datetime


class GetSubboardResponseSchema(BaseSchema):
    subboard_id : int 
    subboard_name: str
    device_name: str
    serial_number: str
    status: str
    pn_code: str

    subboard_type: str | None = None
    subrack_id: str | None = None
    slot_number: str | None = None
    subslot_number: str | None = None
    device_slot_id: str | None = None
    software_version: str | None = None
    hardware_version: str | None = None

    manufacturer_date: datetime | None = None
    eos_date: datetime | None = None
    eol_date: datetime | None = None

    creation_date: datetime
    modification_date: datetime
