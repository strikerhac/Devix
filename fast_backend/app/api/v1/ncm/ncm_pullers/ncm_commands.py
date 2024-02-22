# from ipaddress import ip_address
# import secrets
# import traceback
# from unicodedata import name
# from netmiko import Netmiko,ConnectHandler
# from datetime import datetime
# import re, sys, time, json
# import threading
# from app import app
# from app.common_utils.insert_to_db import UamInventoryData
# from app.monitoring.common_utils.utils import addFailedDevice
# def FormatDate(date):
#     #print(date, file=sys.stderr)
#     if date is not None:
#         result = date.strftime('%d-%m-%Y')
#     else:
#         #result = datetime(2000, 1, 1)
#         result = datetime(1, 1, 2000)
#
#     return result
#
# class IOSPuller(object):
#
#     def __init__(self):
#         self.inv_data = {}
#         self.connections_limit = 50
#         self.stack_priority= 0
#         self.stack_switch= ""
#         self.failed = False
#         self.output = ""
#         self.response = False
#         self.response1 = False
#
#     def poll(self, host,device_type,command):
#         print('HOST IS :',type(host),file=sys.stderr)
#         print(f"NCM - {host['ip_address']} : Connecting...", file=sys.stderr)
#
#         login_tries = 2
#         ssh = 0
#         telnet = 0
#         is_login = False
#         login_exception = None
#
#         connection = None
#
#
#         while ssh < login_tries :
#
#             try:
#                 connection = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=device_type, timeout=600, global_delay_factor=2, banner_timeout=300)
#
#                 # connection = ConnectHandler(**device)
#
#                 print(device,file=sys.stderr)
#                 print(f"NCM - {host['ip_address']} : SSH - Logged In Successfully",file=sys.stderr)
#
#                 is_login = True
#                 break
#             except Exception as e:
#                 ssh +=1
#                 print(f"NCM - {host['ip_address']} : SSH - Failed to login",file=sys.stderr)
#                 login_exception = str(e)
#
#         # print(f"NCM - {host['ip_address']} : Telnet - Login Exception\n{login_exception}", file=sys.stderr)
#
#         if is_login == False:
#
#             device = {
#                 'device_type': f"{device_type}_telnet",
#                 'ip': host['ip_address'],
#                 'password': host['password'],
#                 'secret' : 'S3cur!ty@2020',
#                 'port': 23,
#                 'timeout': 300,
#             }
#
#             while telnet < login_tries :
#
#                 try:
#                     connection = ConnectHandler(**device)
#
#                     print(f"NCM - {host['ip_address']} : Telnet - Logged In Successfully",file=sys.stderr)
#
#                     is_login = True
#                     break
#                 except Exception as e:
#                     telnet +=1
#                     print(f"NCM - {host['ip_address']} : Telnet - Failed to login",file=sys.stderr)
#                     login_exception = str(e)
#
#
#
#         if is_login==False:
#             self.inv_data[host['ip_address']] = {"error":"Login Failed"}
#             date = datetime.now()
#             self.failed = True
#             addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'NCM')
#             self.response = True
#
#
#         if is_login==True:
#             print(f"NCM - {host['ip_address']} : Executing {command} ...",file=sys.stderr)
#
#             if ssh == 2:
#                 connection.enable()
#                 output = connection.send_command(f"{command}")
#                 connection.disconnect()
#             else:
#                 output = connection.send_command(f"{command}")
#
#             print(f"NCM - {host['ip_address']} :  {output}",file=sys.stderr)
#             self.response1 = True
#             self.output =  output
#
#
#     def FailedLogin(self):
#         return self.response
#
#     def CommandExecutionResponse(self):
#         return self.response1
#
#     def CommandOutput(self):
#         return self.output
#