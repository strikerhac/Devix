from datetime import datetime

from pydantic import validator

from app.schema.base_schema import BaseSchema



class GetSntcSchema(BaseSchema):
    sntc_id : int
    pn_code : str | None = None
    hw_eos_date : datetime | None = None
    hw_eol_date : datetime | None =None
    sw_eos_date : datetime | None = None
    sw_eol_date : datetime | None = None
    manufacture_date : datetime | None = None
    creation_date : datetime | None = None
    modification_date : datetime | None = None


class SyncFromInventorySchema(BaseSchema):
    pn_code: str


class SyncResult(BaseSchema):
    object_id: int
    sync_type: str
    success: bool
    error_message: str


class Response200(BaseSchema):
    data: dict
    message: str


class SntcEditRequest(BaseSchema):
    sntc_id: int
    pn_code: str
    hw_eos_date: datetime
    hw_eol_date: datetime
    sw_eos_date: datetime
    sw_eol_date: datetime
    manufacture_date: datetime


class ListtDeleteResponseSchema(BaseSchema):
    data: list[int]
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]


class DeletePnCodeSchema(BaseSchema):
    pn_code : str

class SummeryResponseSchema(BaseSchema):
    data: list[dict]
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class Response200(BaseSchema):
    data: dict
    message: str


class AddSntcRequestSchema(BaseSchema):
    pn_code : str
    hw_eos_date: datetime  | None = None
    hw_eol_date: datetime  | None = None
    sw_eos_date: datetime  | None = None
    sw_eol_date: datetime  | None = None
    manufacture_date: datetime  | None = None

    @validator('hw_eos_date', 'hw_eol_date','sw_eos_date','sw_eol_date','manufacture_date', pre=True)
    def parse_date(cls, v):
        if v is not None and not isinstance(v, datetime):
            try:
                parsed_date = datetime.strptime(v, '%Y-%m-%d')
                if not (
                        1000 <= parsed_date.year <= 9999 and 1 <= parsed_date.month <= 12 and 1 <= parsed_date.day <= 31):
                    raise ValueError('Date does not have a valid year, month, or day.')
                return parsed_date
            except ValueError:
                raise ValueError('Invalid date format. Date should be in YYYY-MM-DD format and must have a valid year, month, or day.')
        return v