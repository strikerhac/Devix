from datetime import datetime

from app.schema.base_schema import *


class AddSiteRequestSchema(BaseSchema):
    site_name: str
    status: str

    region_name: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    city: str | None = None


class EditSiteRequestSchema(AddSiteRequestSchema):
    site_id: int


class GetSiteResponseSchema(EditSiteRequestSchema):
    creation_date: str
    modification_date: str

class GetTotalRacksSchema(BaseSchema):
    name: str
    value: int


class RackLeafLetSchema(BaseSchema):
    longitude: str
    latitude: str

class TopRacksSchema(BaseSchema):
    name: str
    value: int

class AddRackRequestSchema(BaseSchema):
    rack_name: str
    site_name: str
    status: str
    manufacture_date: datetime| None = None # Date format: YYYY-MM-DD
    rfs_date: datetime | None = None
    serial_number: str | None = None
    # manufacture_date: datetime | None = None
    unit_position: str | None = None
    ru: int | None = None
    # rfs_date: datetime | None = None
    height: int | None = None
    width: int | None = None
    depth: int | None = None
    pn_code: str | None = None
    rack_model: str | None = None
    floor: str | None = None

    @validator('manufacture_date', 'rfs_date', pre=True)
    def parse_date(cls, v):
        if v is not None and not isinstance(v, datetime):
            try:
                parsed_date = datetime.strptime(v, '%Y-%m-%d')
                if not (
                        1000 <= parsed_date.year <= 9999 and 1 <= parsed_date.month <= 12 and 1 <= parsed_date.day <= 31):
                    raise ValueError('Date does not have a valid year, month, or day.')
                return parsed_date
            except ValueError:
                raise ValueError('Invalid date format. Date should be in YYYY-MM-DD format and must have a valid year, month, or day')
        return v


class EditRackRequestSchema(AddRackRequestSchema):
    rack_id: int


class GetRackResponseSchema(EditRackRequestSchema):
    creation_date: str
    modification_date: str


class GetRackBySiteRequestSchema(BaseSchema):
    site_name: str


class GetRackByRackNameRequestSchema(BaseSchema):
    rackname: str


class getLocationDevice(BaseSchema):
    name : str
    value : int


class location(BaseSchema):
    name : str
    value : str