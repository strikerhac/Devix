from datetime import datetime

from app.schema.base_schema import BaseSchema



class GetApsSchema(BaseSchema):
    ap_id : int
    ap_ip : str | None = None
    ap_name : str | None = None
    serial_number : str | None = None
    ap_model : str |None = None
    hardware_version : str | None = None
    software_version : str |  None = None
    description  : str | None = None

