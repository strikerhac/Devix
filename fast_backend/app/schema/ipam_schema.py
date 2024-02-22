from datetime import datetime
from app.schema.base_schema import *
from typing import List ,Union



class Response200(BaseSchema):
    data: dict
    message: str

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class GetAtomInIpamSchema(BaseSchema):
    atom_id:int
    ip_address:str
    device_name:str | None = None
    function:str | None = None
    vendor:str | None = None

class AddAtomInIpamSchema(BaseSchema):
    atom_id:int

class AddSubnetManually(BaseSchema):
    subnet_address:str
    subnet_mask:str
    subnet_name:str | None = None
    subnet_location:str | None = None


class EditSubnetSchema(BaseSchema):
    subnet_id:int
    subnet_mask:str
    subnet_name:str | None = None
    subnet_location:str | None = None

class AddSubnetInSubnetSchema(BaseSchema):
    subnet:str


class GetIpBySubnetSchema(BaseSchema):
    subnet:str

class IpHistoryBySubnetSchema(BaseSchema):
    ip_id:int
    mac_address:str | None = None
    status:str | None = None
    vip:str
    asset_tag:str
    configuration_switch:str
    configuration_interface:str
    open_ports:str
    ip_dns:str
    dns_ip:str
    creation_date:datetime
    modification_date:datetime
    ip_address:str
    subnet:str

class DiscoveredSubnetSchema(BaseSchema):
    subnet_id:int
    subnet:str
    subnet_mask:str
    subnet_name:str
    location:str
    discovered_from:str
    subnet_usage:str
    subnet_size:str

class AddDnsSchema(BaseSchema):
    ip_address:str
    server_name:str
    user_name:str
    password:str

class GetallDnsServers(BaseSchema):
    dns_server_id : int
    server_name:str
    number_of_zones:str
    type:str
class getDnsZones(BaseSchema):
    dns_id:int
    zone_name:str
    zone_status:str
    zone_type:str
    lookup_type:str

class GetDnsRecoed(BaseSchema):
    dns_record_id:int
    server_name:str
    server_ip:str

class GetIpamDevicesSchema(BaseSchema):
    ipam_device_id:int
    interface:str
    interface_ip:str
    virtual_ip:str
    vlan:str
    vlan_number:str
    interface_status:str
    fetch_date:datetime
    interface_location:str
    discovered_from:str
    subnet:str
    subnet_mask:str
    subnet_name:str
    scan_date:datetime
    subnet_usage:str
    subnet_size:int


class F5Obj(BaseSchema):
    f5_id: int
    ip_address: str
    device_name: str
    vserver_name: str
    vip: str
    pool_name: str
    pool_member:str  # Change Optional type based on your requirement
    node: str         # Change Optional type based on your requirement
    service_port: int
    monitor_value: str
    monitor_status: str
    lb_method: str
    creation_date: str
    modification_date: datetime
    created_by: datetime
    modified_by: str

class GetAllFirewallVIP(BaseSchema):
    firewall_vip_id:int
    ip_address:str
    device_name:str
    internal_ip:str
    vip:str
    sport:str
    dport:str
    extintf:str
    creation_date:datetime
    modification_date:datetime

class GetAllSubnetSchema(BaseSchema):
    subent_id:int
    subnet:str
    subnet_mask:str
    subnet_name:str
    location:str
    discovered_from:str
    discovered:str
    scan_date:str
    subnet_usage:str
    subnet_size:str

class IPDetailScehma(BaseSchema):
    ip_id:int
    mac_address:str | None = None
    status:str | None = None
    vip:str
    asset_tag:str
    configuration_switch:str
    configuration_interface:str
    open_ports:str
    ip_dns:str
    dns_ip:str
    creation_date:datetime
    modification_date:datetime
    ip_address:str

class ScanSubnetSchema(BaseSchema):
    subnet_id: List[int]
    port_scan: bool
    dns_scan: bool

class ScanAllSubnetSchema(BaseSchema):
    port_scan:bool
    dns_scan:bool

class TestDnsSchema(BaseSchema):
    user_name:str
    password:str
    ip_address:str

class ScanDNSSchema(BaseSchema):
    ip_address:str

class DeleteSubnetScehma(BaseSchema):
    subnet_id:int

class IPhistorySchema(BaseSchema):
    ip_history_id:int
    ip_address:str
    mac_address:str
    asset_tag:str
    date:datetime


class EditDnsSchema(BaseSchema):
    dns_server_id:int
    ip_address:str
    server_name:str
    user_name:str
    password:str
class IpDetailBySubnetResponseSchema(BaseSchema):
    subnet_address:str

class IpHistoryResponseSchema(BaseSchema):
    ip_address:str



class PortsValue(BaseSchema):
    #ports: List[Union[str, None]]
    #counts: List[int]
    name : List[str]
    value : List[int]


class Ip_Address_counts(BaseSchema):
    total_ip : int
    used_ip : int 
    available_ip : int 


class SubnetIPUsage(BaseSchema):
    subnet_address : str
    subnet_usage : str


'''class ResponseDNSSummary(BaseSchema):
    Not_Resolved : int
    Resolved : int'''

class ResponseDNSSummary(BaseSchema):
    name : str
    value : int



class SubnetSummaryResponse(BaseSchema):
    #total_count : int
    name : str 
    value : int

class DnsZoneByServerID(BaseSchema):
    dns_server_id:int

class TypeSummaryResponse(BaseSchema):
    vender : str
    counts : int     

class IpAddressobjlist(BaseSchema):
        total_ip: int
        used_ip :int
        available_ip:int 