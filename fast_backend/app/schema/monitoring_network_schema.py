from datetime import datetime
from app.schema.base_schema import *


class GetMonitoringNetworkDevicesSchema(BaseSchema):
    ip_address : str |None = None
    function:str | None = None
    response:str | None = None
    status:str | None = None
    uptime:str | None = None
    vendor:str |None = None
    cpu:str | None = None
    memory:str |None = None
    packets:str |None = None
    device_name:str | None = None
    interfaces:str | None = None
    date:str | None = None
    device_description:str |None = None
    discovered_time:str | None = None
    device_type:str |None = None

class GetDevicesInterfaceRecordSchema(BaseModel):
    ip_address: str | None = None
    device_name: str | None =None
    function: str | None = None
    interface_status:str | None = None
    vendor:str | None = None
    interface_name: str | None = None
    interface_description: str | None =  None
    download_speed: float = 0
    upload_speed: float = 0
    date: str |  None =  None
    device_type: str | None = None
