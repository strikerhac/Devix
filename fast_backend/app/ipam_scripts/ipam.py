import traceback
from netmiko import Netmiko
# from app import db
from datetime import datetime
import re, sys, time, json
# from app.models.inventory_models import IPAM_DEVICES_FETCH_TABLE
import threading
import socket, struct
# from app.monitoring.common_utils.utils import addFailedDevice
from app.utils.failed_utils import addFailedDevice
from netaddr import IPNetwork
from app.utils.db_utils import *
from fastapi import FastAPI
from app.models.ipam_models import *
import ipaddress
from app.api.v1.ipam.utils.ipam_db_utils import *



def FormatDate(date):
    # print(date, file=sys.stderr)
    if date is not None:
        result = date.strftime('%d-%m-%Y')
    else:
        # result = datetime(2000, 1, 1)
        result = datetime(1, 1, 2000)

    return result


def FormatStringDate(date):
    print(date, file=sys.stderr)

    try:
        if date is not None:
            if '-' in date:
                result = datetime.strptime(date, '%d-%m-%Y')
            elif '/' in date:
                result = datetime.strptime(date, '%d/%m/%Y')
            else:
                print("incorrect date format", file=sys.stderr)
                result = datetime(2000, 1, 1)
        else:
            # result = datetime(2000, 1, 1)
            result = datetime(2000, 1, 1)
    except:
        result = datetime(2000, 1, 1)
        print("date format exception", file=sys.stderr)

    return result


class IPAM(object):
    print("start of IPAM CLASSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", file=sys.stderr)

    def __init__(self):
        self.connections_limit = 50
        self.failed_devices = []
        # self.addInventoryToDB(host,ipam_data)
        # self.poll(host)

    # def add_to_failed_devices(self, host, reason):
    #     failed_device= {}
    #     failed_device["ip_address"]= host
    #     failed_device["date"]= time.strftime("%d-%m-%Y")
    #     failed_device["time"]= time.strftime("%H-%M-%S")
    #     failed_device["reason"]= reason
    #     self.failed_devices.append(failed_device)

    def print_failed_devices(self, ):
        print("Printing Failed Devices::::::::::::::::::::::::::::::::::::::::::::::")
        file_name = time.strftime("%d-%m-%Y") + "-IPAM.txt"
        failed_device = []
        self.is_login =False        # Read existing file
        try:
            with open('app/failed/ims/' + file_name, 'r', encoding='utf-8') as fd:
                failed_device = json.load(fd)
        except:
            pass
        # Update failed devices list
        failed_device = failed_device + self.failed_devices
        try:
            with open('app/failed/ims/' + file_name, 'w', encoding='utf-8') as fd:
                fd.write(json.dumps(failed_device))
        except Exception as e:
            print(e)
            print("Failed to update failed devices list" + str(e), file=sys.stderr)

    def InsertDBData(obj):
        try:
            configs.db.add(obj)
            configs.db.commit()
            return 200
        except Exception as e:
            configs.db.rollback()
            traceback.print_exc()
            print(
                f"Something else went wrong in Database Insertion: {e}", file=sys.stderr)
        return 500

    def sizeCalculator(self, subnet):
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

    def addInventoryToDB(self, host, ipam_data):
        try:
            inventory_data = []
            atom_id = host.get('atom_id')

            for ipam in ipam_data:
                if not ipam.get('ip_address'):
                    continue  # Skip if there's no IP address

                # Handle IPAM devices fetch table
                ipam_device_id = handle_ipam_devices_fetch_table(ipam, host, atom_id)

                # Handle interface table
                interface_id = handle_interface_table(ipam, host, ipam_device_id)

                # Handle subnet table
                subnet_id = handle_subnet_table(ipam, host, ipam_device_id)

                #Handle Subnet usage table
                subnet_usage = handle_subnet_usage(ipam,host,subnet_id)
                # Aggregate device data
                device_dict = aggregate_device_data(ipam, host, ipam_device_id, interface_id, subnet_id)
                inventory_data.append(device_dict)

            return inventory_data
        except Exception as e:
            traceback.print_exc()
            print("error in addInventoryToDB",str(e))

    def get_inventory_data(self, hosts):
        print("Get Inventory data is::::::::::::::::::::::::::", hosts, file=sys.stderr)

        threads = []
        for host in hosts:
            th = threading.Thread(target=self.poll, args=(host,))
            print("th is::::::::::::::::::::::::::::::::", th, file=sys.stderr)
            th.start()
            threads.append(th)
            if len(threads) == self.connections_limit:
                for t in threads:
                    t.join()
                threads = []

        else:
            for t in threads:  # if request is less than connections_limit then join the threads and then return data
                t.join()
            return ""

    def poll(self, host):
        print('HOST IN POLL IS::::::::::::::::::::::::::::::::::::::', host, file=sys.stderr)
        vlans = interfaces = virtualIps = ipamData = secondary_ips = []
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 4
        login_exception = ''
        c = 0
        is_login = False
        sw_type = str(host['device_type']).lower()
        login_exception = ''
        sw_type = sw_type.strip()
        while c < login_tries:
            print("login tries are::::::::::::::::::::::::::::::::::::::", c, file=sys.stderr)
            try:
                device_type = host['device_type']
                device_type = device_type.split('-')[0] if 'leaf' in device_type else device_type
                device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'],
                                 device_type=device_type, timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}")
                is_login = True
                break
            except Exception as e:
                c += 1
                login_exception = str(e)
                traceback.print_exc()

        if is_login == False:
            print(f"Falied to login {host['ip_address']}:::::::::::::::::::::::::::::::::::::::::::::::::::",
                  file=sys.stderr)
            print("failed login for host is::::::::::::::::::::::::::::::::", host, file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Failed to login to host")
            date = datetime.now()
            device_type = host['device_type']
            addFailedDevice(host['ip_address'], date, device_type, login_exception, 'IPAM')

        if is_login == True:
            print(f"Successfully Logged into device {host['ip_address']}", file=sys.stderr)
            if host['device_type'] == 'fortinet':
                print("getting System ARP Detail")
                try:
                    systemArps = device.send_command('get system interface physical', use_textfsm=True,
                                                     textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/fortigate_show_system_interface_physical.textfsm")
                    interfaces1 = list(filter(lambda int: (
                                int['ip_address'] != '' and int['ip_address'].lower() != 'unassigned' and int[
                            'ip_address'].lower() != 'unknown' and int['ip_address'] != '0.0.0.0'), systemArps))
                    print(interfaces1, file=sys.stderr)
                    tempList = []

                    systemArps = device.send_command('show system interface', use_textfsm=True,
                                                     textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/fortigate_show_system_interface.textfsm")
                    interfaces = list(filter(lambda int: (
                                int['ip_address'] != '' and int['ip_address'].lower() != 'unassigned' and int[
                            'ip_address'].lower() != 'unknown' and int['ip_address'] != '0.0.0.0'), systemArps))
                    print(interfaces, file=sys.stderr)
                    for interface in interfaces1:
                        temp = {}
                        interface2 = list(filter(lambda int: int['ip_address'] == interface['ip_address'], interfaces))
                        if len(interface2) > 0:
                            temp['ip_address'] = interface2[0].get('ip_address')
                            temp['interface_name'] = interface2[0].get('interface')
                            temp['subnet_mask'] = interface2[0].get('subnet')
                            cidr = sum(bin(int(x)).count('1') for x in temp['subnet_mask'].split('.'))
                            ipsubnet = temp['ip_address'] + "/" + str(cidr)
                            ip = IPNetwork(ipsubnet)
                            temp['subnet'] = str(ip.network) + "/" + str(ip).split('/')[1]
                            temp['interface_description'] = interface2[0].get('description')
                            if (interface2[0].get('status')).lower() != 'down':
                                temp['protocol_status'] = 'up'
                            else:
                                temp['protocol_status'] = interface2[0].get('status')
                            temp['vlan_number'] = interface2[0].get('vlan_id')

                            tempList.append(temp)

                    self.addInventoryToDB(host, tempList)
                except Exception as e:
                    print(f"Ipam detail not found {host['ip_address']}, {str(e)}", file=sys.stderr)
                    # self.add_to_failed_devices(host['ip_address'], "Failed to get IPAM data "+str(e))
                    date = datetime.now()
                    addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')
                    traceback.print_exc()
            else:

                try:
                    print("getting ip interface detail", file=sys.stderr)

                    if sw_type == "cisco_nxos-leaf":
                        try:
                            output = device.send_command('show ip interface brief',
                                                         textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/aci_leaf_show_ip_interface_brief.textfsm",
                                                         use_textfsm=True)
                            parsed_vrfs = self.parseAcileafData(output, host)
                            interfaces = list(filter(lambda int: 'overlay' not in int['vrf'], parsed_vrfs))
                            interfaces = self.parseInterfaceKeys(interfaces, host['sw_type'], host)
                            ipam_data = self.getSubnetMask(interfaces, host)
                            print(ipam_data, file=sys.stderr)
                            self.addInventoryToDB(host, ipam_data)

                        except Exception as e:
                            print(f"Ipam detail not found {host['ip_address']}, {str(e)}", file=sys.stderr)
                            # self.add_to_failed_devices(host['ip_address'], "Failed to get IPAM data "+str(e))
                            date = datetime.now()
                            addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')
                            traceback.print_exc()
                        return

                    if sw_type == "cisco_nxos":

                        output = device.send_command('show interface',
                                                     textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/cisco_nxos_show_interface.textfsm",
                                                     use_textfsm=True)
                    else:
                        output = device.send_command('show interface', use_textfsm=True)

                    if isinstance(output, str):
                        print(f"Device data not found {output} {host['ip_address']}", file=sys.stderr)
                        raise Exception(f"Device data not found " + str(output))

                    interfaces = list(filter(lambda int: (
                                int['ip_address'] != '' and int['ip_address'].lower() != 'unassigned' and int[
                            'ip_address'].lower() != 'unknown' and int['ip_address'] != '0.0.0.0'), output))
                    if len(interfaces) == 0:
                        print("No Valid Interface found", file=sys.stderr)
                        return
                    interfaces = self.parseInterfaceKeys(interfaces, host['ip_address'], host)
                    # print(" Valid Interface found:::::::::::::::",interfaces, file=sys.stderr)

                    # adding network detail
                    interfaces = self.getSubnetMask(interfaces, host)

                    # getting vlans
                    try:
                        print("getting Vlans detail", file=sys.stderr)
                        if device_type == 'cisco_ios' or device_type == 'cisco_nxos':
                            vlans = device.send_command('show vlan', use_textfsm=True)
                            # print(vlans, file=sys.stderr)
                            try:
                                secondary_ips = device.send_command('show run | begin interface',
                                                                    textfsm_template='app/pullers/ntc-templates/ntc_templates/templates/cisco_ios_show_secondary_vlan_ip.textfsm',
                                                                    use_textfsm=True)
                                if not isinstance(output, list):
                                    secondary_ips = []
                                # print(f"##  {secondary_ips}", file=sys.stderr)
                            except Exception as e:
                                print(f"Error in getting secondary ips {e}", file=sys.stderr)
                        if isinstance(output, str):
                            print(f"VLAN detail not found {output} {host['ip_address']}", file=sys.stderr)
                            raise Exception(f"Vlan detail not found " + str(output))
                        vlans = self.parseValnKeys(vlans, host['ip_address'], host)
                    except Exception as e:
                        print("Failed to get Vlans", file=sys.stderr)
                        # self.add_to_failed_devices(host['ip_address'], "Failed to get vlan detail "+str(e))
                        date = datetime.now()
                        addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')

                    # getting virtual ip
                    try:
                        print("getting Virtual IPS", file=sys.stderr)
                        if sw_type == 'cisco_ios':
                            virtualIps = device.send_command('show standby',
                                                             textfsm_template='app/pullers/ntc-templates/ntc_templates/templates/cisco_ios_show_standby.textfsm',
                                                             use_textfsm=True)
                            # print(f"%%% {virtualIps}")
                        if sw_type == 'cisco_nxos':
                            virtualIps = device.send_command('show hsrp all',
                                                             textfsm_template='app/pullers/ntc-templates/ntc_templates/templates/cisco_nxos_show_hsrp_all.textfsm',
                                                             use_textfsm=True)
                            # print(virtualIps)
                        if isinstance(output, str):
                            print(f"Virtual IPS detail not found {output} {host['ip_address']}", file=sys.stderr)
                            raise Exception(f"Virtual IPS detail not found " + str(output))
                        virtualIps = self.parseVirtualIpKeys(virtualIps, host['ip_address'], host)
                    except Exception as e:
                        print("Failed to get Virtual IPS", file=sys.stderr)
                        # self.add_to_failed_devices(host['ip_address'], "Failed to get Virtual IPS detail "+str(e))
                        date = datetime.now()
                        addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')

                    # Merging All Dictionaries

                    for interface in interfaces:
                        secondary_ip = {}
                        # print("interface in interfaces is:::::::::::::::::::::::::",interface,file=sys.stderr)
                        try:
                            if "vlan" in interface['interface'].lower():
                                vlan_id = interface['interface'][4:]
                                if isinstance(vlans, list):
                                    matched_vlan = list(filter(lambda vlan: vlan['vlan_id'] == vlan_id, vlans))
                                    if matched_vlan:
                                        interface.update(matched_vlan[0])

                                if isinstance(virtualIps, list):
                                    matched_virtualIps = list(filter(lambda vir: vir['vlan_id'] == vlan_id, virtualIps))
                                    # print(matched_virtualIps, file=sys.stderr)
                                    if matched_virtualIps:
                                        interface.update(matched_virtualIps[0])
                                ###
                            secondary_interface = []
                            try:
                                if len(secondary_ips) > 0 and type(secondary_ips) == list:
                                    secondary_interface = list(
                                        filter(lambda int: int.get('vlan_id') == interface['interface'],
                                               secondary_ips))
                                    # print(f"secondaryint fond {secondary_interface} ", file=sys.stderr)

                            except Exception as e:
                                traceback.print_exc()
                                print(f"Exception in finding Secondary IP host: {host['ip_address']} error: {e}",
                                      file=sys.stderr)

                            if len(secondary_interface) > 0:
                                if secondary_interface[0].get('secondary_ip'):

                                    secondary_ip = interface.copy()
                                    secondary_ip['ip_address'] = secondary_interface[0].get('secondary_ip')
                                    try:
                                        secondary_ip['virtual_ip'] = interface.get('secondary_virtual_ip')
                                        ip = IPNetwork(secondary_ip['ip_address'])
                                        secondary_ip['subnet_mask'] = secondary_interface[0].get(
                                            'secondary_subnet_mask')
                                        ip.netmask = secondary_interface[0].get('secondary_subnet_mask')
                                        secondary_ip['subnet'] = str(ip)
                                    except Exception as e:
                                        print("Failed to get secondary virtual ip", file=sys.stderr)

                                    ipamData.append(secondary_ip)

                            ipamData.append(interface)
                        except Exception as e:
                            print("Failed to Parse IPAM data" + str(e), file=sys.stderr)
                            # self.add_to_failed_devices(host['ip_address'], "Failed to Parse IPAM data"+str(e))
                            date = datetime.now()
                            addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')
                            traceback.print_exc()

                    # print(f"Final IPAM Data is : {ipamData}", file=sys.stderr)
                    self.addInventoryToDB(host, ipamData)

                except Exception as e:
                    print(f"Ipam detail not found {host['ip_address']}, {str(e)}", file=sys.stderr)
                    # self.add_to_failed_devices(host['ip_address'], "Failed to get IPAM data "+str(e))
                    date = datetime.now()
                    addFailedDevice(host['ip_address'], date, device_type, str(e), 'IPAM')
                    traceback.print_exc()

    def getSubnetMask(self, interfaces, host):
        try:
            for interface in interfaces:
                print("interfaces in interfaxes is::::::::::::::::::", interface, file=sys.stderr)
                try:
                    ip = ipaddress.ip_interface(interface['ip_address'])
                    print("ip is:::::::::::::::::::::", ip, file=sys.stderr)
                    network = ipaddress.ip_network(ip.network)
                    interface['subnet'] = str(network)
                    interface['ip_address'] = ip.ip
                    interface['subnet_mask'] = ip.netmask
                except Exception as e:
                    print(f"Exception Occurred for Interface {interface}: {e}", file=sys.stderr)
                    # Handle the exception for this specific interface
                    # You can log, modify, or perform other operations here
        except Exception as e:
            print(f"Exception Occurred for Host {host['ip_address']}: {e}", file=sys.stderr)
            traceback.print_exc()
            # Handle the exception for the host itself
            date = datetime.now()
            addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')

        return interfaces

    def parseInterfaceKeys(self, interfaces, sw_type, host):
        try:
            for interface in interfaces:
                if sw_type == 'cisco_ios':
                    interface['vlan_number'] = interface['interface'][4:] if 'vlan' in interface[
                        'interface'].lower() else ''
                    interface['interface_name'] = interface.pop('interface')
                    interface['admin_status'] = interface.pop('link_status')

                elif sw_type == 'cisco_xr':
                    interface['vlan_number'] = interface['interface'][4:] if 'vlan' in interface[
                        'interface'].lower() else ''
                    interface['interface_name'] = interface.pop('interface')
                    interface['protocol_status'] = interface.pop('link_status')
                    interface['admin_status'] = interface.pop('admin_state')

                elif sw_type == 'cisco_nxos':
                    interface['vlan_number'] = interface['interface'][4:] if 'vlan' in interface[
                        'interface'].lower() else ''
                    interface['interface_name'] = interface.pop('interface')
                    interface['protocol_status'] = interface.pop('link_status')
                    interface['admin_status'] = interface.pop('admin_state')

                elif sw_type == 'cisco_nxos-leaf':
                    interface['vlan_number'] = interface['interface_name'][4:] if 'vlan' in interface[
                        'interface_name'].lower() else ''
                    interface['vlan_name'] = interface['vrf'] if 'vlan' in interface['interface_name'].lower() else ''
                    interface['description'] = interface['vrf']

        except Exception as e:
            print(f"Exception Occured while Parsing Interfaces Keys {e}", file=sys.stderr)
            traceback.print_exc()

            # self.add_to_failed_devices(host['ip_address'], "Exception Occured while Parsing Interfaces Keys "+str(e))
            date = datetime.now()
            addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')

        return interfaces

    def parseValnKeys(self, vlans, sw_type, host):
        try:
            for vlan in vlans:
                if sw_type == 'cisco_ios' or sw_type == 'cisco_nxos':
                    vlan['vlan_name'] = vlan.pop('name')
        except Exception as e:
            print(f"Exception Occured while Parsing Vlan Keys {e}", file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Exception Occured while Parsing Vlan Keys "+str(e))
            date = datetime.now()
            addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')

        return vlans

    def parseVirtualIpKeys(self, virtualIps, sw_type, host):
        try:
            for virtualIp in virtualIps:
                if sw_type == 'cisco_ios':
                    virtualIp['virtual_ip'] = virtualIp.pop('virtual_ip')
                if sw_type == 'cisco_nxos':
                    virtualIp['virtual_ip'] = virtualIp.pop('primary_ipv4_address')
                    virtualIp['group'] = virtualIp.pop('group_number')
        except Exception as e:
            print(f"Exception Occured while Parsing Vitual IP Keys {e}", file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Exception Occured while Parsing Virtual IP Keys "+str(e))
            date = datetime.now()
            addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')
        return virtualIps

    def parseAcileafData(self, interfaces, host):
        try:
            interfaces = self.parseVrfs(interfaces, host)

        except Exception as e:
            print(f"Exception Occured While Parsing ACI Leaf data {e}", file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Exception Occured while Parsing ACI LEAF data "+str(e))
            date = datetime.now()
            addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')
        return interfaces

    def parseVrfs(self, interfaces, host):
        vrf = ""
        for interface in interfaces:
            try:
                if interface['vrf'] != "" and interface['vrf'] != ":":
                    vrf = interface['vrf']
                interface['vrf'] = vrf
            except Exception as e:
                print(f"Exception Occured While Parsing VRFS {e}", file=sys.stderr)
                # self.add_to_failed_devices(host['ip_address'], "Exception Occured while Parsing VRFS "+str(e))
                date = datetime.now()
                addFailedDevice(host['ip_address'], date, host['device_type'], str(e), 'IPAM')

        return interfaces

    def FormatStringDate(self, date):
        # print(date, file=sys.stderr)
        try:

            if date is not None:
                result = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                return result

        except:
            result = datetime(2000, 1, 1)
            print("date format exception", file=sys.stderr)
            return result

    def getIpam(self, devices):
        puller = IPAM()
        hosts = []
        # with open('app/cred.json') as inventory:
        #     inv = json.loads(inventory.read())
        for device in devices:

            user_name = device['username']
            password = device['password']

            print(device, file=sys.stderr)
            sw_type = str(device['device_type']).lower()

            if sw_type == 'cisco_ios':
                sw_type = 'cisco_ios'
            elif sw_type == 'ios-xe':
                sw_type = 'cisco_ios'
            elif sw_type == 'ios-xr':
                sw_type = 'cisco_xr'
            elif sw_type == 'nx-os':
                sw_type = 'cisco_nxos'
            elif sw_type == 'aci-leaf':
                sw_type = 'cisco_nxos-leaf'
            elif sw_type == 'fortinet':
                sw_type = 'fortinet'
            else:
                sw_type = ''

            host = {
                "ip_address": device["ip_address"],
                "user": user_name,
                "pwd": password,
                "sw_type": sw_type,
                "time": (datetime.now()),
                "device_name": device["device_name"]
            }

            hosts.append(host)
        puller.get_inventory_data(hosts)
        puller.print_failed_devices()
        print("IPAM Completed", file=sys.stderr)