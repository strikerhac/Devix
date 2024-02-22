from app.models.ipam_models import *
from app.api.v1.ipam.utils import *
from app.api.v1.ipam.routes.device_routes import *
from app.api.v1.ipam.utils.ipam_utils import *
from app.models.common_models import *
from sqlalchemy import desc
import sys
from typing import List
import traceback
from app.models.ipam_models import *
from app.schema.ipam_schema import *
from app.schema.base_schema import *
# from app.schema.
from sqlalchemy import and_, distinct
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
from app.schema.ipam_schema import *
from app.core.config import configs
from app.models.atom_models import *
from app.utils.db_utils import *
import threading
from threading import Thread
import subprocess
from pywinos import WinOSClient
# from ping3 import ping, verbose_ping
import os
from subprocess import *
import re
import gzip
import json
from fastapi.responses import JSONResponse
import base64
import socket
import nmap
from netaddr import IPNetwork
import platform
from app.models.uam_models import *
from io import BytesIO
# from app.ipam_scripts.f5 import F5
# from app.ipam_scripts.fortigate_vip import FORTIGATEVIP
# from app.ipam_scripts.ipam import IPAM
# from app.ipam_scripts.ipam_physical_mapping import IPAMPM
from fastapi import FastAPI,APIRouter,Query
from starlette.responses import Response
from fastapi.responses import JSONResponse
router = APIRouter(
    prefix = '/ipam_device',
    tags = ['ipam_device']
)


@router.get('/test')
def test_route():
    try:
        return {"messgae":"This is testing routes"}
    except Exception as e:
        traceback.print_exc()

@router.get('/get_atom_in_ipam',
            responses = {
                200:{"model":list[GetAtomInIpamSchema]},
                400:{"model":str},
                500:{"model":str}
            },
            summary="Use this API in IPAM devices page to list down all the atom the atoms in add device from atom.This API is of get method",
            description="Use this API in IPAM devices page to list down all the atom the atoms in add device from atom.This API is of get method"
            )
def get_atom_in_ipam():
    try:
        atom_list = []
        atom_exist = configs.db.query(AtomTable).all()

        for atom in atom_exist:
            ipam_atom = configs.db.query(IpamDevicesFetchTable).filter_by(atom_id=atom.atom_id).first()
            if not ipam_atom:
                atom_obj = {
                    "atom_id": atom.atom_id,
                    "ip_address":atom.ip_address,
                    "device_name": atom.device_name,
                    "function": atom.function,
                    "vendor": atom.vendor,
                    "on_board_status":atom.onboard_status
                }
                atom_list.append(atom_obj)

        return JSONResponse(content=atom_list, status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Getting Atom In Ipam", status_code=500)


@router.post('/add_atom_in_ipam',responses={
    200:{"model":SummeryResponseSchema},
    400:{"model":str},
    500:{"model":str}
},
summary="Use this API in IPAM devices page to insert the atom in IPAM Devices page.This is of post API and insert the atom based on the atom_id",
description="Use this API in IPAM devices page to insert the atom in IPAM Devices page.This is of post API and insert the atom based on the atom_id"
)
async def add_atom_in_ipam(ipam_obj: list[int]):
    try:
        data = []
        success_lst = []
        error_list = []
        for atom_data in ipam_obj:
            atom_id = atom_data
            print("atom_id is:", atom_id, file=sys.stderr)
            atom_ip = configs.db.query(AtomTable).filter_by(atom_id=atom_id).first()
            ip_address = atom_ip.ip_address
            print("ip address is::::",ip_address,file=sys.stderr)
            atom_exists = configs.db.query(IpamDevicesFetchTable).filter_by(atom_id=atom_id).first()
            if atom_exists:
                return JSONResponse(status_code=400, content="Atom Already Exists")
            else:
                new_atom = IpamDevicesFetchTable(atom_id=atom_id)  # Create a new atom object
                print("new atom is ::::::::::::::",new_atom,file=sys.stderr)
                print("Atom added to the IPAM devices fetch table", file=sys.stderr)
                from app.api.v1.ipam.utils.ipam_utils import FetchIpamDevices
                response = FetchIpamDevices(atom_id)
                print("response of the puller is:::::::::::::::",response,file=sys.stderr)
            failed_ip = configs.db.query(FailedDevicesTable).filter_by(ip_address=ip_address).first()
            print("failed ip is::::::::::::::::::", failed_ip, file=sys.stderr)
            if failed_ip:
                error_list.append(f"{failed_ip.ip_address} : {failed_ip.failure_reason}")

            ipam_devices = configs.db.query(IpamDevicesFetchTable).filter_by(atom_id = atom_id).all()
            if ipam_devices:
                for device in ipam_devices:
                    devices_data = {}
                    devices_data['ip_address'] = atom_ip.ip_address
                    devices_data['device_name'] = atom_ip.device_name
                    devices_data['ipam_device_id'] = device.ipam_device_id
                    devices_data['interface_ip'] = device.interface_ip
                    devices_data['interface_description'] = device.interface_description
                    devices_data['virtual_ip'] = device.virtual_ip
                    devices_data['vlan'] = device.vlan
                    devices_data['vlan_number'] = device.vlan_number
                    devices_data['interface_status'] = device.interface_status
                    devices_data['fetch_date'] = device.fetch_date
                    ip_interfaces = configs.db.query(ip_interface_table).filter_by(ipam_device_id = device.ipam_device_id).all()
                    for ip in ip_interfaces:
                        devices_data['discovered_from'] = ip.discovered_from
                    subnet = configs.db.query(subnet_table).filter_by(ipam_device_id = device.ipam_device_id).all()
                    for row in subnet:
                        devices_data['subnet'] = row.subnet_address
                        devices_data['subnet_mask'] = row.subnet_mask
                        devices_data['location'] = row.location
                        subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id = row.subnet_id).all()
                        for usage in subnet_usage:
                            devices_data['subnet_usage'] = usage.subnet_usage
                            devices_data['subnet_size'] = usage.subnet_size
                    data.append(devices_data)
                    success_lst.append(f"{atom_id} : Inserted Successfully")
        print("data is::::::",data,file=sys.stderr)
        responses = {
            'data':data,
            "success_list":success_lst,
            "error_list":error_list,
            "success":len(success_lst),
            "erro":len(error_list)
        }
        return responses

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content="Error Occurred While Adding Atom in IPAM")


@router.get('/get_all_ipam_devices',
            responses={
                200: {"model": list[GetIpamDevicesSchema]},
                400: {"model": str},
                500: {"model": str}
            },
            summary = "Use This API to list down all the IPAM devices in a table",
            description="Use This API to list down all the IPAM devices in a table"
            )
def get_ipam_fetch_devices():
    try:
        devices_list = []
        ipam_devices = configs.db.query(IpamDevicesFetchTable).all()

        for devices in ipam_devices:
            print("device in ipma devicesi is::::::::::::",devices,file=sys.stderr)
            atom_exist = configs.db.query(AtomTable).filter_by(atom_id=devices.atom_id).first()
            interfaces = configs.db.query(ip_interface_table).filter_by(ipam_device_id=devices.ipam_device_id).first()
            subnet = configs.db.query(subnet_table).filter_by(ipam_device_id=devices.ipam_device_id).first()

            print("atom exsist is:",atom_exist,file=sys.stderr)
            print("insterface exsist is:::",file=sys.stderr)
            print("subnet is::::::",subnet,file=sys.stderr)
            subnet_address = subnet_mask = subnet_name = scan_date = None
            subnet_usage_value = subnet_size = None

            if subnet:
                subnet_address = subnet.subnet_address
                subnet_mask = subnet.subnet_mask
                subnet_name = subnet.subnet_name
                scan_date = subnet.scan_date
                print("subnet address:::::",subnet_address,file=sys.stderr)
                subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id=subnet.subnet_id).first()
                if subnet_usage:
                    subnet_usage_value = subnet_usage.subnet_usage
                    subnet_size = subnet_usage.subnet_size
                    print("subent usage iss::",subnet_usage,file=sys.stderr)

            devices_dict = {
                "ipam_device_id": devices.ipam_device_id,
                "ip_address": atom_exist.ip_address if atom_exist else None,
                "device_name": atom_exist.device_name if atom_exist else None,
                "subnet_address": subnet_address,
                "subnet_mask": subnet_mask,
                "subnet_name": subnet_name,
                "interface": devices.interface,
                "interface_ip": devices.interface_ip,
                "interface_description": devices.interface_description,
                "virtual_ip": devices.virtual_ip,
                "vlan": devices.vlan,
                "vlan_number": devices.vlan_number,
                "interface_status": devices.interface_status,
                "fetch_date": devices.fetch_date,
                "interface_location": interfaces.interface_location if interfaces else None,
                "discovered_from": interfaces.discovered_from if interfaces else None,
                "interface_status": interfaces.interface_status if interfaces else None,
                "scan_date": scan_date,
                "subnet_usage": subnet_usage_value,
                "subnet_size": subnet_size
            }
            print("device dict is::::::::::")
            devices_list.append(devices_dict)
        print("devices list is:::::::::::::::::",devices_list,file=sys.stderr)
        return devices_list

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(content={"error": "Error Occurred While Getting IPAM devices", "details": str(e)}, status_code=500)


@router.post('/add_subnet',responses={
    200:{"model":Response200},
    400:{"model":str},
    500:{"model":str}
},
summary="Use this API in subnet page to add the subnet manually or static subnet this api is of post method",
             description="Use this API in subnet page to add the subnet manually or static subnet this api is of post method"
)
def add_subnet(subnetObj:AddSubnetManually):
    try:
        subnet_data_dict = {}
        subnet_list =[]
        subnet_obj = dict(subnetObj)
        print("subnet obj is :::::",file=sys.stderr)
        subnet_exsist = configs.db.query(subnet_table).filter_by(subnet_address = subnet_obj['subnet_address']).first()
        if subnet_exsist:
            return JSONResponse(content=f"{subnet_obj['subnet_address']} : Already Exist",status_code=400)
        else:
            subnet_tab = subnet_table()
            subnet_tab.subnet_address = subnet_obj['subnet_address']
            subnet_tab.subnet_mask = subnet_obj['subnet_mask']
            subnet_tab.subnet_name = subnet_obj['subnet_name']
            subnet_tab.location = subnet_obj['subnet_location']
            subnet_tab.discovered = 'Not Discovered'
            InsertDBData(subnet_tab)
            subnet_dict = {
                "subnet_id":subnet_tab.subnet_id,
                "subnet_mask":subnet_tab.subnet_mask,
                "subnet_address": subnet_tab.subnet_address,
                "subnet_name":subnet_tab.subnet_name,
                "subnet_location":subnet_tab.location,
                "discovered":subnet_tab.discovered
            }
            subnet_data_dict['data'] = subnet_dict
            subnet_data_dict['message'] = f"{subnet_tab.subnet_address} : Inserted Successfully"
            subnet_list.append(subnet_dict)
        return JSONResponse(content=subnet_data_dict,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While adding the subnett",status_code=500)

@router.post('/addsubnetinsubnet',
             responses={
                 200:{"model":str},
                 400:{"model":str},
                500:{"model":str}
             }
             )
def AddSusbnetInSunet(data:list[AddSubnetInSubnetSchema]):
    try:
        for subnet in data:
            subnet_address = subnet.subnet

            query = (
                configs.db.query(AtomTable.device_name)
                .join(IpamDevicesFetchTable, AtomTable.atom_id == IpamDevicesFetchTable.atom_id)
                .filter(IpamDevicesFetchTable.ipam_device_id == subnet_table.ipam_device_id)
                .distinct()
                .all()
            )

            print("query is:::::::::::",query,file=sys.stderr)
            if query:
                for row in query:
                    print("row is::::::",row,file=sys.stderr)
                    subnet_data = (
                        configs.db.query(subnet_table)
                        .filter_by(discovered_from=row.device_name)
                        .first()
                    )

                    if subnet_data:
                        print("subnet adta is:::::",subnet_data,file=sys.stderr)
                        subnet_usage = (
                            configs.db.query(subnet_usage_table)
                            .filter_by(subnet_id=subnet_data.subnet_id)
                            .first()
                        )

                        if subnet_usage:
                            print("subnet usage is::::",subnet_usage,file=sys.stderr)
                            subnet_usage.subnet_size = subnet_usage.subnet_size
                            subnet_usage.subnet_usage = subnet_usage.subnet_usage

                        subnet_data.discovered_from = row.device_name
                        subnet_data.status = 'Waiting'
                        subnet_data.scan_date = datetime.now()

                        existing_subnet = (
                            configs.db.query(subnet_table)
                            .filter_by(subnet_address=subnet_address)
                            .first()
                        )

                        if existing_subnet:
                            print("exisiting subnet is:::::::::",existing_subnet,file=sys.stderr)
                            existing_subnet.subnet_mask = subnet_data.subnet_mask
                            existing_subnet.subnet_name = subnet_data.subnet_name
                            existing_subnet.location = subnet_data.location
                            existing_subnet.discovered_from = subnet_data.discovered_from
                            existing_subnet.status = 'Not Scanned'

                            if existing_subnet.discovered == 'Discovered':
                                existing_subnet.discovered = 'Not Discovered'
                                configs.db.commit()
                                response = True
                            else:
                                configs.db.add(subnet_data)
                                configs.db.commit()
                                print(f'{subnet_data.subnet_address} Updated Successfully',file=sys.stderr)
                                response = True

                            try:
                                ips = GetIps(subnet)
                                print("ips are:::::::::::::::::",ips,file=sys.stderr)
                                for ip in ips:
                                    print("ips in ip is",ip,file=sys.stderr)
                                    subnet_id = subnet_data.subnet_id
                                    ip_exists = (
                                        configs.db.query(IpTable)
                                        .filter_by(ip_address=ip, subnet_id=subnet_id)
                                        .first()
                                    )
                                    print("ip exsist is::::",ip_exists,file=sys.stderr)
                                    if ip_exists:
                                        ip_exists.mac_address = ''
                                        ip_exists.configuration_interface = ''
                                        ip_exists.configuration_switch = ''
                                        ip_exists.status = ''
                                        ip_exists.ip_to_dns = ''
                                        ip_exists.dns_to_ip = ''
                                        ip_exists.status_history = ''
                                        ip_exists.vip = ''
                                    else:
                                        subnet_id = subnet_data.subnet_id
                                        new_ip = IpTable(ip_address=ip, subnet_id=subnet_id)
                                        configs.db.add(new_ip)

                                configs.db.commit()
                                return {"Response": "Subnet added successfully"}
                            except Exception as e:
                                traceback.print_exc()
                                return {"Response": "Error occurred while processing IP addresses"}
            else:
                return {'Response': "No subnet found"}

    except Exception as e:
        traceback.print_exc()
        return {"Response": "Error Occurred while adding subnet in subnet"}

@router.post('/get_ip_detail_by_subnet',
            responses = {
                200:{"model":list[IpHistoryBySubnetSchema]},
                400:{"model":str},
                500:{"model":str}
            },
            summary = "Use this API in the subnet table while clicking on the subnet get the detail of its ip",
            description="Use this API in the subnet table while clicking on the subnet get the detail of its ip"
            )
async def get_ip_details_by_stubnet(subnet_address:IpDetailBySubnetResponseSchema):
    try:
        ip_list = []
        data = subnet_address
        print("data is::::", data, file=sys.stderr)

        # Fetch subnet detail from the database
        subnet_detail = (
            configs.db.query(subnet_table)
            .filter_by(subnet_address=data.subnet_address)
            .first()
        )

        if subnet_detail:
            # Fetch IP details associated with the found subnet
            print("subnet detai;ls",subnet_detail,file=sys.stderr)
            ip_detail = (
                configs.db.query(IpTable)
                .filter_by(subnet_id=subnet_detail.subnet_id)
                .all()
            )
            print("ip details is",ip_detail,file=sys.stderr)
            for ip in ip_detail:
                print("ip is::",ip,file=sys.stderr)
                print("ip is::",ip,file=sys.stderr)
                ip_dict = {
                    "ip_id": ip.ip_address,
                    "mac_address": ip.mac_address,
                    "status": ip.status,
                    "vip": ip.vip,
                    "asset_tag":ip.asset_tag,
                    "configuration_switch":ip.configuration_switch,
                    "configuration_interface":ip.configuration_interface,
                    "open_ports":ip.open_ports,
                    "ip_dns":ip.ip_dns,
                    "dns_ip":ip.dns_ip,
                    "creation_date":ip.creation_date,
                    "modification_date":ip.modification_date,
                    "ip_address":ip.ip_address,
                    "subnet_address":subnet_detail.subnet_address
                }
                ip_list.append(ip_dict)

            return ip_list
        else:
            return JSONResponse(content="Subnet detail not found", status_code=400)

    except Exception as e:
        traceback.print_exc()
        print(f"Error occurred while getting subnet details by subnet: {e}")
        return JSONResponse(
            content="Error Occurred While getting subnet details by subnet",
            status_code=500
        )

@router.get("/get_all_discovered_subnet",
            responses = {
                200:{"model":list[DiscoveredSubnetSchema]},
                400:{"model":str},
                500:{"model":str}
            },
            summary="Use this API to list down all the discovered subnet in subnet page in discovered subnet table",
            description="Use this API to list down all the discovered subnet in subnet page in discovered subnet table"
            )
def get_all_discovered_subnet():
    try:
        subnet_lst = []
        subnets = configs.db.query(subnet_table).filter_by(discovered="Discovered").all()
        for subnet in subnets:
            subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id = subnet.subnet_id).first()
            subnet_dict = {
                "subnet_id":subnet.subnet_id,
                "subnet_address":subnet.subnet_address,
                "subnet_mask":subnet.subnet_mask,
                "subnet_name":subnet.subnet_name,
                "location":subnet.location,
                "discovered_from":subnet.discovered_from,
                "subnet_usage":subnet_usage.subnet_usage,
                "subnet_size":subnet_usage.subnet_size,
            }
            subnet_lst.append(subnet_dict)
        return subnet_lst
    except Exception as e:
        traceback.print_exc()

@router.post('/add_dns',
             responses={
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="Use this API to add the DNS in the DNs page.This API is of post method",
             description="Use this API to add the DNS in the DNs page.This API is of post method"
             )
def AddDNS(data: AddDnsSchema):
    try:
        data_dns = {}
        response = False
        dns_data_dict = {}
        print("data is::::",data,file=sys.stderr)
        dns_data = dict(data)
        if dns_data['ip_address'] and dns_data['user_name'] and dns_data['password']:
            try:
                tool = WinOSClient(host=dns_data['ip_address'], username=dns_data['user_name'],
                                   password=dns_data['password'])
                print("tootl is:::::::::::::::::::::::::::::::",tool,file=sys.stderr)
                response = tool.run_ps('Get-DnsServerZone | ConvertTo-Json')
                print("repsonse of the add dns test is:::::::::::::::::",response,file=sys.stderr)
                response = True
            except Exception as e:
                traceback.print_exc()
        else:
            response = False
        if response == True:

            add_dns = DnsServerTable()
            print("ip_address found in dns ip address True updating executing>>", file=sys.stderr)
            dns_query1 = configs.db.query(DnsServerTable).filter_by(ip_address=dns_data['ip_address']).first()
            if dns_query1:
                print("dns query is >>>>>>>>>>>", dns_query1, file=sys.stderr)
                # updating the add dns table
                dns_query1.ip_address = dns_data['ip_address']
                dns_query1.user_name = dns_data['user_name']
                dns_query1.password = dns_data['password']
                dns_query1.server_name = dns_data['server_name']
                dns_query1.number_of_zones = 0
                dns_query1.type = ''
                UpdateDBData(add_dns)
                dns_data_dict['ip_address'] = dns_query1.ip_address
                dns_data_dict['user_name'] = dns_query1.user_name
                dns_data_dict['password'] = dns_query1.password
                dns_data_dict['server_name'] = dns_query1.server_name
                dns_data_dict['number_of_zones'] = dns_query1.number_of_zones
                dns_data_dict['type'] = dns_query1.type
                dns_data_dict['dns_server_id'] = dns_query1.dns_server_id
                print("DNS Table Updated >>>>>>>>>>", file=sys.stderr)
                data_dns['data'] = dns_data_dict
                data_dns['message'] = f"{dns_data['ip_address']} : DNS Updated Successfully"
            else:
                add_dns.ip_address = dns_data['ip_address']
                add_dns.username = dns_data['user_name']
                add_dns.password = dns_data['password']
                add_dns.server_name = dns_data['server_name']
                InsertDBData(add_dns)
                dns_data_dict['ip_address'] = add_dns.ip_address
                dns_data_dict['user_name'] = add_dns.username
                dns_data_dict['password'] = add_dns.password
                dns_data_dict['server_name'] = add_dns.server_name
                dns_data_dict['number_of_zones'] = add_dns.number_of_zones
                dns_data_dict['type'] = add_dns.type
                dns_data_dict['dns_server_id'] = add_dns.dns_server_id
                print("Inserted Into ADD DNS TABLE>", file=sys.stderr)
                data_dns['data'] = dns_data_dict
                # data_dns['message'] = f"{ip_address} DNS Inserted Successfully"
                data_dns['message'] = f"{dns_data['ip_address']} : DNS Inserted Successfully"
            return data_dns
        else:
            return JSONResponse(content="DNS Server Is Not Authenticated",status_code=400)

    except Exception as e:
        traceback.print_exc()
        return {"Reponse": "Error Occured while Adding DNS"}

@router.get('/get_dns_servers',
            responses={
                200:{"model":list[GetallDnsServers]},
                500:{"model":str}
            },
            summary="Use this API to list down all the dns server in the dns server page",
            description="Use this API to list down all the dns server in the dns server page"
            )
def GetAllDnsServers():
    if True:
        try:
            objList = []
            dnsServersObjs = configs.db.query(DnsServerTable).all()
            for dnsServerObj in dnsServersObjs:
                objDict = {}
                objDict['dns_server_id'] = dnsServerObj.dns_server_id
                objDict['ip_address'] = dnsServerObj.ip_address
                objDict['server_name'] = dnsServerObj.server_name
                objDict['number_of_zones'] = dnsServerObj.number_of_zones
                objDict['user_name'] = dnsServerObj.user_name,
                objDict['password'] = dnsServerObj.password,
                objDict['type'] = dnsServerObj.type
                objList.append(objDict)
            print(objList, file=sys.stderr)
            # return jsonify(objList),200
            return objList

        except Exception as e:
            print(str(e), file=sys.stderr)
            traceback.print_exc()
            return str(e), 500
    else:
        print("Authentication Failed", file=sys.stderr)
        return JSONResponse(content="Error Occured while Getting dns servers",status_code=500)


@router.get('/get_dns_zones',responses={
    200:{"model":list[getDnsZones]},
    500:{"model":str}
},
summary="Use this api to list down all the dns zones in the table.this api is of get method",
description="Use this api to list down all the dns zones in the table.this api is of get method"
)
def GetAllDnsZones():
    if True:
        try:
            objList = []
            dnsZonesObjs = configs.db.query(DnsZonesTable)
            for dnsZoneObj in dnsZonesObjs:
                dns_server_exsist = configs.db.query(DnsServerTable).filter_by(dns_server_id = dnsZoneObj.dns_server_id).first()
                objDict = {}
                objDict['dns_id'] = dnsZoneObj.dns_zone_id
                objDict['zone_name'] = dnsZoneObj.zone_name
                objDict['zone_status'] = dnsZoneObj.zone_status
                objDict['zone_type'] = dnsZoneObj.zone_type
                objDict['lookup_type'] = dnsZoneObj.lookup_type
                objDict['server_type']= dns_server_exsist.server_name
                objDict['ip_address'] = dns_server_exsist.ip_address
                objList.append(objDict)
            print(objList,file=sys.stderr)
            return objList
        except Exception as e:
            print(str(e),file=sys.stderr)
            traceback.print_exc()
            return str(e),500
    else:
        print("Authentication Failed", file=sys.stderr)
        return ({'message': 'Authentication Failed'}), 401

@router.get('/get_dns_records',responses={
    200:{"model":list[GetDnsRecoed]},
    500:{"model":str}
},
summary="Use this API to get all the dns records in the table",
description="Use this API to get all the dns records in the table"
)
def GetAllDnsServersRecord():
    if True:
        try:
            objList = []
            dnsServersRecordObjs = configs.db.query(DnsRecordTable).all()
            for dnsServersRecordObj in dnsServersRecordObjs:
                dns_zone_exsist = configs.db.query(DnsZonesTable).filter_by(dns_zone_id = dnsServersRecordObj.dns_zone_id).first()
                dns_server_exsist = configs.db.query(DnsServerTable).filter_by(dns_Server_id = dns_zone_exsist.dns_server_id).first()
                objDict = {}
                objDict['dns_record_id'] = dnsServersRecordObj.dns_id
                objDict['server_name'] = dnsServersRecordObj.server_name
                objDict['server_ip'] = dnsServersRecordObj.server_ip
                objDict['zone_name'] = dns_zone_exsist.zone_name
                objDict['dns_name'] = dns_server_exsist.server_name
                objDict['dns_type'] = dns_server_exsist.type

                objList.append(objDict)
            print(objList,file=sys.stderr)
            return objList
        except Exception as e:
            print(str(e),file=sys.stderr)
            traceback.print_exc()
            return str(e),500
    else:
        print("Authentication Failed", file=sys.stderr)
        return ({'message': 'Authentication Failed'}), 401

@router.get('/get_all_f5',
            responses={
                200:{'model':list[F5Obj]},
                400:{"model":str},
                500:{"model":str}
            })
def get_all_f5():
    try:
        f5ObjList = []
        f5Objs = configs.db.execute('SELECT * FROM f5 WHERE creation_date = (SELECT max(creation_date) FROM f5)')

        for f5Obj in f5Objs:
            f5DataDict = {
                "f5_id":f5Obj.f5_id,
                "ip_address":f5Obj.ip_address,
                "device_name":f5Obj.device_name,
                "vserver_name":f5Obj.vserver_name,
                "vip":f5Obj.vip,
                "pool_name":f5Obj.pool_name,
                "pool_member":f5Obj.pool_member,
                "node":f5Obj.node,
                "service_port":f5Obj.service_port,
                "monitor_value":f5Obj.monitor_value,
                "monitor_status":f5Obj.monitor_status,
                "lb_method":f5Obj.lb_method,
                "creation_date":f5Obj.creation_date,
                "modification_date":f5Obj.modification_date,
                "created_by":f5Obj.created_by,
                "modified_by":f5Obj.modified_by
            }
            f5ObjList.append(f5DataDict)

        content = json.dumps(f5ObjList).encode('utf-8')
        compressed_content = gzip.compress(content)

        # Use BytesIO to wrap the compressed content
        compressed_stream = BytesIO(compressed_content)

        # Extract bytes from BytesIO object using getvalue()
        compressed_bytes = compressed_stream.getvalue()

        # Create FastAPI Response with gzip compression and appropriate headers
        response = Response(
            content=compressed_bytes,
            media_type="application/json",
            headers={
                "Content-Encoding": "gzip",
                "Content-Length": str(len(compressed_bytes)),
            },
        )
        return response
    except Exception as e:
        traceback.print_exc()


@router.get('/get_all_firewall_vip',
            responses = {
                200:{"model":list[GetAllFirewallVIP]},
                500:{"model":str}
            },
            summary="Use this aspi in the VIP to list down all the firewall vip",
            description="Use this aspi in the VIP to list down all the firewall vip"
            )
def get_all_firewall_vip():
    try:
        firewall_lst = []
        firewall = configs.db.query(FIREWALL_VIP).all()
        for row in firewall:
            firewall_dict ={
                "firewall_vip_id":row.firewall_vip_id,
                "ip_address":row.ip_address,
                "device_name":row.device_name,
                "internal_ip":row.internal_ip,
                "vip":row.vip,
                "sport":row.sport,
                "dport":row.dport,
                "extintf":row.extintf,
                "creation_date":row.creation_date,
                "modification_date":row.modification_date
            }
            firewall_lst.append(firewall_dict)
        content = json.dumps(firewall_lst).encode('utf-8')
        compressed_content = gzip.compress(content)

        # Use BytesIO to wrap the compressed content
        compressed_stream = BytesIO(compressed_content)

        # Extract bytes from BytesIO object using getvalue()
        compressed_bytes = compressed_stream.getvalue()

        # Create FastAPI Response with gzip compression and appropriate headers
        response = Response(
            content=compressed_bytes,
            media_type="application/json",
            headers={
                "Content-Encoding": "gzip",
                "Content-Length": str(len(compressed_bytes)),
            },
        )
        return response
    except Exception as e:
        traceback.print_exc()
        return (JSONResponse
                (content="Error occured while getting all firewall vip",status_code=500))

@router.get('/get_all_subnet',
            responses={
                200:{"model":list[GetAllSubnetSchema]},
                500:{"model":str}
            },
            summary="Use this API to list down all the subnet in subnet details",
            description="Use this API to list down all the subnet in subnet details",
            )
def get_all_subnet():
    try:
        subnet_list = []
        subnet = configs.db.query(subnet_table).all()
        for row in subnet:
            subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id = row.subnet_id).first()
            subnet_dict = {
                "subnet_id":row.subnet_id,
                "subnet_address":row.subnet_address,
                "subnet_mask":row.subnet_mask,
                "subnet_name":row.subnet_name,
                "location":row.location,
                "discovered_from":row.discovered_from,
                "discovered":row.discovered,
                "scan_date":row.scan_date,
                "subnet_usage":subnet_usage.subnet_usage if subnet_usage else None,
                "subnet_size":subnet_usage.subnet_size if subnet_usage else None
            }
            subnet_list.append(subnet_dict)
        return subnet_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While getting subnet",status_code=500)

@router.get('/get_all_ip_details',
            responses={
                200:{"model":list[IPDetailScehma]},
                500:{"model":str}
            },
            summary= "use this ip to list down all the ip details",
            description = "use thi api to list down all the ip details in ip details"
            )
async def get_all_details():
    try:
        ip_list = []
        ip_detail = configs.db.query(IpTable).all()
        for ip in ip_detail:
            subnet_exsist = configs.db.query(subnet_table).filter_by(subnet_id = ip.subnet_id).first()
            if ip.ip_address is not None:
                print("ip is::", ip, file=sys.stderr)
                print("ip is::", ip, file=sys.stderr)
                subnet_address = None
                if subnet_exsist and subnet_exsist.subnet_address is not None :
                    subnet_address = subnet_exsist.subnet_address
                ip_dict = {
                    "ip_id": ip.ip_id,
                    "mac_address": ip.mac_address,
                    "status": ip.status,
                    "vip": ip.vip,
                    "asset_tag": ip.asset_tag,
                    "configuration_switch": ip.configuration_switch,
                    "configuration_interface": ip.configuration_interface,
                    "open_ports": ip.open_ports,
                    "ip_dns": ip.ip_dns,
                    "dns_ip": ip.dns_ip,
                    "creation_date": ip.creation_date,
                    "modification_date": ip.modification_date,
                    "ip_address": ip.ip_address,
                    "subnet_address":subnet_address
                }
                ip_list.append(ip_dict)
        return ip_list
    except Exception as e:
        traceback.print_exc()

@router.post('/scan_subnet',
             responses = {
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str},
             },
             summary="Use this API to in the subnet subnet table to scan the subnet this API will scan a subnet based on the subent in the body.This API is of post method",
             description = 'Use this API to in the subnet subnet table to scan the subnet this API will scan a subnet based on the subent in the body.This API is of post method'
             )
def scan_subnets(subnets: ScanSubnetSchema):
    try:
        print("subnet data is:::",subnets,file=sys.stderr)
        print("type os subnets is",type(subnets),file=sys.stderr)
        data = {}
        subnet_ids = subnets.subnet_id
        port_scan = subnets.port_scan
        dns_scan = subnets.dns_scan
        for subnet_id in subnet_ids:
            print("Processing subnet:", subnet_id, file=sys.stderr)
            options = []
            subnet_data = configs.db.query(subnet_table).filter_by(subnet_id=subnet_id).first()
            if port_scan:
                options.append('Port Scan')

            if dns_scan:
                options.append('DNS Scan')

            if subnet_data:
                print("subnet data is:::::",subnet_data,file=sys.stderr)
                subnet_data_dict = {
                    "subnet_id": subnet_data.subnet_id,
                    "subnet_address": subnet_data.subnet_address,
                    "subnet_mask": subnet_data.subnet_mask,
                }
                print("subnet data dict is::::::::::::",subnet_data_dict,file=sys.stderr)
                data = {
                    "data": subnet_data_dict,
                    "message": f"{subnet_data.subnet_address} : Scanned Successfully"
                }

                # Update subnet status
                subnet_data.status = 'Waiting'
                UpdateDBData(subnet_data)
                print("subnet data is updated and added to waiting list:::",file=sys.stderr)

                # Additional updates for IP data
                ip_data = configs.db.query(IpTable).filter_by(subnet_id=subnet_data.subnet_id).first()
                if ip_data:
                    ip_data.mac_address = ''
                    ip_data.configuration_switch = ''
                    ip_data.configuration_interface = ''
                    ip_data.status = ''
                    ip_data.ip_dns = ''
                    ip_data.dns_ip = ''
                    ip_data.vip = ''
                    UpdateDBData(ip_data)

            Thread(target=MultiPurpose, args=(options,)).start()
            print("Threading is being executed", file=sys.stderr)

        return data

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": "Error Occurred While Scanning the subnets", "details": str(e)}, status_code=500)

@router.post('/scan_all_subnets',
             responses = {
                 200:{"model":SummeryResponseSchema},
                 400:{"model":str},
                 500:{"model":str},
             },
             summary="Use this API in the subnet page on a scan subnet button to scan all the option this API accepts the dns_scan or port_scan in  a boolean.This API is of post method",
             description = 'Use this API in the subnet page on a scan subnet button to scan all the option this API accepts the dns_scan or port_scan in  a boolean.This API is of post method'
             )
async def scan_all_subnets(subnet: ScanAllSubnetSchema):
    try:
        data_dict = {}
        success_list = []
        error_list = []

        options = []
        data = dict(subnet)
        if data['port_scan'] is True:
            options.append('Port Scan')

        if data['dns_scan'] is True:
            options.append('DNS Scan')

        # If you want to append both 'Port Scan' and 'DNS Scan' when both are True
        if data['port_scan'] and data['dns_scan']:
            options.append('Port Scan')
            options.append('DNS Scan')

        print("data in scan subnet is:::::::", data, file=sys.stderr)
        option_dict = {"options": options}

        subnet_data = configs.db.query(subnet_table).all()
        for obj in subnet_data:
            try:
                if obj:
                    obj.status = 'Waiting'
                    # Update other attributes accordingly
                    configs.db.merge(obj)
                    configs.db.commit()  # Commit changes after merging
                    ip_data = configs.db.query(IpTable).filter_by(subnet_id=obj.subnet_id).first()
                    if ip_data:
                        ip_data.mac_address = ''
                        ip_data.configuration_switch = ''
                        ip_data.configuration_interface = ''
                        ip_data.status = ''
                        ip_data.ip_dns = ''
                        ip_data.dns_ip = ''
                        ip_data.vip = ''
                    configs.db.merge(ip_data)
                    configs.db.commit()  # Commit changes after merging
                print("DB updated::::::::::", file=sys.stderr)
                subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id = obj.subnet_id).first()
                subnet_data_dict = {
                    "subnet_id":obj.subnet_id,
                    "subnet_address":obj.subnet_address,
                    "subnet_mask":obj.subnet_mask,
                    "subnet_usage":subnet_usage.subnet_usage,
                    "subnet_size":subnet_usage.subnet_size
                }
                data_dict['data'] = subnet_data_dict
                success_list.append(f"{obj.subnet_address} : Scanned Successfully")
            except Exception as e:
                configs.db.rollback()  # Rollback changes if an exception occurs
                traceback.print_exc()


        stat = Thread(target=MultiPurpose, args=(option_dict.get('options'),)).start()
        print("threading is being executed::",stat,file=sys.stderr)
        if stat == "success":
            responses = {
                "data":data_dict,
                "success_list":success_list,
                "error_list":error_list,
                "success":len(success_list),
                "errror":len(error_list)
            }
        else:
            responses = {
                "data": [],
                "success_list": [],
                "error_list": ["Bulk Scanning Failed Due To Exception"],
                "success": 0,
                "error": 1
            }
        return responses
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Scanning the subnets", status_code=500)


@router.post('/test_dns',
             responses = {
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="Use this API in the DNS Serevr page in add dns fom to test the dns before adding the table",
             description = "Use this API in the DNS Serevr page in add dns fom to test the dns before adding the table"
             )
def test_dns(dns:TestDnsSchema):
    try:
        data = {}
        dns_data = dict(dns)
        print("dns data is:::::::",dns_data,file=sys.stderr)
        if dns_data['ip_address'] and dns_data['user_name'] and dns_data['password']:
            try:
                tool = WinOSClient(host=dns_data['ip_address'], username=dns_data['user_name'],
                                   password=dns_data['password'])

                response = tool.run_ps('Get-DnsServerZone | ConvertTo-Json')
                data = {"ip_address":dns_data['ip_address'],
                     "user_name":dns_data['user_nsame'],
                        "password":dns_data['password']
                     }

                response_dict = {
                    "data":data,
                    "message":f"{dns_data['ip_address']} : Authenticated"
                }
                return JSONResponse(content=response_dict,status_code=200)
            except Exception as e:
                traceback.print_exc()
                return JSONResponse(content="Authentication Failed",status_code=500)
    except Exception as e:
        traceback.print_exc()


@router.post('/scan_dns',responses = {
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="Use this API in the dns server table to scan a DNS based on the IP address",
             description="Use this API in the dns server table to scan a DNS based on the IP address"
             )
def scan_dns_by_ip(ip_address:ScanDNSSchema):
    try:
        dns_server = configs.db.query(DnsServerTable).filter_by(ip_address=ip_address).first()
        if dns_server:
            dns_server_id = dns_server.dns_server_id
            dns_zones = configs.db.query(DnsZonesTable).filter_by(dns_server_id=dns_server_id).all()
            for dns_zone in dns_zones:
                dns_records = configs.db.query(DnsRecordTable).filter_by(dns_zone_id=dns_zone.dns_zone_id).all()
                for dns_record in dns_records:
                    configs.db.delete(dns_record)
                configs.db.delete(dns_zone)
            configs.db.commit()

        status = scan_dns(ip_address)
        print("status for scan dns is:::::::::::::",status,file=sys.stderr)
        return status
    except Exception as e:
        traceback.print_exc()



@router.post('/add_subnets', responses={
    200: {"model": SummeryResponseSchema},
    400: {"model": str},
    500: {"model": str}
},
summary="Use this API in the subnet page to add the subent from the execel",
description="Use this API in the subnet page to add the subent from the execel"
)
def add_subnets(subnetObj: list[AddSubnetManually]):
    try:
        print("subnet obj is::::::::",subnetObj,file=sys.stderr)
        success_list = []
        error_list = []
        subnet_data_dict = {"data": []}  # Initialize subnet_data_dict as a list

        for obj in subnetObj:
            try:
                subnet_existing = configs.db.query(subnet_table).filter_by(subnet_address=obj.subnet_address).first()

                if subnet_existing:
                    # Update existing subnet details
                    subnet_existing.subnet_address = obj.subnet_address
                    subnet_existing.subnet_mask = obj.subnet_mask
                    subnet_existing.subnet_name = obj.subnet_name
                    subnet_existing.location = obj.subnet_location
                    subnet_existing.discovered = 'Not Discovered'
                    subnet_existing.subnet_state = 'Not Discovered'
                    UpdateDBData(subnet_existing)
                    configs.db.commit()

                    subnet_dict = {
                        "subnet_id": subnet_existing.subnet_id,
                        "subnet_mask": subnet_existing.subnet_mask,
                        "subnet_address": subnet_existing.subnet_address,
                        "subnet_name": subnet_existing.subnet_name,
                        "location": subnet_existing.location,
                        "discovered": subnet_existing.discovered
                    }
                    success_list.append(f"{subnet_existing.subnet_address} : Updated Successfully")
                else:
                    subnet_tab = subnet_table()
                    subnet_tab.subnet_address = obj.subnet_address
                    subnet_tab.subnet_mask = obj.subnet_mask
                    subnet_tab.subnet_name = obj.subnet_name
                    subnet_tab.location = obj.subnet_location
                    subnet_tab.discovered = 'Not Discovered'
                    subnet_tab.subnet_state = 'Not Discovered'
                    InsertDBData(subnet_tab)
                    subnet_dict = {
                        "subnet_id": subnet_tab.subnet_id,
                        "subnet_mask": subnet_tab.subnet_mask,
                        "subnet_address": subnet_tab.subnet_address,
                        "subnet_name": subnet_tab.subnet_name,
                        "location": subnet_tab.location,
                        "discovered": subnet_tab.discovered
                    }
                    success_list.append(f"{subnet_tab.subnet_address} : Inserted Successfully")

                subnet_data_dict["data"].append(subnet_dict)  # Append subnet_dict to subnet_data_dict

            except Exception as e:
                # If an error occurs during processing, append the error message to error_list
                error_list.append(f"Error occurred: {str(e)}")

        responses = {
            "data": subnet_data_dict["data"],  # Return the list of subnet data
            "success_list": success_list,
            "error_list": error_list,
            "success": len(success_list),
            "error": len(error_list)
        }
        return JSONResponse(content=responses, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While adding the subnet", status_code=500)


@router.post('/edit_subnet',responses={
    200:{"model":Response200},
    400:{"model":str},
    500:{"model":str}
},
summary="Use this API in the subent page in a subent table to edit a subnet",
             description="Use this API in the subent page in a subent table to edit a subnet"
)
def add_subnet(subnetObj:EditSubnetSchema):
    try:
        subnet_data_dict = {}
        subnet_list =[]
        subnet_obj = dict(subnetObj)
        print("subnet obj is :::::",file=sys.stderr)
        subnet_exsist = configs.db.query(subnet_table).filter_by(subnet_id = subnet_obj['subnet_id']).first()
        if subnet_exsist:
            subnet_exsist.subnet_mask = subnet_obj['subnet_mask']
            subnet_exsist.subnet_name = subnet_obj['subnet_name']
            subnet_exsist.location = subnet_obj['subnet_location']
            subnet_exsist.discovered = 'Not Discovered'
            UpdateDBData(subnet_exsist)
            subnet_dict = {
                "subnet_id":subnet_exsist.subnet_id,
                "subnet_mask":subnet_exsist.subnet_mask,
                "subnet_address": subnet_exsist.subnet_address,
                "subnet_name":subnet_exsist.subnet_name,
                "subnet_location":subnet_exsist.location,
                "discovered":subnet_exsist.discovered
            }
            subnet_data_dict['data'] = subnet_dict
            subnet_data_dict['message'] = f"{subnet_exsist.subnet_address} : Updated Successfully"
            subnet_list.append(subnet_dict)
        return JSONResponse(content=subnet_data_dict,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While adding the subenrt",status_code=500)


@router.get('/fetch_ipam_devices',responses={
    200:{"model":SummeryResponseSchema},
    400:{"model":str},
    500:{"model":str}
},
summary="Use API in the IPam devices page on a fetch button to fetch all the devices this API is of get method",
description="Use API in the IPam devices page on a fetch button to fetch all the devices this API is of get method"
            )
def fetch_ipam_devices():
    try:
        data = []
        host = {}
        devices_data = {}
        success_list = []
        error_list = []
        ipam_devices = configs.db.query(IpamDevicesFetchTable).all()
        for row in ipam_devices:
            atom_id = row.atom_id
            status = FetchIpamDevices(atom_id)
            print("status",status,file=sys.stderr)
            atom_exsist = configs.db.query(AtomTable).filter_by(atom_id = atom_id).first()
            if atom_exsist:
                ip_address = atom_exsist.ip_address
                current_time = datetime.now()
                devices_data['ip_address'] = atom_exsist.ip_address
                devices_data['device_name'] =atom_exsist.device_name

                latest_failed_device = (
                    configs.db.query(FailedDevicesTable)
                    .filter(FailedDevicesTable.ip_address == ip_address)
                    .filter(
                        FailedDevicesTable.date <= current_time)  # Filter for records created up to the current time
                    .order_by(desc(FailedDevicesTable.date))  # Then order by creation_date in descending order
                    .first()  # And get the most recent record
                )
                if latest_failed_device:
                    error_list.append(f"{latest_failed_device.ip_address} : failed due to {latest_failed_device.failure_reason}")
                else:
                    ipam_devices = configs.db.query(IpamDevicesFetchTable).filter_by(atom_id=atom_id).all()
                    for device in ipam_devices:
                        devices_data['ipam_device_id'] = device.ipam_device_id
                        devices_data['interface_ip'] = device.interface_ip
                        devices_data['interface'] = device.interface
                        devices_data['interface_description'] = device.interface_description
                        devices_data['virtual_ip'] = device.virtual_ip
                        devices_data['vlan'] = device.vlan
                        devices_data['vlan_number'] = device.vlan_number
                        devices_data['interface_status'] = device.interface_status
                        devices_data['fetch_date'] = device.fetch_date
                        ip_interfaces = configs.db.query(ip_interface_table).filter_by(
                            ipam_device_id=device.ipam_device_id).all()
                        for ip in ip_interfaces:
                            devices_data['discovered_from'] = ip.discovered_from
                        subnet = configs.db.query(subnet_table).filter_by(ipam_device_id=device.ipam_device_id).all()
                        for row in subnet:
                            devices_data['subnet_address'] = row.subnet_address
                            devices_data['subnet_mask'] = row.subnet_mask
                            devices_data['location'] = row.location
                            devices_data['subnet_name'] = row.subnet_name
                            subnet_usage = configs.db.query(subnet_usage_table).filter_by(subnet_id=row.subnet_id).all()
                            for usage in subnet_usage:
                                devices_data['subnet_usage'] = usage.subnet_usage
                                devices_data['subnet_size'] = usage.subnet_size
                        data.append(devices_data)
                        success_list.append(f"{atom_exsist.ip_address} : Fetched Successfully")
        respones = {
            "data":data,
            "suucess_list":success_list,
            "error_list": error_list,
            "success":len(success_list),
            "error":len(error_list)
        }

        print("reposne",respones,file=sys.stderr)
        return respones
        return JSONResponse(content="IPAM devices Fetched",status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Fetching Ipam Devices",status_code=500)


@router.post('/delete_subnets',responses = {
    200:{"model":DeleteResponseSchema},
    500:{"model":str}
},
summary="Use this API in the subnet table to delete the subents based on there ids",
description="Use this APi in the subnet table to delete the subnet based on there ids"
)
def delete_subnets(subnet:list[int]):
    try:
        data = []
        success_list = []
        error_list = []

        # Assuming subnet is a list of subnet IDs
        for subnet_id in subnet:
            subnet_exsist = configs.db.query(subnet_table).filter_by(subnet_id=subnet_id).first()
            if subnet_exsist:
                data.append(subnet_id)
                DeleteDBData(subnet_exsist)
                success_list.append(f"{subnet_id} : Subnet Deleted Successfully")
            else:
                error_list.append(f"{subnet_id} : Subnet Not Found")

        responses = {
            "data": data,
            "success_list": success_list,
            "error_list": error_list,
            "success": len(success_list),
            "error": len(error_list)
        }
        return responses
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Deleting the Subnet", status_code=500)


@router.get('/get_all_ip_history',
            responses = {
                200:{"model":list[IPhistorySchema]},
                500:{"model":str}
            },
            summary = "Use this API in the subnet IP history page to list down all the IP history in a table",
            description = "Use this API in the subnet IP histoory page to list down all the IP history in a table"
            )
def get_ip_history():
    try:
        history_list = []
        history = configs.db.query(IP_HISTORY_TABLE).all()
        for data in history:
            history_dict = {
                "ip_history_id":data.ip_history_id,
                "mac_address":data.mac_address,
                "ip_address":data.ip_address,
                "asset_tag":data.asset_tag,
                "date":data.date
            }
            history_list.append(history_dict)
        return  history_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting the IP History",status_code=500)


@router.post('/get_history_by_ip',
            responses={
                200: {"model": list[IPhistorySchema]},
                500: {"model": str}
            },
            summary="Use this API in the subnet => IP details page to get the history based on the IP click",
            description="Use this API in the subnet => IP details page to get the history based on the IP click"
            )
def get_history_by_ip(ip_address: IpHistoryResponseSchema):
    try:
        print("ip history is:ipaddress",ip_address,file=sys.stderr)
        history_list = []
        history = configs.db.query(IP_HISTORY_TABLE).filter_by(ip_address=ip_address.ip_address).all()
        print("history is:::::::::::::::",history,file=sys.stderr)
        for data in history:
            print("data in istory is:::::::::::::",data,file=sys.stderr)
            history_dict = {
                "ip_history_id": data.ip_history_id,
                "mac_address": data.mac_address,
                "ip_address": data.ip_address,
                "asset_tag": data.asset_tag,
                "date": data.date
            }
            print("history_dict is:::::::::",history_dict,file=sys.stderr)
            history_list.append(history_dict)
        print("history list is::::::::",history_list,file=sys.stderr)
        return history_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error occurred while fetching history", status_code=500)


@router.post('/delete_dns_servers',responses = {
    200:{"model":DeleteResponseSchema},
    400:{"model":str},
    500:{"model":str}
},
summary = "Use this API in the DNS Server Page to delete the DNS Servers.This API is of post methods and accepts list of integers",
description = "Use this API in the DNS Server Page to delete the DNS Servers.This API is of post methods and accepts list of integers"
)
def delete_dns(dns:list[int]):
    try:
        deleted_ids =[]
        error_list = []
        success_list = []
        for ids in dns:
            dns_exsist = configs.db.query(DnsServerTable).filter_by(dns_server_id = ids).first()
            if dns_exsist:
                deleted_ids.append(ids)
                DeleteDBData(dns_exsist)
                success_list.append(f"{ids} : Deleted Successfully")
            else:
                error_list.append(f"{ids} : DNS Server ID Not Found")
        responses = {
            "data":deleted_ids,
            "success_list":success_list,
            "error_lsit":error_list,
            "success":len(success_list),
            "error":len(error_list)
        }
        return responses
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Deleting the DNS Server",status_code=500)


@router.post('/get_dns_zones_by_server_id', responses={
    200:{"model":list[GetallDnsServers]},
    400:{"model":str},
    500:{"model":str}
},
summary="Use this API in the dns server page while clicking on dns server get the dns zones",
description="Use this API in the dns server page while clicking on dns server get the dns zones"
)
def get_dns_zones_by_server_id(dns_server_id:DnsZoneByServerID):
    try:
        objList = []
        dns_server_exsist = configs.db.query(DnsServerTable).filter_by(dns_server_id = dns_server_id.dns_server_id).first()
        if dns_server_exsist:
           dns_zones = configs.db.query(DnsZonesTable).filter_by(dns_server_id = dns_server_exsist.dns_server_id).all()
           for dnsZoneObj in dns_zones:
               objDict = {}
               objDict['dns_id'] = dnsZoneObj.dns_zone_id
               objDict['zone_name'] = dnsZoneObj.zone_name
               objDict['zone_status'] = dnsZoneObj.zone_status
               objDict['zone_type'] = dnsZoneObj.zone_type
               objDict['lookup_type'] = dnsZoneObj.lookup_type
               objList.append(objDict)
        else:
            return JSONResponse(content=f"{dns_server_id.dns_server_id} : Not Found",status_code=400)
        return objList
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While getting the DNS Server Zones",status_code=500)


@router.get('/get_dns_record_by_zone_id',
            responses = {
                200:{"model":list[GetDnsRecoed]},
                400:{"model":str},
                500:{"model":str}
            })
def get_dns_record_by_zones(dns_zone_id: int = Query(..., description="ID of dns server")):
    try:
        objList =[]
        dns_zone_exsist = configs.db.query(DnsZonesTable).filter_by(dns_zone_id = dns_zone_id).first()
        if dns_zone_exsist:
            dns_record = configs.db.query(DnsRecordTable).all()
            for dnsServersRecordObj in dns_record:
                objDict = {}
                objDict['dns_record_id'] = dnsServersRecordObj.dns_id
                objDict['server_name'] = dnsServersRecordObj.server_name
                objDict['server_ip'] = dnsServersRecordObj.server_ip
                objList.append(objDict)
            print(objList,file=sys.stderr)
            return objList
        else:
            return JSONResponse(content=f"{dns_zone_id} : Not Founbd",status_code=400)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Dns Record by zone",status_code=500)



@router.post('/edit_dns',
             responses={
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="Use this API to edit the DNS in the DNs page.This API is of post method",
             description="Use this API to edit the DNS in the DNs page.This API is of post method"
             )
def AddDNS(data: EditDnsSchema):
    try:
        data_dns = {}
        response = False
        dns_data_dict = {}
        print("data is::::",data,file=sys.stderr)
        dns_data = dict(data)
        dns_exsist = configs.db.query(DnsServerTable).filter_by(dns_server_id = dns_data['dns_server_id']).first()
        if dns_exsist:
            if dns_data['ip_address'] and dns_data['user_name'] and dns_data['password']:
                try:
                    tool = WinOSClient(host=dns_data['ip_address'], username=dns_data['user_name'],
                                       password=dns_data['password'])
                    print("tootl is:::::::::::::::::::::::::::::::",tool,file=sys.stderr)
                    response = tool.run_ps('Get-DnsServerZone | ConvertTo-Json')
                    print("repsonse of the add dns test is:::::::::::::::::",response,file=sys.stderr)
                    response = True
                except Exception as e:
                    traceback.print_exc()
            else:
                response = False
            if response == True:

                add_dns = DnsServerTable()
                print("ip_address found in dns ip address True updating executing>>", file=sys.stderr)
                dns_query1 = configs.db.query(DnsServerTable).filter_by(ip_address=dns_data['ip_address']).first()
                if dns_query1:
                    print("dns query is >>>>>>>>>>>", dns_query1, file=sys.stderr)
                    # updating the add dns table
                    dns_query1.ip_address = dns_data['ip_address']
                    dns_query1.user_name = dns_data['user_name']
                    dns_query1.password = dns_data['password']
                    dns_query1.server_name = dns_data['server_name']
                    dns_query1.number_of_zones = 0
                    dns_query1.type = ''
                    UpdateDBData(add_dns)
                    dns_data_dict['ip_address'] = dns_query1.ip_address
                    dns_data_dict['user_name'] = dns_query1.user_name
                    dns_data_dict['password'] = dns_query1.password
                    dns_data_dict['server_name'] = dns_query1.server_name
                    dns_data_dict['number_of_zones'] = dns_query1.number_of_zones
                    dns_data_dict['type'] = dns_query1.type
                    dns_data_dict['dns_server_id'] = dns_query1.dns_server_id
                    print("DNS Table Updated >>>>>>>>>>", file=sys.stderr)
                    data_dns['data'] = dns_data_dict
                    data_dns['message'] = f"{dns_data['ip_address']} : DNS Updated Successfully"

                return data_dns
            else:
                return JSONResponse(content="DNS Server Is Not Authenticated",status_code=400)
        else:
            return JSONResponse(content=f"{dns_data['dns_server_id']} : Not Exsists",status_code=400)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Updating The DNS",status_code=500)


@router.get('/get_ipam_devices_fetch_dates',responses={
    200:{"model":str},
    500:{"model":str}
},
summary = "API to get the IPAM fetch dates",
description="API to get the IPAM fetch dates"
)
async def et_ipam_fetch_dates():
    try:
        query = f"SELECT DISTINCT fetch_date FROM ipam_devices_fetch_table ORDER BY fetch_date DESC;"
        result = configs.db.execute(query)
        print("result ofr the fetch date is:::",result,file=sys.stderr)
        dates = []
        for row in result:
            fetch_date = row[0]  # Access the datetime object
            print("fetch date is:::::::::",fetch_date,file=sys.stderr)
            if fetch_date:  # Check if fetch_date is not None
                formatted_date = fetch_date.strftime("%d-%m-%Y-%H%M %S")
                print("formatted date for the fetch date is:", formatted_date, file=sys.stderr)
                dates.append(fetch_date)
        print("date are::::",dates,file=sys.stderr)
        return dates
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error occured while getting the ipam fetch dates",status_code=500)


@router.post('/get_ipam_by_date',responses ={
    200:{"model":str},
    400:{"model":str},
    500:{"model":str}
},
summary="API to get ipam by dates",
description="API to get the ipamby dates"
)
async def get_ipam_by_date(date:str):
    try:
        date_data = dict(date)
        utc = datetime.strptime(
            date_data['date'],'%a, %d %b %Y %H:%M:%S GMT'
        )
        current_time = utc.strftime("%Y-%m-%d %H:%M:%S")
        print('current_time is :', current_time, file=sys.stderr)
        print(current_time, file=sys.stderr)
        objList = []
        fetch_date = configs.db.query(IpamDevicesFetchTable).filter_by(fetch_date = utc).first()
        if fetch_date:
            fetch_dict = {
                "ipam_device_id":fetch_date.ipam_device_id,
                "interface":fetch_date.interface,
                "interface_ip":fetch_date.interface_ip,
                "interface_description":fetch_date.interface_description,
                "virtual_ip":fetch_date.virtual_ip,
                "vlan":fetch_date.vlan,
                "vlan_number":fetch_date.vlan_number,
                "interface_status":fetch_date.interface_status,
                "fetch_date":fetch_date.fetch_date
            }
            objList.append(fetch_dict)
        return objList
    except Exception as e:
        traceback.print_exc()


@router.post('/delete_ipam_devices',
             responses={
                 200:{"model":str},
                 400:{"model":str},
                 500:{"model":str}
             }
             )
def delete_ipam_device(ipam_data:list[int]):
    try:
        data = []
        success_list = []
        error_list = []
        for ipam_id in ipam_data:
            print("ipam_id:::::::::::::::",ipam_id,file=sys.stderr)
            is_ipam_device_exsists = configs.db.query(IpamDevicesFetchTable).filter_by(ipam_device_id = ipam_id).first()
            if is_ipam_device_exsists:
                data.append(is_ipam_device_exsists.ipam_device_id)
                DeleteDBData(is_ipam_device_exsists)
                success_list.append(f"IPAM devices deleted successfully")
            else:
                error_list.append("IPAM device id not found")
        responses = {
            "data":data,
            "success":len(success_list),
            "error":len(error_list),
            "success_list":success_list,
            "error_list":error_list
        }

        return responses
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured while deleteing ipam device",status_code=500)