from datetime import datetime

from app.schema.base_schema import *


class MonitoringSpiralSchema(BaseSchema):
    fill: str
    name: str
    value: str


class SnapShotSchema(BaseSchema):
    name: str
    devices: int
    alarms: int


class MapNodeSchema(BaseSchema):
    id: str
    title: str
    label: str
    function: str
    image: str
    status: str


class ColorSchema(BaseSchema):
    color: str


class MapEdgeSchema(BaseSchema):
    id: str
    from_: str
    to: str
    color: ColorSchema


class MonitoringMapSchema(BaseSchema):
    nodes: list[MapNodeSchema]
    edges: list[MapEdgeSchema]


class MonitoringCardBaseSchema(BaseSchema):
    ip_address: str
    device_name: str
    function: str
    device_type: str
    status: str
    vendor: str | None
    date: datetime


class DeviceCardDataSchema(MonitoringCardBaseSchema):
    response: str
    uptime: str
    cpu: int
    memory: float
    packets: str
    interfaces: int
    device_description: str
    discovered_time: datetime


class InterfaceCardDataSchema(MonitoringCardBaseSchema):
    download_speed: float
    upload_speed: float
    interface_name: str
    interface_description: str


class TopInterfacesSchema(BaseSchema):
    ip_address: str
    device_name: str
    interface_name: str
    download_speed: float
    upload_speed: float


class MonitoringAlertSchema(BaseSchema):
    alarm_id: int
    ip_address: str
    description: str
    alert_type: str
    category: str
    alert_status: str
    mail_status: str
    date: datetime


class GetMonitoringDevicesCardsResponseSchema(BaseSchema):
    device: list[DeviceCardDataSchema]
    interfaces: list[InterfaceCardDataSchema]
    alerts: list[MonitoringAlertSchema]




class TopItemDashboardSchema(BaseSchema):
    ip_address: str
    device_name: str
    function: str


class CpuDashboardSchema(TopItemDashboardSchema):
    cpu: float


class MemoryDashboardSchema(TopItemDashboardSchema):
    memory: float


class InterfaceBandwidthGraphSchema(BaseSchema):
    name: str
    date: datetime
    download: str
    upload: str


class InterfaceBandwidthTableSchema(BaseSchema):
    bandwidth: str
    min: float
    max: float
    avg: float


class InterfaceBandwidthSchema(BaseSchema):
    all: list[InterfaceBandwidthGraphSchema]
    table: list[InterfaceBandwidthTableSchema]


class MonitoringDeviceSchema(BaseSchema):
    monitoring_device_id: int
    ip_address: str
    device_type: str
    device_name: str
    vendor: str | None
    function: str
    source: str | None
    credentials: str | None
    active: str | None
    status: str | None
    snmp_status: str | None
    profile_name:str | None
    ping_status: str | None
    # creation_date: datetime
    # modification_date: datetime
class UpdateMonitoringDeviceSchema(BaseSchema):
    monitoring_device_id: int
    monitoring_credentials_id: str | None



class AtomInMonitoringSchema(BaseSchema):
    ip_address: str
    device_name: str
    device_type: str
    vendor : str


class GetFunctionDataSchema(BaseSchema):
    function: str
    device_type: str | None


class AlertStatusSchema(BaseSchema):
    name : str
    value : int 


class SnmpCredentialsSchema(BaseSchema):
    profile_name: str
    description: str | None
    port: int


class SnmpV2CredentialsRequestSchema(SnmpCredentialsSchema):
    community: str


class SnmpV3CredentialsRequestSchema(SnmpCredentialsSchema):
    username: str
    authentication_password: str
    encryption_password: str
    authentication_protocol: str
    encryption_protocol: str





class AddMonitoringSnmpV3CredentialsRequestSchema(BaseSchema):
    username: str
    authorization_password: str
    encryption_password: str
    authorization_protocol: str
    encryption_protocol: str
    profile_name: str
    description: str | None
    port: int

class MonitoringSnmpV3CredentialsRequestSchema(BaseSchema):
    monitoring_credentials_id:int
    username: str
    authorization_password: str
    encryption_password: str
    authorization_protocol: str
    encryption_protocol: str
    profile_name: str
    description: str | None
    port: int


class SnmpV2CredentialsResponseSchema(SnmpV2CredentialsRequestSchema):
    monitoring_credentials_id: int


class SnmpV3CredentialsResponseSchema(SnmpV3CredentialsRequestSchema):
    monitoring_credentials_id: int

class Response200(BaseSchema):
    data: dict
    message: str

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class WMIMonitoringCredentialSchema(BaseSchema):
    user_name:str
    profile_name:str
    password:str

class GetWMIMonitoringCredentialSchema(BaseSchema):
    monitoring_credentials_id:int
    username:str
    profile_name:str
    password:str
    category:str


class MonitoringCredentialsResponseSchema(BaseSchema):
    monitoring_credentials_id:int
    category:str
    profile_name:str

class InterfaceBandScema(BaseSchema):
    ip_address:str
    interface_name:str


class AddAtomInMonitoringSchema(BaseSchema):
    atom_id:int
    monitoring_credentials_id:int


class EditSnmpV2Credentials(SnmpV2CredentialsResponseSchema):
    monitoring_credentials_id : int

class EditSnmpV3CredentialsResponseSchema(MonitoringSnmpV3CredentialsRequestSchema):
    monitoring_credentials_id:int

class MonitoringAlertsByIpAddress(BaseSchema):
    ip_address:str

class NewInterfaceCardResponse(BaseSchema):
    availability: int
    packets : int
    cpu: int 
    memory: int
    response_time : int


# class DeleteMonitoringSchema(BaseSchema):
#     ip_address:str