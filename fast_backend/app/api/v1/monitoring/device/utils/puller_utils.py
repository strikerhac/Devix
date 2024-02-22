import re
import traceback
import sys
from datetime import datetime
import time

from pysnmp.hlapi import *
from influxdb_client.client.write_api import SYNCHRONOUS

from app.core.config import *
from app.api.v1.monitoring.device.utils.alerts_utils import *
from app.api.v1.monitoring.device.utils.ping_parse import *
from app.models.common_models import *

from app.models.monitoring_models import *


#
# Method to create SNMP V1/V2 Object
#
def createSnmpObjectV2(ip, string, port):
    try:
        print(f"{ip}: Creating SNMP V1/V2 Object", file=sys.stderr)
        engin = SnmpEngine()
        community = CommunityData(mpModel=1, communityIndex=ip, communityName=string)
        transport = UdpTransportTarget((ip, port), timeout=5.0, retries=1)
        context = ContextData()

        return [engin, community, transport, context]
    except Exception as e:
        print(f"{ip}: Exception While Creating SNMP V1/V2 Object", file=sys.stderr)
        traceback.print_exc()
        return None


#
# Method to create SNMP V3 Object
#
def createSnmpObjectV3(credentials, ip_address):
    try:
        auth_proc = None
        encryp_proc = None
        if credentials.authentication_method == "MD5":
            auth_proc = usmHMACMD5AuthProtocol
        if credentials.authentication_method == "SHA":
            auth_proc = usmHMACSHAAuthProtocol
        if credentials.authentication_method == "SHA-128":
            auth_proc = usmHMAC128SHA224AuthProtocol
        if credentials.authentication_method == "SHA-256":
            auth_proc = usmHMAC192SHA256AuthProtocol
        if credentials.authentication_method == "SHA-512":
            auth_proc = usmHMAC384SHA512AuthProtocol

        if credentials.encryption_method == "DES":
            encryp_proc = usmDESPrivProtocol
        if credentials.encryption_method == "AES-128" or credentials.encryption_method == "AES":
            encryp_proc = usmAesCfb128Protocol
        if credentials.encryption_method == "AES-192":
            encryp_proc = usmAesCfb192Protocol
        if credentials.encryption_method == "AES-256":
            encryp_proc = usmAesCfb256Protocol

        engin = SnmpEngine()
        # community = CommunityData(mpModel=1,communityIndex=atom.ip_address, communityName= host[13])# snmp community
        community = UsmUserData(
            userName=credentials.username,
            authKey=credentials.password,
            privKey=credentials.encryption_password,
            authProtocol=auth_proc,
            privProtocol=encryp_proc,
        )  # snmp community
        transport = UdpTransportTarget(
            (ip_address, credentials.snmp_port), timeout=5.0, retries=1
        )
        context = ContextData()

        return [engin, community, transport, context]

    except Exception as e:
        print(
            f"{ip_address}: Exception While Creating SNMP V3 Object",
            file=sys.stderr,
        )
        traceback.print_exc()
        return None


#
# Method to Test SNMP V2 Connection
#


def testSnmpConnection(snmp):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        oid = ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)

        error_indication, error_status, error_index, var_binds = next(
            getCmd(engn, community, transport, cnxt, ObjectType(oid))
        )
        # Check if SNMP query was successful
        if error_indication:
            print(f"SNMP query failed: {error_indication}", file=sys.stderr)
        elif error_status:
            print(f"SNMP query failed: {error_status.prettyPrint()}", file=sys.stderr)
        else:
            return True

        return False
    except Exception as e:
        traceback.print_exc()
        return False


def get_oid_data(engn, community, transport, cnxt, oid):
    try:
        print(f"\nSNMP walk started for OID {oid}", file=sys.stderr)

        oid = ObjectType(ObjectIdentity(oid))
        all = []

        for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
            engn, community, transport, cnxt, oid, lexicographicMode=False
        ):
            if errorIndication:
                print(f"error=>{errorIndication}", file=sys.stderr)
                return "NA"

            elif errorStatus:
                print(
                    "%s at %s"
                    % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                    )
                )
                return "NA"
            else:
                for varBind in varBinds:
                    all.append(varBind)
        return all
    except Exception as e:
        print(f"Failed to run SNMP walk: {e}", file=sys.stderr)
        traceback.print_exc()
        return "NA"


def getSnmpData(host, oids):
    try:
        atom, monitoring_device, credentials = host
        print(
            f"\n---------->>>>>>>> {atom.ip_address} : Start <<<<<<<<-----------\n",
            file=sys.stderr,
        )

        status = dict()
        try:
            status["status"], status["response"], status["packets"] = ping(atom.ip_address)
            if status["status"] == "Up":
                status_alert(monitoring_device, "Up")
            else:
                status_alert(monitoring_device, "Down")
        except Exception as e:
            traceback.print_exc()
            print(f"{atom.ip_address}: Error In Ping0", file=sys.stderr)
            status["status"] = "Down"
            status["response"] = "NA"
            try:
                status_alert(monitoring_device, "Down")
            except:
                traceback.print_exc()

        # if status['status'] == 'Down':
        #     return

        snmp = None
        connection = False

        if credentials.category == "v3":
            snmp = createSnmpObjectV3(atom.ip_address, credentials)
            connection = testSnmpConnection(snmp)

        elif credentials.category == "v1/v2":
            snmp = createSnmpObjectV2(
                atom.ip_address, credentials.snmp_read_community, credentials.snmp_port
            )
            connection = testSnmpConnection(snmp)

        else:
            print(f"{atom.ip_address}: Error : SNMP Version Unknown", file=sys.stderr)

        # check snmp credentials
        if connection is False:
            print(f"{atom.ip_address}: Error : Check SNMP Credentials", file=sys.stderr)
            snmp_alert(monitoring_device.monitoring_device_id, False)
            snmp = None

        else:
            print(f"{atom.ip_address}: SNMP Connection Successfull", file=sys.stderr)
            snmp_alert(monitoring_device.monitoring_device_id, True)

        # check if snmp is not set up successfully
        if snmp is None:
            print(f"{atom.ip_address}: Exiting Poll. Failed", file=sys.stderr)
            return None

        device = dict()
        try:
            print(
                f"\n---------->>>>>>>\n{atom.ip_address}: Device Data Extraction/Insertion Started\n",
                file=sys.stderr,
            )

            device = getDeviceData(host, snmp, oids)
            device.update(status)
            dumpDeviceData(atom, device)

        except Exception as e:
            traceback.print_exc()
            print(
                f"{atom.ip_address}: Device Data Extraction/Insertion Failed",
                file=sys.stderr,
            )

        print(
            f"\n{atom.ip_address}: Device Data Extraction/Insertion Complete\n<<<<<---------------\n",
            file=sys.stderr,
        )

        interface = dict()
        try:
            print(
                f"\n---------->>>>>>>\n{atom.ip_address}: Interface Data Extraction/Insertion Started\n",
                file=sys.stderr,
            )

            interface = getInterfaceData(atom.ip_address, snmp, oids)
            if interface is not None:
                dumpInterfaceData(atom, device, interface)

        except Exception as e:
            traceback.print_exc()
            print(
                f"{atom.ip_address}: Interface Data Extraction/Insertion Failed",
                file=sys.stderr,
            )

        print(
            f"\n{atom.ip_address}: Interface Data Extraction/Insertion Complete\n<<<<<---------------\n",
            file=sys.stderr,
        )
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while getting SNMP data",str(e))

def getDeviceData(host, snmp, oids):
    try:
        atom, monitoring_device, credentials = host
        output = dict()

        # Uptime
        output["uptime"] = getUpTime(atom.ip_address, snmp, oids["uptime"])

        # CPU Utilization
        output["cpu"] = getCpuUtilization(atom, snmp, oids["cpu_utilization"])
        try:
            cpu_alert(atom.ip_address, monitoring_device, output["cpu"])
        except:
            traceback.print_exc()

        # Memory Utilization
        output["memory"] = 0.0
        output["memory"] = getMemoryUtilization(atom, snmp, oids)
        try:
            memory_alert(atom.ip_address, monitoring_device, int(output["memory"]))
        except:
            traceback.print_exc()

        # Device Description
        output["device_name"] = getDeviceName(atom.ip_address, snmp, oids["device_name"])

        # Device Description
        output["device_description"] = getDeviceDescription(
            atom.ip_address, snmp, oids["device_description"]
        )

        return output
    except Exception as e:
        traceback.print_exc()
        print("Error OCcured while getting device data",str(e))

def getInterfaceData(ip_address, snmp, oids):
    try:
    
        interfaces = getInterfaceList(ip_address, snmp, oids["interfaces"])
        if interfaces == None:
            return None

        interface_description = getInterfaceList(ip_address, snmp, oids["interface_description"])
        if interface_description == None:
            return None

        interface_status = getInterfaceList(ip_address, snmp, oids["interface_status"])
        if interface_status == None:
            interface_status = dict()
            for key in interfaces.keys():
                interface_status[key] = ["NA"]

        # Get first snapshot
        start_time = datetime.now()
        print(
            f"{ip_address}: Taking 1st Snapshot : {str(start_time)}", file=sys.stderr
        )
        download_counter_start = getInterfaceList(ip_address, snmp, oids["download"])
        if download_counter_start == None:
            print(f"{ip_address}: Error in Interface Download", file=sys.stderr)

        upload_counter_start = getInterfaceList(ip_address, snmp, oids["upload"])
        if upload_counter_start == None:
            print(f"{ip_address}: Error in Interface Upload", file=sys.stderr)

        print(f"{ip_address}: Waiting For 2nd Snapshot", file=sys.stderr)
        try:
            time.sleep(10)
        except Exception as e:
            traceback.print_exc()
            print(f"{ip_address}: Error in Waiting", file=sys.stderr)

        end_time = datetime.now()
        print(f"{ip_address}: Taking 2nd Snapshot : {str(end_time)}", file=sys.stderr)

        download_counter_end = getInterfaceList(ip_address, snmp, oids["download"])
        if download_counter_end == None:
            print(f"{ip_address}: Error in Interface Download", file=sys.stderr)

        upload_counter_end = getInterfaceList(ip_address, snmp, oids["upload"])
        if upload_counter_end == None:
            print(f"{ip_address}: Error in Interface Upload", file=sys.stderr)

        time_difference = (end_time - start_time).total_seconds()
        print(
            f"{ip_address}: Time Difference : {str(time_difference)}", file=sys.stderr
        )

        interfaceList = dict()
        for key in interfaces.keys():
            description = "NA"
            status = "NA"
            download = 0.0
            upload = 0.0

            if key in interface_description.keys():
                description = interface_description[key][0]

            if key in interface_status.keys():
                if interface_status[key][0] == "1":
                    status = "Up"
                else:
                    status = "Down"

            try:
                if download_counter_start is not None and download_counter_end is not None:
                    if (
                        key in download_counter_start.keys()
                        and key in download_counter_end.keys()
                    ):
                        download = int(download_counter_end[key][0]) - int(
                            download_counter_start[key][0]
                        )
                        if download < 0:
                            print(
                                f"{ip_address}: Error In Download Difference : {interfaces[key]} : {download}",
                                file=sys.stderr,
                            )
                        else:
                            download = (download * 8) / time_difference  # bps
                            download = download / 1000  # Kbps
                            download = download / 1000  # Mps
                            download = round(download, 2)

            except Exception as e:
                traceback.print_exc()
                print(
                    f"{ip_address}: Error In Download Calculation : {interfaces[key]}",
                    file=sys.stderr,
                )

            try:
                if upload_counter_start is not None and upload_counter_end is not None:
                    if (
                        key in upload_counter_start.keys()
                        and key in upload_counter_end.keys()
                    ):
                        upload = int(upload_counter_end[key][0]) - int(
                            upload_counter_start[key][0]
                        )
                        if upload < 0:
                            print(
                                f"{ip_address}: Error In Upload Difference : {interfaces[key]} : {upload}",
                                file=sys.stderr,
                            )
                        else:
                            upload = (upload * 8) / time_difference  # bps
                            upload = upload / 1000  # Kbps
                            upload = upload / 1000  # Mbps
                            upload = round(upload, 2)

            except Exception as e:
                traceback.print_exc()
                print(
                    f"{ip_address}: Error In Upload Calculation : {interfaces[key]}",
                    file=sys.stderr,
                )

            interfaceObj = {
                "name": interfaces[key][0],
                "status": status,
                "description": description,
                "download": download,
                "upload": upload,
            }

            interfaceList[key] = interfaceObj

        return interfaceList
    except Exception as e:
        traceback.print_exc()
        print("Error OCcured while getting interface data ",str(e))

def getInterfaceList(ip_address, snmp, oid):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        interfaces = None
        try:
            value = get_oid_data(engn, community, transport, cnxt, oid)
            interfaces = parse_snmp_output(value)
        except:
            print(f"{ip_address}: Error in Interfaces", file=sys.stderr)
            traceback.print_exc()
            return None

        print(f"{ip_address}: Interfaces : {interfaces}", file=sys.stderr)
        return interfaces
    except Exception as e:
        traceback.print_exc()
        print("Error OCcured while getting interface list",str(e))


def getUpTime(ip_address, snmp, oid):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        uptime = 0
        try:
            value = get_oid_data(engn, community, transport, cnxt, oid)
            uptime = int(parse_general(value))
            uptime = convert_time(uptime)
        except:
            print(f"{ip_address}: Error in Up Time", file=sys.stderr)
            traceback.print_exc()
            uptime = 0

        print(f"{ip_address}: Up Time : {uptime}", file=sys.stderr)
        return uptime
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while getting up time",str(e))

def getCpuUtilization(atom, snmp, oid):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        cpu = 0
        try:
            value = None
            cpu_list = {}
            if atom.device_type.lower() == "cisco_ios_xr":
                if len(oid) != 2:
                    print(
                        f"{atom.ip_address}: IOS-XR - Error in CPU - Invalid SNMP OID & Index",
                        file=sys.stderr,
                    )
                    return "NA"

                value = get_oid_data(engn, community, transport, cnxt, oid[0])

                if value is None or value == "NA":
                    value = "NA"
                else:
                    cpu_list = parse_snmp_output(value)

                    if oid[1] in cpu_list.keys():
                        cpu_list = {oid[1]: cpu_list[oid[1]]}
                    else:
                        print(
                            f"{atom.ip_address}: IOS-XR - Error in CPU - SNMP Index Does Nor Match",
                            file=sys.stderr,
                        )
            else:
                value = get_oid_data(engn, community, transport, cnxt, oid)
                if value is None or value == "NA":
                    value = "NA"
                else:
                    cpu_list = parse_snmp_output(value)

            if value == "NA":
                cpu = "NA"
            else:
                for key in cpu_list.keys():
                    cpu += int(cpu_list[key][0])
                if cpu > 0:
                    cpu = int(cpu / (len(cpu_list.keys())))
        except:
            print(f"{atom.ip_address}: Error in CPU", file=sys.stderr)
            traceback.print_exc()
            cpu = "NA"

        print(f"{atom.ip_address}: CPU Utilization : {cpu}", file=sys.stderr)
        return cpu
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while getting cpu utilixation",str(e))

def parseMemory(memory_data):
    try:
        memory = 0.0
        memoryList = parse_snmp_output(memory_data)
        for key in memoryList.keys():
            memory += float(memoryList[key][0])

        return memory, len(memoryList.keys())
    except Exception as e:
        traceback.print_exc()
        print("Error in parse memory",str(e))

# Method to get memory utilization by extracting used and free memory
def getMemoryUtilization(atom, snmp, oids):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        memory_util = 0.0
        if atom.device_type.lower() == "fortinet" or atom.device_type.lower() == "juniper":
            if "memory" in oids.keys():
                try:
                    memory = get_oid_data(engn, community, transport, cnxt, oids["memory"])
                    memory_util, count = parseMemory(memory)

                    if memory_util > 0.0 and count != 0:
                        memory_util = memory_util / count

                except Exception as e:
                    print(
                        f"{atom.ip_address}: Error in Memory Utilization", file=sys.stderr
                    )
                    traceback.print_exc()
            else:
                print(
                    f"{atom.ip_address}: Error : Memory Percent Utilization OID Not Given",
                    file=sys.stderr,
                )

        elif (
            atom.device_type.lower() == "cisco_ios"
            or atom.device_type.lower() == "cisco_ios_xe"
            or atom.device_type.lower() == "cisco_ios_xr"
            or atom.device_type.lower() == "cisco_nxos"
            or atom.device_type.lower() == "cisco_apic"
        ):
            try:
                if "memory_used" in oids.keys() and "memory_free" in oids.keys():
                    memory_used = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_used"]
                    )

                    memory_used = parseMemory(memory_used)[0]
                    print(f"{atom.ip_address}: Memory Used: {memory_used}", file=sys.stderr)

                    memory_free = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_free"]
                    )
                    memory_free = parseMemory(memory_free)[0]
                    print(f"{atom.ip_address}: Memory Free: {memory_free}", file=sys.stderr)

                    memory_util = (memory_used * 100) / (memory_used + memory_free)
                else:
                    print(
                        f"{atom.ip_address}: Error : Memory Used Or Memory Free OID Not Given",
                        file=sys.stderr,
                    )
            except Exception as e:
                print(f"{atom.ip_address}: Error in Memory Utilization", file=sys.stderr)
                traceback.print_exc()

        elif atom.device_type.lower() == "window" or atom.device_type.lower() == "paloalto":
            try:
                if "memory_used" in oids.keys() and "memory_total" in oids.keys():
                    memory_used = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_used"]
                    )
                    memory_used = parseMemory(memory_used)[0]
                    print(f"{atom.ip_address}: Memory Used: {memory_used}", file=sys.stderr)

                    memory_total = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_total"]
                    )
                    memory_total = parseMemory(memory_total)[0]
                    print(
                        f"{atom.ip_address}: Memory Total: {memory_total}", file=sys.stderr
                    )

                    memory_util = (memory_used * 100) / (memory_total)
                else:
                    print(
                        f"{atom.ip_address}: Error : Memory Used Or Memory Total OID Not Given",
                        file=sys.stderr,
                    )

            except Exception as e:
                print(f"{atom.ip_address}: Error in Memory Utilization", file=sys.stderr)
                traceback.print_exc()

        elif atom.device_type.lower() == "extream" or atom.device_type.lower() == "linux":
            try:
                if "memory_free" in oids.keys() and "memory_total" in oids.keys():
                    memory_free = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_free"]
                    )
                    memory_free = float(parse_general(memory_free))
                    print(f"{atom.ip_address}: Memory Free: {memory_free}", file=sys.stderr)

                    memory_total = get_oid_data(
                        engn, community, transport, cnxt, oids["memory_total"]
                    )
                    memory_total = int(parse_general(memory_total))
                    print(
                        f"{atom.ip_address}: Memory Total: {memory_total}", file=sys.stderr
                    )

                    memory_util = (memory_total - memory_free * 100) / (memory_total)
                else:
                    print(
                        f"{atom.ip_address}: Error : Memory Used Or Memory Total OID Not Given",
                        file=sys.stderr,
                    )

            except Exception as e:
                print(f"{atom.ip_address}: Error in Memory Utilization", file=sys.stderr)
                traceback.print_exc()

        memory_util = round(memory_util, 2)
        print(f"{atom.ip_address}: Memory Utilization : {memory_util}", file=sys.stderr)
        return memory_util
    except Exception as e:
        traceback.print_exc()
        print("Error Occured whilecpu utilixation",str(e))

def getDeviceDescription(ip_address, snmp, oid):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        device = "NA"
        try:
            value = get_oid_data(engn, community, transport, cnxt, oid)
            device = parse_general(value)
        except:
            print(f"{ip_address}: Error in Device Description", file=sys.stderr)
            traceback.print_exc()

        print(f"{ip_address}: Device Description : {device}", file=sys.stderr)
        return device
    except Exception as e:
        traceback.print_exc()
        print("Error while device description",str(e))

def getDeviceName(ip_address, snmp, oid):
    try:
        engn = snmp[0]
        community = snmp[1]
        transport = snmp[2]
        cnxt = snmp[3]

        device = "NA"
        try:
            value = get_oid_data(engn, community, transport, cnxt, oid)
            device = parse_general(value)
        except:
            print(f"{ip_address}: Error in Device Name", file=sys.stderr)
            traceback.print_exc()

        print(f"{ip_address}: Device Name : {device}", file=sys.stderr)
        return device
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while getting device name",str(e))

def parse_snmp_output(varbinds):
    try:
        intefaces_val = dict()
        for varbind in varbinds:
            out = re.search(r"\d* .*", str(varbind)).group()
            value = out.split("=")
            intefaces_val[value[0].strip()] = [value[1].strip()]

        return intefaces_val
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while getting parse snmp output",str(e))

def parse_general(varbinds):
    try:
        for varBind in varbinds:
            res = " = ".join([x.prettyPrint() for x in varBind])
            if "No Such Instance" not in res:
                result = res.split("=")[1].strip()
                return result
    except Exception as e:
        traceback.print_exc()
        print("error occured while parse genenral",str(e))

def dumpDeviceData(atom, output):
    try:

        print(f"{atom.ip_address}: Dumping Device Data", file=sys.stderr)
        write_api = configs.client.write_api(write_options=SYNCHRONOUS)
        print("write API in device dump data is:::::::::::",write_api,file=sys.stderr)
        dictionary = [
            {
                "measurement": "Devices",
                "tags": {
                    "DEVICE_NAME": output["device_name"],
                    "STATUS": output["status"],
                    "IP_ADDRESS": atom.ip_address,
                    "FUNCTION": atom.function,
                    "VENDOR": atom.vendor,
                    "DEVICE_TYPE": atom.device_type,
                },
                "time": datetime.now(),
                "fields": {
                    "INTERFACES": 0,
                    "DISCOVERED_TIME": str(datetime.now()),
                    "DEVICE_DESCRIPTION": output["device_description"],
                    "CPU": output["cpu"],
                    "Memory": output["memory"],
                    "PACKETS_LOSS": output["packets"],
                    "Response": output["response"],
                    "Uptime": output["uptime"],
                    "Date": str(datetime.now()),
                },
            }
        ]
        if dictionary[0]["fields"]["CPU"] == "NA":
            dictionary[0]["fields"]["CPU"] = 0

        if dictionary[0]["fields"]["Memory"] == "NA":
            dictionary[0]["fields"]["Memory"] = 0.0

        try:
            print("dictionary in dump device datais:::::::",dictionary,file=sys.stderr)
            write_api.write(org='monetx',bucket="monitoring", record=dictionary)
            print("writting into influxdb for dump device data",file=sys.stderr)
        except Exception as e:
            traceback.print_exc()
            print(
                f"{atom.ip_address}: Influx Connection Issue For Device: {e}",
                file=sys.stderr,
            )
    except Exception as e:
        traceback.print_exc()
        print("Error Occured while dumpDeviceData",str(e))

def dumpInterfaceData(atom, output, interfaces):
    try:
        print("atom in dump interface is::::::::::;",atom,file=sys.stderr)
        print("output is::::::::::",output,file=sys.stderr)
        print("interfaces in dump insertaces are:::",interfaces,file=sys.stderr)

        write_api = configs.client.write_api(write_options=SYNCHRONOUS)

        if len(interfaces.items()) > 0:
            for k in interfaces.keys():
                dictionary1 = [
                    {
                        "measurement": "Interfaces",
                        "tags": {
                            "DEVICE_NAME": output["device_name"],
                            "STATUS": output["status"],
                            "IP_ADDRESS": atom.ip_address,
                            "FUNCTION": atom.function,
                            "VENDOR": atom.vendor,
                            "DEVICE_TYPE": atom.device_type,
                        },
                        "time": datetime.now(),
                        "fields": {
                            "Interface_Name": interfaces[k]["name"],
                            "Status": interfaces[k]["status"],
                            "Download": float(interfaces[k]["download"]),
                            "Upload": float(interfaces[k]["upload"]),
                            "Interface Description": interfaces[k]["description"],
                            "Date": str(datetime.now()),
                        },
                    }
                ]
                print("dictionary 1 for the interfaces are:::",dictionary1,file=sys.stderr)

                try:
                    print("writing in to inlfux for interfaces",file=sys.stderr)
                    write_api.write(org='monetx',bucket="monitoring", record=dictionary1)
                except Exception as e:
                    print(
                        f"{atom.ip_address}: Influx Connection Issue For Interface: {interfaces[k]['name']}: {e}",
                        file=sys.stderr,
                    )
    except Exception as e:
        traceback.print_exc()
        print("error occured while dumping devices interface data")
#
#
#
#
#
#
#
#


# def InsertData(obj):
#     # add data to db
#     try:
#         db.session.add(obj)
#         db.session.commit()

#     except Exception as e:
#         db.session.rollback()
#         print(f"Something else went wrong in Database Insertion {e}", file=sys.stderr)

#     return True


# def UpdateData(obj):
#     # add data to db
#     # print(obj, file=sys.stderr)
#     try:
#         # db.session.flush()

#         db.session.merge(obj)
#         db.session.commit()

#     except Exception as e:
#         db.session.rollback()
#         print(f"Something else went wrong during Database Update {e}", file=sys.stderr)

#     return True


def addFailedDevice(ip, date, device_type, failure_reason, module):
    try:
        failed = FailedDevicesTable()
        failed.ip_address = ip
        failed.date = date
        failed.device_type = device_type
        failed.failure_reason = failure_reason
        failed.module = module
        if (
            FailedDevicesTable.query.with_entities(
                FailedDevicesTable.ip_address
            ).filter_by(ip_address=ip)
            is not None
        ):
            print("Updated " + ip, file=sys.stderr)
            UpdateDBData(failed)
        else:
            print("Inserted ", ip, file=sys.stderr)
            InsertDBData(failed)
    except Exception as e:
        traceback.print_exc()
        print("error occured while getting failed devies",str(e))

def convert_time(seconds):
    try:
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60

        return "%d:%02d:%02d" % (hour, minutes, seconds)
    except Exception as e:
        traceback.print_exc()
        print("error occured while convert time",str(e))

def general(varbinds):
    try:
        for varBind in varbinds:
            res = " = ".join([x.prettyPrint() for x in varBind])
            if "No Such Instance" not in res:
                result = res.split("=")[1].strip()

                return result
    except Exception as e:
        traceback.print_exc()

# def date_diff(datedb, datenow):
#     NUM_SECONDS_IN_A_MIN = 60

#     seconds = (datenow-datedb).total_seconds()
#     minutes = seconds / NUM_SECONDS_IN_A_MIN
#     print("//////////////difference in seconds:", seconds, type(seconds),
#           "\n///////////difference in minutes:", minutes, type(minutes), file=sys.stderr)
#     return minutes


# thrushold_list = [30, 60, 120, 300, 1440]


# def alert_check(ip, value, category, func):
#     if category == 'memory' or category == 'cpu':
#         try:
#             if value == "None" or value == "NA" or value == None:
#                 # start_time_query = f"select start_date from alerts_table where IP_ADDRESS='{ip}' and  (ALERT_TYPE='critical' and category='{category}') and ALERT_STATUS='Open';"
#                 # start_time = db.session.execute(start_time_query)
#                 # print("printing start time of alert",start_time,file=sys.stderr)
#                 queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and (ALERT_TYPE='critical' and ALERT_STATUS='Open') and category='{category}';"
#                 result = db.session.execute(queryString)
#                 check_ip = ""
#                 for row in result:
#                     check_ip = row[0]
#                     if check_ip != "" or check_ip != None:
#                         time = date_diff(row[3], datetime.now())

#                         if int(time) > 30:
#                             sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and (ALERT_TYPE='critical' and ALERT_STATUS='Open') and category='{category}';"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                             des = f"Not Providing Value of {category.upper()} from the Last {int(time)} Minutes"
#                             sqlquery1 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{row[3]}','{func}');"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                 if check_ip == "":
#                     des = f"Not Providing Value of {category.upper()}"
#                     sqlquery1 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{datetime.now()}','{func}');"
#                     db.session.execute(sqlquery1)
#                     db.session.commit()
#                 sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Critical' where ip_address='{ip}';"
#                 db.session.execute(sqlquery1)
#                 db.session.commit()

#             elif float(value) < 50:
#                 queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and (ALERT_STATUS='Open' and category='{category}');"
#                 result = db.session.execute(queryString)
#                 check_ip = ""
#                 for row in result:
#                     check_ip = row[0]
#                     if check_ip != "":
#                         sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and category='{category}';"
#                         db.session.execute(sqlquery1)
#                         db.session.commit()
#                         des = f"Device {category.upper()} Utilization is Clear Now."
#                         sqlquery2 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','clear','{category}','Close','no','{datetime.now()}','{row[3]}','{func}');"
#                         db.session.execute(sqlquery2)
#                         db.session.commit()
#                 sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Clear' where ip_address='{ip}';"
#                 db.session.execute(sqlquery1)
#                 db.session.commit()

#             if float(value) > 50 and float(value) < 70:
#                 # start_time_query = f"select min(start_date) from alerts_table where IP_ADDRESS='{ip}' and  (ALERT_TYPE='informational' and category='{category}');"
#                 # start_time = db.session.execute(start_time_query)
#                 # print("printing start time of alert",start_time,file=sys.stderr)

#                 queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and (ALERT_TYPE='informational'and ALERT_STATUS='Open') and category='{category}';"
#                 result = db.session.execute(queryString)
#                 check_ip = ""
#                 for row in result:
#                     check_ip = row[0]
#                     if check_ip != "":
#                         date_db = row[2]
#                         date_now = datetime.now()
#                         time = date_diff(row[3], datetime.now())
#                         if int(time) > 30:
#                             sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and (ALERT_TYPE='informational' and ALERT_STATUS='Open' and category='{category}');"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                             des = f"Utilizing {value}% of {category.upper()} from the Last {int(time)} Minutes"
#                             sqlquery1 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{row[3]}','{func}');"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                 if check_ip == "":
#                     des = f"Utilizing {value}% of {category.upper()}"
#                     sqlquery = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','informational','{category}','Open','no','{datetime.now()}','{datetime.now()}','{func}');"
#                     db.session.execute(sqlquery)
#                     db.session.commit()
#                 sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Attention' where ip_address='{ip}';"
#                 db.session.execute(sqlquery1)
#                 db.session.commit()

#             if float(value) > 70:
#                 # start_time_query = f"select min(start_date) from alerts_table where IP_ADDRESS='{ip}' and  (ALERT_TYPE='critical' and category='{category}') and ALERT_STATUS='Open';"
#                 # start_time = db.session.execute(start_time_query)
#                 # print("printing start time of alert",start_time,file=sys.stderr)
#                 queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and ( ALERT_TYPE='critical'and ALERT_STATUS='Open' ) and category='{category}';"
#                 result = db.session.execute(queryString)
#                 check_ip = ""
#                 for row in result:
#                     check_ip = row[0]
#                     if check_ip != "":
#                         date_db = row[2]
#                         date_now = datetime.now()
#                         time = date_diff(row[3], datetime.now())
#                         if int(time) > 30:
#                             sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and (ALERT_TYPE='critical' and ALERT_STATUS='Open' and category='{category}');"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                             des = f"Utilizing {value}% of {category.upper()} from the Last {int(time)} Minutes"
#                             sqlquery1 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{row[3]}','{func}');"
#                             db.session.execute(sqlquery1)
#                             db.session.commit()
#                 if check_ip == "":

#                     des = f"utilizing {value}% of {category}"
#                     sqlquery = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{datetime.now()}','{func}');"
#                     db.session.execute(sqlquery)
#                     db.session.commit()
#                 sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Critical' where ip_address='{ip}';"
#                 db.session.execute(sqlquery1)
#                 db.session.commit()

#         except Exception as e:
#             print("/////Printing exception in alerts/////",
#                   str(e), file=sys.stderr)
#             traceback.print_exc()

#     if category == 'device_down':
#         # start_time_query = f"select min(start_date) from alerts_table where IP_ADDRESS='{ip}' and  (ALERT_TYPE='critical' and category='{category}') and ALERT_STATUS='Open';"
#         # start_time = db.session.execute(start_time_query)
#         # print("printing start time of alert",start_time,file=sys.stderr)
#         queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and (ALERT_TYPE='device_down'and ALERT_STATUS='Open') and category='{category}';"
#         result = db.session.execute(queryString)
#         check_ip = ""
#         for row in result:
#             check_ip = row[0]
#             if check_ip != "":
#                 date_db = row[2]
#                 date_now = datetime.now()
#                 time = date_diff(row[3], datetime.now())
#                 if int(time) > 30:
#                     sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and (ALERT_TYPE='critical' and ALERT_STATUS='Open' and category='{category}');"
#                     db.session.execute(sqlquery1)
#                     db.session.commit()
#                     des = f"Device is Offline from the Last {int(time)} Minutes"
#                     sqlquery1 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','critical','{category}','Open','no','{datetime.now()}','{row[3]}','{func}');"
#                     db.session.execute(sqlquery1)
#                     db.session.commit()
#         if check_ip == "":

#             des = f"Device is Offline"
#             sqlquery = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','device_down','{category}','Open','no','{datetime.now()}','{datetime.now()}','{func}');"
#             db.session.execute(sqlquery)
#             db.session.commit()
#         sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Device Down' where ip_address='{ip}';"
#         db.session.execute(sqlquery1)
#         db.session.commit()

#     if category == 'device_up':
#         queryString = f"select IP_ADDRESS,ALERT_TYPE,date,start_date from alerts_table where IP_ADDRESS='{ip}' and (ALERT_STATUS='Open' and category='device_down');"
#         result = db.session.execute(queryString)
#         check_ip = ""
#         for row in result:
#             check_ip = row[0]
#             if check_ip != "":
#                 sqlquery1 = f"update alerts_table set ALERT_STATUS = 'Close' where IP_ADDRESS='{ip}' and category='device_down';"
#                 db.session.execute(sqlquery1)
#                 db.session.commit()
#                 des = f"Device is Online now."
#                 sqlquery2 = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`CATEGORY`,`ALERT_STATUS`,`MAIL_STATUS`,`DATE`,`START_DATE`,`FUNCTION`) values ('{ip}','{des}','clear','{category}','Close','no','{datetime.now()}','{row[3]}','{func}');"
#                 db.session.execute(sqlquery2)
#                 db.session.commit()

#         sqlquery1 = f"update monitoring_devices_table set `DEVICE_HEATMAP`='Clear' where ip_address='{ip}';"
#         db.session.execute(sqlquery1)
#         db.session.commit()
