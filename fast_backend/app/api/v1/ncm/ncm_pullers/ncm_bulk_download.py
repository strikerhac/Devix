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
# from app import app,db
# import os
#
# def FormatDate(date):
#     #print(date, file=sys.stderr)
#     if date is not None:
#         result = date.strftime('%d-%m-%Y')
#     else:
#         #result = datetime(2000, 1, 1)
#         result = datetime(1, 1, 2000)
#
#     return result
# global response2
# global response3
# response2 = False
# response3 = False
#
# class DownloadPuller(object):
#
#     def __init__(self):
#         self.inv_data = {}
#         self.connections_limit = 50
#         self.stack_priority= 0
#         self.stack_switch= ""
#         self.failed = False
#         self.response2 = False
#         self.response3 = False
#     def get_inventory_data(self, hosts,device_type,command):
#         threads =[]
#         print('THIS IS INVENTORY DATA',file=sys.stderr)
#         for host in hosts:
#             th = threading.Thread(target=self.poll, args=(host,device_type,command))
#             th.start()
#             threads.append(th)
#             if len(threads) == self.connections_limit:
#                 for t in threads:
#                     t.join()
#                 threads =[]
#
#         else:
#             for t in threads: # if request is less than connections_limit then join the threads and then return data
#                 t.join()
#
#             return self.failed
#
#
#     def poll(self, host,device_type,command):
#         print('HOST IS :',type(host),file=sys.stderr)
#         print(f"Connecting to {host['ip_address']}")
#         login_tries = 2
#         telnet = 0
#         ssh = 0
#         is_login = False
#         login_exception = None
#         connection = None
#
#         while ssh < login_tries :
#             try:
#                 connection = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=device_type, timeout=600, global_delay_factor=2, banner_timeout=300)
#
#                 print(f"NCM - {host['ip_address']} : SSH - Logged In Successfully",file=sys.stderr)
#
#                 is_login = True
#                 break
#             except Exception as e:
#                 ssh +=1
#                 print(f"Failed to login {host['ip_address']}",file=sys.stderr)
#                 login_exception = str(e)
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
#                     # device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=host['device_type'], timeout=600, global_delay_factor=2, banner_timeout=300)
#
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
#         if is_login==False:
#             # self.inv_data[host['ip_address']] = {"error":"Login Failed"}
#             date = datetime.now()
#             self.failed = True
#             addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'NCM')
#             self.response3 = True
#
#         if is_login==True:
#
#             print(f"NCM - {host['ip_address']} : Executing {command} ...",file=sys.stderr)
#
#             current_time = datetime.now()
#             file_name = f"{host['ip_address']}_{host['device_name']}_{current_time}"
#
#             if ssh ==2:
#                 connection.enable()
#                 connection.send_command(f"terminal length 0")
#                 output = connection.send_command(f"{command}")
#                 ip_br = connection.send_command("show ip interface brief")
#                 version = connection.send_command("show version")
#                 output+="\n\n\n"+ip_br+"\n\n\n"+version
#                 connection.disconnect()
#             else:
#                 output = connection.send_command(f"{command}")
#                 ip_br = connection.send_command("show ip interface brief")
#                 version = connection.send_command("show version")
#                 output+="\n\n\n"+ip_br+"\n\n\n"+version
#
#             print(f"BACKUP GENERATED FOR DEVICE {host['device_name']} at {current_time}",file=sys.stderr)
#             dataDict = {}
#             dataDict['name']=file_name
#             dataDict['value'] = (output)
#             self.response2 = True
#             return dataDict
#
#
#
#     def Success(self):
#         return self.response2
#
#     def FailedLogin(self):
#         return self.response3