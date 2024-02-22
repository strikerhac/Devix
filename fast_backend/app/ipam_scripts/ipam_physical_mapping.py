from netmiko import Netmiko
# from app import db
import json
import sys
import threading
import time
# from app import db
from datetime import datetime

# from app.monitoring.common_utils.utils import addFailedDevice
from app.utils.db_utils import *
from netmiko import Netmiko


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


class IPAMPM(object):
    def __init__(self):
        self.connections_limit = 1
        self.failed_devices = []

    def print_failed_devices(self, ):
        print("Printing Failed Devices")
        file_name = time.strftime("%d-%m-%Y") + "-IPAM.txt"
        failed_device = []
        # Read existing file
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

    def get_inventory_data(self, hosts):

        threads = []
        for host in hosts:
            th = threading.Thread(target=self.poll, args=(host,))
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
        global device, arps
        pmData = []
        ipData = []
        print("host is:::::::::::::::::::::::",host,file=sys.stderr)
        print(f"HOST IN POLL IS {host}", file=sys.stderr)
        vlans = interfaces = virtualIps = ipamData = secondary_ips = []
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 10
        login_exception = ''
        c = 0
        is_login = False
        sw_type = str(host['sw_type']).lower()
        login_exception = ''
        sw_type = sw_type.strip()
        while c < login_tries:
            try:
                device_type = host['sw_type']
                device_type = device_type.split('-')[0] if 'leaf' in device_type else device_type
                device = Netmiko(host=host['ip_address'], username=host['user'], password=host['pwd'],
                                 device_type=device_type, timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}")
                is_login = True
                break
            except Exception as e:
                c += 1
                login_exception = str(e)

        if is_login == False:
            print(f"Falied to login {host['ip_address']}", file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Failed to login to host")
            date = datetime.now()

            # addFailedDevice(host['ip_address'],date,device_type,login_exception,'IPAM')

        if is_login == True:
            print(f"Successfully Logged into device {host['ip_address']}", file=sys.stderr)

            print(f"getting arp table of {host['ip_address']}", file=sys.stderr)
            if sw_type == 'fortinet':
                try:
                    if sw_type == 'fortinet':
                        systemArps = device.send_command('get system arp', use_textfsm=True)
                        if isinstance(systemArps, str):
                            print("Error in show ip arp", file=sys.stderr)
                            raise Exception("Failed to send Command, get system arp" + str(systemArps))
                        for systemArp in systemArps:
                            temp = {}
                            temp['ip_address'] = systemArp['address']
                            temp['interface'] = systemArp['interface']
                            temp['mac_address'] = systemArp['mac']
                            print("temp for showing the arp is:::",temp,file=sys.stderr)
                            pmData.append(temp)

                except Exception as e:
                    print("Failed to send Command, get system arp " + str(e), file=sys.stderr)
                    self.add_to_failed_devices(host['host'], str(e))
            else:

                try:
                    len = device.send_command("terminal length 0")
                    device.send_command(len, use_textfsm=True)
                except Exception as e:
                    print("Failed to send Command, terminal length 0" + str(e))

                try:
                    arps = device.send_command("show ip arp", use_textfsm=True)
                    print("arps are :::::::::::::::::::::::::::::: ",arps,file=sys.stderr)
                    if isinstance(arps, str):
                        print("Error in show ip arp", file=sys.stderr)
                        raise Exception("Failed to send Command, show ip arp" + str(arps))

                    for arp in arps:
                        print("arp is: :::::::::::::::::::::::::::::::: ",arp,file=sys.stderr)
                        mac_address = arp.get("address")
                        print("mac address is:::::::::::::::::",mac_address,file=sys.stderr)
                        ip_address = arp.get("address")
                        print("ip adress is::::::::::::::::",ip_address,file=sys.stderr)
                        dic = {}
                        dic['ip_address'] = arp.get("address")
                        dic['mac_address'] = arp.get("mac")
                        dic['interface'] = ""
                        pmData.append(dic)

                except Exception as e:
                    print("Failed to send Command, show ip arp " + str(e), file=sys.stderr)
                    self.add_to_failed_devices(host['host'], str(e))

                print(f"getting ip interface brief table of {host['ip_address']}", file=sys.stderr)
                try:
                    ips = []
                    if sw_type == "cisco_nxos":
                        ips = device.send_command('show interface',
                                                  textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/cisco_nxos_show_interface.textfsm",
                                                  use_textfsm=True)
                    else:
                        ips = device.send_command('show interface', use_textfsm=True)
                        print("ips are:::::::::::::::::::::",ips,file=sys.stderr)
                    if isinstance(arps, str):
                        print("Error in show ip interface brief", file=sys.stderr)
                        raise Exception("Failed to send Command, show ip interface brief" + str(arps))

                    for ip in ips:
                        print("ip in ips ::::::::::::::::::",ip,file=sys.stderr)
                        dic = {}
                        ips = ip.get("ip_address")
                        if "/" in ips:
                            ips = ips.split('/')
                            if ips:
                                ips = ips[0]
                        dic['ip_address'] = ips
                        dic['interface'] = ip.get("interface")
                        ipData.append(dic)

                    for arp in pmData:
                        print("arp in pmData :::::::::::::::::::::::",arp,file=sys.stderr)
                        for ip in ipData:
                            print("ip in IP data is::::::::::::",ip,file=sys.stderr)
                            if ip['ip_address']:

                                if arp['ip_address'] == ip['ip_address']:
                                    arp['interface'] = ip.get('interface')
                    print(f"Completed Data fetching for host {host['ip_address']}", file=sys.stderr)
                    print(pmData, file=sys.stderr)
                except Exception as e:
                    print("Failed to send Command, show ip arp " + str(e), file=sys.stderr)
                    self.add_to_failed_devices(host['host'], str(e))

            try:
                # Updating IP Data
                print("Populating PM data in Ip Table", file=sys.stderr)
                for record in pmData:
                    print("record in pm data is::::::::::::::::::::",record,file=sys.stderr)
                    print("RECORDDDDDDDDDDDDDDDDD IS ", record, file=sys.stderr)
                    query = f"update ip_table set MAC_ADDRESS='{record['mac_address']}', CONFIGURATION_INTERFACE='{record['interface']}', CONFIGURATION_SWITCH='{host['device_name']}' where IP_ADDRESS='{record['ip_address']}';"
                    try:
                        configs.db.execute(query)
                        configs.db.commit()
                        print(f"Added recorded of PM for ip {arp['ip_address']}")
                    except Exception as e:
                        print("Exception Occured in Executing Database Query", file=sys.stderr)

                    ## Update MAC Hstory
                    tagId = None
                    date = datetime.now()
                    query_string = f"SELECT ASSET_TAG FROM ip_table WHERE IP_ADDRESS='{record['ip_address']}';"
                    result3 = configs.db.execute(query_string)
                    for row in result3:
                        tagId = row[0]

                    query_string = f"SELECT MAC_ADDRESS FROM ip_history_table WHERE IP_ADDRESS='{record['ip_address']}';"
                    result2 = configs.db.execute(query_string)
                    historyMacAddress = ""
                    for row in result2:
                        historyMacAddress = row[0]
                    print(f"HISTORY MAC VARIABLE {historyMacAddress} {record['ip_address']}", file=sys.stderr)
                    if historyMacAddress:
                        if historyMacAddress != record['mac_address']:
                            query_string = f"INSERT INTO ip_history_table (IP_ADDRESS, MAC_ADDRESS, ASSET_TAG,`DATE`) VALUES ('{record['ip_address']}','{record['mac_address']}', '{tagId}','{date}');"
                            try:
                                configs.db.execute(query_string)
                                configs.db.commit()
                                print(f"HISTORY MAC ADDRESS {historyMacAddress} {record['ip_address']}",
                                      file=sys.stderr)
                            except Exception as e:
                                print(f"Exception Occured in Executing Database Query {e}", file=sys.stderr)
                        else:
                            pass

                    else:
                        query_string = f"INSERT INTO ip_history_table (IP_ADDRESS, MAC_ADDRESS, ASSET_TAG,`DATE`) VALUES ('{record['ip_address']}','{record['mac_address']}', '{tagId}','{date}');"
                        try:
                            configs.db.execute(query_string)
                            configs.db.commit()
                            print(f"IN ELSE CONDITION  {record['ip_address']}", file=sys.stderr)
                        except Exception as e:
                            print(f"Exception Occured in Executing Database Query {e}", file=sys.stderr)

            except Exception as e:
                print("Failed to send Command, show interface " + str(e), file=sys.stderr)
                # self.add_to_failed_devices(host['host'], str(e))

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
        puller = IPAMPM()
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
            else:
                sw_type = ''
            if sw_type == 'fortinet':
                sw_type = 'fortinet'

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


'''
puller = IPAMPM()
hosts = []
host={
    "ip_address": "192.168.30.186",
    "user": "nets",
    "pwd": "Nets@123",
    "sw_type": "cisco_ios",
    "time":(datetime.now())
    #"device_name":device["device_name"]
    }
hosts.append(host)

puller.get_inventory_data(hosts)
'''