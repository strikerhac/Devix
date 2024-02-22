from datetime import datetime

from app.schema.base_schema import BaseSchema


class GetLicenseResponseSchema(BaseSchema):
    license_id: int
    uam_id: int
    device_name: str

    license_name: str
    status: str

    license_description: str | None = None
    rfs_date: datetime | None = None
    activation_date: datetime | None = None
    expiry_date: datetime | None = None
    grace_period: str | None = None
    serial_number: str | None = None
    capacity: str | None = None
    usage: str | None = None
    pn_code: str | None = None

    creation_date: datetime
    modification_date: datetime
