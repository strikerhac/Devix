import traceback
from subprocess import Popen, PIPE
from netaddr import IPNetwork
from ipaddress import ip_network, ip_address
from ipaddress import ip_interface
from app.ipam_scripts.ipam import *
from app.ipam_scripts.f5 import F5 as load_balancer_f5
from app.ipam_scripts.ipam_physical_mapping import *
from app.ipam_scripts.fortigate_vip import *
from app.api.v1.ipam.routes.device_routes import *
from pywinos import WinOSClient
from app.models.atom_models import *
# from app.api.v1.ipam.ipam_import import *
# from app.api.v1.ipam.ipam_import import *
import platform
import subprocess
import nmap
from app.api.v1.ipam.utils.ipam_utils import *


def sizeCalculator(subnet):
    subnetCdrs = {'/32': 1, '/31': 2, '/30': 2, '/29': 6, '28/': 14, '/27': 30, '/26': 62, '/25': 126, '/24': 254,
                  '/23': 510, '/22': 1022, '/21': 2046, '/20': 4094, '/19': 8190, '/18': 16382, '/17': 32766,
                  '/16': 65534, '/15': 131070, '/14': 262142, '/13': 524286, '/12': 1048574, '/11': 2097150,
                  '/10': 4194302, '/9': 8388606, '/8': 16777214, '/7': 33554430, '/6': 67108862, '/5': 134217726,
                  '/4': 268435454, '/3': 536870910, '/2': 1073741822, '/1': 2147483646, '/0': 4294967294}
    temp_size = 0
    for subnetCdr in subnetCdrs:
        if subnet[-3:] == subnetCdr or subnet[-2:] == subnetCdr:
            temp_size = subnetCdrs[subnetCdr]
    return temp_size



def handle_ipam_devices_fetch_table(ipam, host, atom_id):
    try:
        ipam_db_entry = configs.db.query(IpamDevicesFetchTable).filter_by(interface_ip=ipam['ip_address']).first()
        if ipam_db_entry:
            # Update or set fields for IPAM device
            ipam_db_entry.interface_ip = ipam.get('ip_address')
            ipam_db_entry.atom_id = atom_id
            ipam_db_entry.fetch_date = datetime.now()
            ipam_db_entry.interface = ipam.get("interface", "")
            ipam_db_entry.interface_status = 'up' if 'up' in ipam.get("protocol_status", "down") else 'down'
            ipam_db_entry.vlan_number = ipam.get("vlan_number", "")
            ipam_db_entry.interface_description = ipam.get("description", "")
            ipam_db_entry.vlan = ipam.get("vlan_name", "")
            ipam_db_entry.virtual_ip = ipam.get("virtual_ip", "")
            UpdateDBData(ipam_db_entry)
            print("Ipam devices fetch tbale updated")
        else:
            ipam_db_entry = IpamDevicesFetchTable()
            # Update or set fields for IPAM device
            ipam_db_entry.interface_ip = ipam.get('ip_address')
            ipam_db_entry.atom_id = atom_id
            ipam_db_entry.fetch_date = datetime.now()
            ipam_db_entry.interface = ipam.get("interface", "")
            ipam_db_entry.interface_status = 'up' if 'up' in ipam.get("protocol_status", "down") else 'down'
            ipam_db_entry.vlan_number = ipam.get("vlan_number", "")
            ipam_db_entry.interface_description = ipam.get("description", "")
            ipam_db_entry.vlan = ipam.get("vlan_name", "")
            ipam_db_entry.virtual_ip = ipam.get("virtual_ip", "")
            # Additional fields can be updated here

            configs.db.add(ipam_db_entry)
            configs.db.commit()
        return ipam_db_entry.ipam_device_id
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return None


def handle_interface_table(ipam, host, ipam_device_id):
    try:
        interface_entry = configs.db.query(ip_interface_table).filter_by(interface_ip=ipam['ip_address']).first()
        if interface_entry:
            # Update or set fields for interface
            interface_entry.interface_ip = ipam['ip_address']
            interface_entry.ipam_device_id = ipam_device_id
            interface_entry.discovered_from = host.get('device_name')
            interface_entry.interface_location = ipam.get("description", "")
            interface_entry.interfaces = ','.join(ipam.get('interfaces', []))
            interface_entry.mac_address = ipam.get('mac_address', "")
            interface_entry.interface_status = 'up' if 'up' in ipam.get("protocol_status", "down") else 'down'
            # Additional fields can be updated here
            UpdateDBData(interface_entry)
        else:
            interface_entry = ip_interface_table()
            # Update or set fields for interface
            interface_entry.interface_ip = ipam['ip_address']
            interface_entry.ipam_device_id = ipam_device_id
            interface_entry.discovered_from = host.get('device_name')
            interface_entry.interface_location = ipam.get("description", "")
            interface_entry.interfaces = ','.join(ipam.get('interfaces', []))
            interface_entry.mac_address = ipam.get('mac_address', "")
            interface_entry.interface_status = 'up' if 'up' in ipam.get("protocol_status", "down") else 'down'
            # Additional fields can be updated here
            configs.db.add(interface_entry)
            configs.db.commit()
        return interface_entry.ip_interface_id
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return None


def handle_subnet_table(ipam, host, ipam_device_id):
    try:
        subnet_entry = configs.db.query(subnet_table).filter_by(subnet_address=ipam.get('subnet')).first()
        if subnet_entry:
            # Update or set fields for subnet
            subnet_entry.subnet_address = ipam.get('subnet')
            subnet_entry.subnet_mask = ipam.get('subnet_mask', "")
            subnet_entry.ipam_device_id = ipam_device_id
            subnet_entry.subnet_name = host.get('device_name')
            subnet_entry.discovered = 'Discovered'
            # Additional fields can be updated here, such as discovered_from, discovered status, etc.
            UpdateDBData(subnet_entry)
        else:
            subnet_entry = subnet_table()
            # Update or set fields for subnet
            subnet_entry.subnet_address = ipam.get('subnet')
            subnet_entry.subnet_mask = ipam.get('subnet_mask', "")
            subnet_entry.ipam_device_id = ipam_device_id
            subnet_entry.subnet_name = host.get('device_name')
            subnet_entry.discovered = 'Discovered'
            # Additional fields can be updated here, such as discovered_from, discovered status, etc.

            configs.db.add(subnet_entry)
            configs.db.commit()
        return subnet_entry.subnet_id
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return None


def handle_subnet_usage(ipam, host, subnet_id):
    try:
        subnet_data = ipam.get("subnet", "")
        subnet_exsists = configs.db.query(subnet_usage_table).filter_by(subnet_id=subnet_id).first()
        if subnet_exsists:
            subnet_exsists.subnet_size = sizeCalculator(str(subnet_data))
            UpdateDBData(subnet_exsists)
        else:
            subnet_exsists = subnet_usage_table()
            # Assign subnet_id based on whether it's an existing subnet or newly inserted
            subnet_exsists.subnet_id = subnet_id
            subnet_exsists.subnet_size = sizeCalculator(str(subnet_data))
            InsertDBData(subnet_exsists)
        return subnet_exsists.subnet_usage_id
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return None


def aggregate_device_data(ipam, host, ipam_device_id, interface_id, subnet_id):
    aggregated_data = {
        # IPAM Device attributes
        "ipam_device_id": ipam_device_id,
        "interface_ip": ipam.get('ip_address'),
        "atom_id": host.get('atom_id'),
        "interface": ipam.get("interface", ""),
        "interface_status": 'up' if 'up' in ipam.get("protocol_status", "down") else 'down',
        "vlan_number": ipam.get("vlan_number", ""),
        "interface_description": ipam.get("description", ""),
        "vlan": ipam.get("vlan_name", ""),
        "virtual_ip": ipam.get("virtual_ip", ""),
        "fetch_date": datetime.now(),  # Assuming fetch_date is set to now if not provided

        # Interface attributes
        "interface_id": interface_id,
        "discovered_from": host.get('device_name'),
        "interface_location": ipam.get("description", ""),  # Duplication with interface_description
        "interfaces": ','.join(ipam.get('interfaces', [])),  # Assuming this is a list of interfaces
        "mac_address": ipam.get('mac_address', ""),

        # Subnet attributes
        "subnet_id": subnet_id,
        "subnet_address": ipam.get('subnet'),
        "subnet_mask": ipam.get('subnet_mask', ""),
    }
    print("attrbute data is:::::::::::::::::::",aggregated_data,file=sys.stderr)

    # Optional: Add additional processing if some data needs to be transformed or enriched
    return aggregated_data