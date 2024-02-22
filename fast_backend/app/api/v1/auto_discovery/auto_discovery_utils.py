import re
import sys
import traceback
from datetime import datetime
import paramiko
from app.models.auto_discovery_models import *
from app.utils.db_utils import *
from app.api.v1.auto_discovery import auto_discover
from app.models.atom_models import *

def validate_subnet(subnet):
    subnet_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$'

    # Use the re.match function to check if the input matches the pattern
    if re.match(subnet_pattern, subnet):
        return True
    else:
        return False


def check_network_id(network_obj):
    network_exist = (configs.db.query(AutoDiscoveryNetworkTable)
                     .filter(AutoDiscoveryNetworkTable.network_id == network_obj['network_id'])
                     .first())

    return network_exist, 200


def check_network_name(network_obj):
    network_obj['network_name'] = network_obj['network_name'].strip()
    if network_obj['network_name'] == "":
        return f"Network Name Can Not Be Empty", 400

    network_exist = configs.db.query(AutoDiscoveryNetworkTable).filter(
        AutoDiscoveryNetworkTable.network_name == network_obj['network_name']).first()

    return network_exist, 200


def check_subnet(network_obj):
    network_obj['subnet'] = network_obj['subnet'].strip()
    if network_obj['subnet'] == "":
        return f"{network_obj['network_name']} : Subnet Can Not Be Empty", 400

    if validate_subnet(network_obj['subnet']) is False:
        return f"{network_obj['subnet']} : Subnet Pattern Is Not Valid", 400

    subnet_exist = configs.db.query(AutoDiscoveryNetworkTable).filter(
        AutoDiscoveryNetworkTable.subnet == network_obj['subnet']).first()

    return subnet_exist, 200


def add_network_util(network_obj, update):
    try:
        data = {}
        scan_status_list = ['Active','In Active']
        network, status = check_network_name(network_obj)

        if status != 200:
            return network, status

        subnet, status = check_subnet(network_obj)
        if status != 200:
            return subnet, status

        exist = False
        if network is not None:
            exist = True
            if not update:
                return f"{network_obj['network_name']} : Network Name Already Assigned", 400

            if subnet is not None:
                if network.subnet != subnet.subnet:
                    return f"{network_obj['network_name']} : Subnet Already Exists - {network_obj['subnet']}", 400
        else:
            if subnet is not None:
                return f"{network_obj['network_name']} : Subnet Already Exists - {network_obj['subnet']}", 400

            network = AutoDiscoveryNetworkTable()
            network.network_name = network_obj['network_name']

        network.subnet = network_obj['subnet']

        if network_obj['scan_status'] not in scan_status_list:
            return f"{network_obj['scan_status'] : Is Unknown} ", 400

        if network_obj['scan_status'] is None:
            network_obj['scan_status'] = "InActive"
        elif str(network_obj['scan_status']).lower() == 'inactive':
            network_obj['scan_status'] = "InActive"
        else:
            network_obj['scan_status'] = "Active"

        network.scan_status = network_obj['scan_status']

        if network_obj['excluded_ip_range'] is None:
            network.excluded_ip_range = ""
        elif network_obj['excluded_ip_range'].strip() == "":
            network.excluded_ip_range = ""
        else:
            network.excluded_ip_range = network_obj['excluded_ip_range'].strip()

        if exist:
            if UpdateDBData(network) == 200:
                data_dict = {
                    "network_id": network.network_id,
                    "network_name": network.network_name,
                    "scan_status": network.scan_status,
                    "excluded_ip_range": network.excluded_ip_range,
                    "no_of_devices": network.no_of_devices,
                    "subnet": network.subnet
                }
                msg = f"{network_obj['network_name']} : Network Updated Successfully"
                data['data'] = data_dict
                data['message'] = msg
                status = 200
            else:

                msg = f"{network_obj['network_name']} : Error While Updating Network"
                status = 500
        else:
            if InsertDBData(network) == 200:
                data_dict = {
                    "network_id": network.network_id,
                    "network_name": network.network_name,
                    "scan_status": network.scan_status,
                    "excluded_ip_range": network.excluded_ip_range,
                    "no_of_devices":network.no_of_devices,
                    "subnet":network.subnet
                }
                msg = f"{network_obj['network_name']} : Network Inserted Successfully"
                data['data'] = data_dict
                data['message'] = msg
                status = 200
            else:
                msg = f"{network_obj['network_name']} : Error While Inserting Network"
                status = 500

        print(msg, file=sys.stderr)
        return data, status

    except Exception:
        traceback.print_exc()
        return "Server Error While Adding Discovery Network", 500


def edit_network_util(network_obj):
    try:
        data = {}

        network, status = check_network_id(network_obj)

        network_name, status = check_network_name(network_obj)
        if status != 200:
            return network_name, status

        subnet, status = check_subnet(network_obj)
        if status != 200:
            return subnet, status

        if network is not None:
            if network_name is not None:
                if network.network_id != network_name.network_id:
                    return f"{network_obj['network_name']} : Network Name Already Assigned", 400

            if subnet is not None:
                if network.subnet != subnet.subnet:
                    return f"{network_obj['network_name']} : Subnet Already Exists - {network_obj['subnet']}", 400
        else:
            return f"Network Not Found", 400

        network.network_name = network_obj['network_name']
        network.subnet = network_obj['subnet']

        if network_obj['scan_status'] is None:
            network_obj['scan_status'] = "In Active"
        elif network_obj['scan_status'] == 'In Active':
            network_obj['scan_status'] = "In Active"
        else:
            network_obj['scan_status'] = "Active"

        network.scan_status = network_obj['scan_status']

        if network_obj['excluded_ip_range'] is None:
            network.excluded_ip_range = "No Exclusion"
        elif network_obj['excluded_ip_range'].strip() == "":
            network.excluded_ip_range = "No Exclusion"
        else:
            network.excluded_ip_range = network_obj['excluded_ip_range'].strip()

        if UpdateDBData(network) == 200:
            data_dict = {
                "network_id": network.network_id,
                "network_name": network.network_name,
                "scan_status": network.scan_status,
                "excluded_ip_range": network.excluded_ip_range,
                "no_of_devices":network.no_of_devices,
                "subnet":network.subnet
            }
            msg = f"{network_obj['network_name']} : Network Updated Successfully"
            data['data'] = data_dict
            data['message'] = msg
            status = 200
        else:
            msg = f"{network_obj['network_name']} : Error While Updating Network"
            status = 500

        print(msg, file=sys.stderr)
        return data, status

    except Exception:
        traceback.print_exc()
        return "Server Error While Updating Discovery Network", 500


def get_discovery_data_util(subnet, function):
    obj_list = []
    try:
        print("subnet in get discovery data util is:::::::::::",file=sys.stderr)
        if str(subnet).lower() != "all":
            if function is None:
                results = configs.db.query(AutoDiscoveryTable).filter(
                    AutoDiscoveryTable.subnet == subnet).all()
                print("result is::::::::::::::::::::::auto discovery table is",results,file=sys.stderr)
            else:
                results = configs.db.query(AutoDiscoveryTable).filter(
                    AutoDiscoveryTable.subnet == subnet and AutoDiscoveryTable.function == function
                ).all()
                print("result is::::::::::::::::::",results,file=sys.stderr)
        else:
            if function is None:
                results = configs.db.query(AutoDiscoveryTable).all()
                print("result is:::::::::::::::::::::",results,file=sys.stderr)
            else:
                results = configs.db.query(AutoDiscoveryTable).filter(
                    AutoDiscoveryTable.function == function).all()

        for data in results:
            print("data is:::::::::::::::::::::",data,file=sys.stderr)
            obj_list.append(data.as_dict())

        return obj_list, 200

    except Exception:
        traceback.print_exc()
        return "Server Error While Fetching Discovery Data", 500



def CheckSSHConnection(ip_address, username, password):
    response = 'False'
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip_address, 22, username=username, password=password)
        print(f"Successfully connected to {ip_address}:{22} via SSH.")
        client.close()
        response = 'True'
        return response
    except paramiko.AuthenticationException:
        print(
            f"Failed to connect to {ip_address}:{22} via SSH. Authentication failed.")
        response = 'False'
        return response
    except paramiko.SSHException:
        print(
            f"Failed to connect to {ip_address}:{22} via SSH. Connection failed.")
        response = 'False'
        return response
    except Exception as e:
        print(f"Failed to connect to {ip_address}:{22} via SSH. {str(e)}")
        response = 'False'
        return response


def CheckSSHStatus():
    try:
        data =False
        ipList = []
        query_string = f"select IP_ADDRESS from auto_discovery_table;"
        result = configs.db.execute(query_string)
        print("result for query string on ip address is::::::",result,file=sys.stderr)
        for row in result:
            print("row is::::::::",row[0],file=sys.stderr)
            ipList.append(row[0])
        for ip in ipList:
            print("ip is:::::::::::",ip,file=sys.stderr)
        # query_string = f"select username,password from password_group_table;"
        # result = configs.db.execute(query_string)
        username = ''
        password = ''
        passwords = configs.db.query(PasswordGroupTable).all()
        for password in passwords:
            username = password.username
            password = password.password
        print("Result is:::::::::::::::::",result,file=sys.stderr)


        objList = []
        for row in result:
            objDict = {}
            username = username
            password = password
            objDict['username'] = username
            objDict['password'] = password
            objList.append(objDict)
        for dict in objList:
            for ip in ipList:

                status = CheckSSHConnection(ip, dict['username'], dict['password'])
                print("status is::::::::::::::::::::::::",status,file=sys.stderr)
                print(f"SSH STATUS is {status}", file=sys.stderr)
                queryString1 = f"update auto_discovery_table set SSH_STATUS='{status}' where IP_ADDRESS='{ip}' or SSH_STATUS!='True';"
                configs.db.execute(queryString1)
                configs.db.commit()
                print(f"SSH STATUS SUCCESSFULLY UPDATED FOR {ip}", file=sys.stderr)
                if status ==True:
                    data =True
        return data
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return data


def CheckSNMPCredentials():
    try:
        data = False
        # Fetch enabled SNMP statuses using ORM
        enabled_snmp_devices = configs.db.query(AutoDiscoveryTable).filter_by(snmp_status='Enabled').all()
        print("Enabled SNMP devices are:::::::::::::",enabled_snmp_devices,file=sys.stderr)
        # Fetch SNMP v1/v2 credentials using ORM
        v1_v2_credentials = configs.db.query(SNMP_CREDENTIALS_TABLE).filter_by(category='v1/v2').all()
        print("v1________v2___________credentials are:::::::::::",v1_v2_credentials,file=sys.stderr)
        # Fetch SNMP v3 credentials using ORM
        v3_credentials = configs.db.query(SNMP_CREDENTIALS_TABLE).filter_by(category='v3').all()
        print("v3 credential are::::::::::::::::",v3_credentials,file=sys.stderr)
        v2_list = [cred.snmp_read_community for cred in v1_v2_credentials]
        v3_list = []
        for cred in v3_credentials:
            print("credeentials are:::::::::::::::::::::",cred,file=sys.stderr)
            snmp_obj = {
                'username': cred.username,
                'port': cred.snmp_port,
                'authentication_protocol': cred.authentication_method,
                'authentication_password': cred.password,
                'encryption_protocol': cred.encryption_method,
                'encryption_password': cred.encryption_password
            }
            v3_list.append(snmp_obj)

        for device in enabled_snmp_devices:
            test_result = auto_discover.test_snmp_v2_credentials(device.ip_address, v2_list)
            print("test_result is::::::::::::::::",test_result,file=sys.stderr)
            if test_result is None:
                # No v2 credentials matched, try v3
                test_result = auto_discover.TestSNMPV3Credentials(device.ip_address, v3_list)
                if test_result!=False:
                    data =True

            if test_result is not None:
                # Credentials matched, update the device entry
                device.SNMP_VERSION = test_result['snmp_version']
                device.MODIFICATION_DATE = datetime.now()
                configs.db.session.commit()
        return data

    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        print("Error in SNMP credentials:", str(e), file=sys.stderr)
        return False


# def CheckSNMPCredentials():
#     try:
#         query_string = f"SELECT * FROM auto_discovery_table WHERE `SNMP_STATUS`='Enabled';"
#         results = configs.db.execute(query_string)
#         print("result for query string enable SNMP status", results, file=sys.stderr)
#
#         # Fetch v2 credentials
#         query_string = f"SELECT snmp_read_community FROM snmp_credentials_table WHERE category='v1/v2';"
#         creds = configs.db.execute(query_string)
#         print("creds are::::::::::::::::::::::", creds, file=sys.stderr)
#         v2_list = [row[0] for row in creds]
#
#         # Fetch v3 credentials
#         query_string = f"SELECT profile_name, username, snmp_port, authentication_method, password, encryption_method, encryption_password, CREDENTIALS_ID FROM snmp_credentials_table WHERE category='v3';"
#         results = configs.db.execute(query_string)
#         v3_list = []
#         for row in results:
#             SNMPObj = {
#                 'username': row[1],
#                 'port': row[2],
#                 'authentication_protocol': row[3],
#                 'authentication_password': row[4],
#                 'encryption_protocol': row[5],
#                 'encryption_password': row[6]
#             }
#             v3_list.append(SNMPObj)
#
#         for row in results:
#             test_result = auto_discover.test_snmp_v2_credentials(row[1], v2_list)
#             if test_result is None:
#                 test_result = auto_discover.test_snmp_v3_credentials(row[1], v3_list)
#
#             if test_result is not None:
#                 query_string = f"UPDATE auto_discovery_table SET SNMP_VERSION='{test_result['snmp_version']}', MODIFICATION_DATE='{datetime.now()}' WHERE IP_ADDRESS='{row[1]}';"
#                 configs.db.execute(query_string)
#                 configs.db.commit()
#                 break  # Add a break statement to exit the loop after updating
#
#     except Exception as e:
#         configs.db.rollback()
#         traceback.print_exc()
#         print("Error in SNMP credentials ", str(e))
def add_networks_util(network_obj, update):
    try:
        data = {}
        network, status = check_network_name(network_obj)
        print("network id:::::::::::::::::::",network,file=sys.stderr)
        print("status is::::::::::::::::::::",status,file=sys.stderr)
        network_id = network.network_id
        print("network id is::::::::::::::::::::",network_id,file=sys.stderr)
        if status != 200:
            return network, status

        subnet, status = check_subnet(network_obj)
        if status != 200:
            return subnet, status

        exist = False
        if network is not None:
            exist = True
        #     if not update:
        #         return f"{network_obj['network_name']} : Network Name Already Assigned", 400
        #
        #     if subnet is not None:
        #         if network.subnet != subnet.subnet:
        #             return f"{network_obj['network_name']} : Subnet Already Exists - {network_obj['subnet']}", 400
        # else:
        #     if subnet is not None:
        #         return f"{network_obj['network_name']} : Subnet Already Exists - {network_obj['subnet']}", 400

            network = AutoDiscoveryNetworkTable()
            network.network_name = network_obj['network_name']

        network.subnet = network_obj['subnet']

        if network_obj['scan_status'] is None:
            network_obj['scan_status'] = "InActive"
        elif str(network_obj['scan_status']).lower() == 'inactive':
            network_obj['scan_status'] = "InActive"
        else:
            network_obj['scan_status'] = "Active"

        network.scan_status = network_obj['scan_status']

        if network_obj['excluded_ip_range'] is None:
            network.excluded_ip_range = "No Exclusion"
        elif network_obj['excluded_ip_range'].strip() == "":
            network.excluded_ip_range = "No Exclusion"
        else:
            network.excluded_ip_range = network_obj['excluded_ip_range'].strip()

        if exist:
            if UpdateDBData(network) == 200:
                data_dict = {
                    "network_id": network_id,
                    "network_name": network.network_name,
                    "scan_status": network.scan_status,
                    "excluded_ip_range": network.excluded_ip_range,
                    "no_of_devices": network.no_of_devices,
                    "subnet": network.subnet
                }
                msg = f"{network_obj['network_name']} : Network Updated Successfully"
                data['data'] = data_dict
                data['message'] = msg
                status = 200
            else:

                msg = f"{network_obj['network_name']} : Error While Updating Network"
                status = 500
        else:
            if InsertDBData(network) == 200:
                data_dict = {
                    "network_id": network.network_id,
                    "network_name": network.network_name,
                    "scan_status": network.scan_status,
                    "excluded_ip_range": network.excluded_ip_range,
                    "no_of_devices":network.no_of_devices,
                    "subnet":network.subnet
                }
                msg = f"{network_obj['network_name']} : Network Inserted Successfully"
                data['data'] = data_dict
                data['message'] = msg
                status = 200
            else:
                msg = f"{network_obj['network_name']} : Error While Inserting Network"
                status = 500

        print(msg, file=sys.stderr)
        return data, status

    except Exception:
        traceback.print_exc()
        return "Server Error While Adding Discovery Network", 500
def construct_obj_dict(row):
    """
    Transforms a database row object into a dictionary.

    Args:
    - row: An object representing a row from the database.
           This object should have attributes that match the database columns.

    Returns:
    A dictionary with keys and values extracted from the row object.
    """
    return {
        "discovery_id": row.discovery_id,
        "ip_address": row.ip_address,
        "subnet": row.subnet,
        "os_type": row.os_type,
        "make_model": row.make_model,
        "function": row.function,
        "vendor": row.vendor,
        "snmp_status": row.snmp_status,
        "snmp_version": row.snmp_version,
        "ssh_status": row.ssh_status
    }