from datetime import datetime

from app.schema.base_schema import BaseSchema, SummeryResponseSchema,validator
from typing import Optional, Union

class AddDiscoveryNetworkRequestSchema(BaseSchema):
    network_name: str
    subnet: str
    scan_status: str | None = None
    excluded_ip_range: str | None = None


class EditDiscoveryNetworkRequestSchema(BaseSchema):
    network_id: int
    network_name: str
    subnet: str
    scan_status: str | None = None
    excluded_ip_range: str | None = None


class GetDiscoveryNetworkResponseSchema(EditDiscoveryNetworkRequestSchema):
    no_of_devices: int | None = None
    creation_date: datetime
    modification_date: datetime


class DiscoveryFunctionCountResponseSchema(BaseSchema):
    devices: int
    firewall: int
    router: int
    switch: int
    other: int


class GetFunctionDiscoveryDataRequestSchema(BaseSchema):
    subnet: str
    function: str


class GetDiscoveryDataResponseSchema(BaseSchema):
    discovery_id: int
    ip_address: str
    subnet: str
    os_type: str | None = None
    make_model: str | None = None
    function: str | None = None
    vendor: str | None = None
    snmp_status: str | None = None
    snmp_version: str | None = None
    ssh_status: str | None = None

    creation_date: datetime
    modification_date: datetime


class AutoDiscoveryFunctionCountResponseSchema(BaseSchema):
    switches: int
    firewalls: int
    routers: int
    others: int

class Response200(BaseSchema):
    data: dict
    message: str

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]






class AddSnmpV1_V2Schema(BaseSchema):
    profile_name : str
    community : str
    description : str | None= None
    port:int | None = None

class AddSnmpV3Schema(BaseSchema):
    user_name:str
    encryption_protocol: str
    profile_name:str | None = None
    description: str | None = None
    port:int | None = None
    authentication_protocol:str |None = None
    authentication_password:str | None = None
    encryption_password:str |None = None


class SNMPCredentials(BaseSchema):
    category:str
    profile_name: str
    community: str
    description: str | None = None
    port: int | None = None
    username: str
    authorization_protocol: str | None = None
    authorization_password: str | None = None
    encryption_protocol: str
    encryption_password: str

    @validator('category')
    def check_profile_name(cls, v, values, **kwargs):
        if v is None or v =='string':
            raise ValueError('category is required')
        return v
    @validator('profile_name','community')
    def check_snmp_community(cls, v, values,field, **kwargs):
        if values.get('category') in ['v1/v2'] and v is None:
            raise ValueError(f'{field["alias"]} is required for v1/v2 category')
        return v

    @validator('username', 'encryption_protocol', 'encryption_password')
    def check_v3_required_fields(cls, v, values, field, **kwargs):
        category = values.get('category')
        if v is None:
            raise ValueError(f'{field.name} is required for v3 category')
        elif v=='string':
            raise ValueError(f'{field.name} cannot be a string for v3 category')
        return v

class GetSnmpV1V2Schema(BaseSchema):
    credential_id: int
    category:str |None = None
    profile_name:str | None = None
    description:str | None = None
    community:str | None = None
    port:str | None = None

class GetSnmpV3Schema(BaseSchema):
    credential_id:int | None = None
    category:str | None = None
    profile_name:str | None = None
    description:str | None = None
    community:str | None = None
    port:int | None = None
    user_name:str | None = None
    authentication_protocol:str | None = None
    authentication_password:str | None = None
    encryption_protocol:str | None = None
    encryption_password:str | None = None


class GetSnmpV2_V2_V2_login_Count(BaseSchema):
    snmp_v1_v2:int
    snmp_v3: int
    ssh_login:int

class GetSSHLoginSchema(BaseSchema):
    password_group_id:int
    password_group: str
    password_group_type:str
    username:str
    password:str

class RequestSubnetSchema(BaseSchema):
    subnet : str


class EditSnmpV2RequestSchema(AddSnmpV1_V2Schema):
    credentials_id:int


class EditSnmpV3RequestSchema(AddSnmpV3Schema):
    credentials_id:int





class DiscoveryDataSchema(BaseSchema):
    ip_address:str
    os_type:str | None = None
    subnet:str | None = None
    make_model:str | None = None
    vendor:str | None = None


class GetDiscoveryDataSchema(DiscoveryDataSchema):
    discovery_id:int