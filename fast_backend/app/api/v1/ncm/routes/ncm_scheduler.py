#
# # from app.monitoring.pullers.general import GeneralPuller
# # from app.monitoring.pullers.window import WindowPuller
# # from app.monitoring.pullers.linux import LinuxPuller
# # from app.monitoring.pullers.cisco_asa import ASAPuller
# # from app.monitoring.pullers.juniper import JuniperPuller
# # from app.monitoring.pullers.fortinet import FortinetPuller
# # from app.monitoring.pullers.cisco_wlc import WLCSPuller
# # from app.monitoring.pullers.cisco_ios import IOSPuller
#
# from app.ncm_pullers.backup_configurations import *
# from flask_apscheduler import APScheduler
# from app import app, db
# import sys
# from app.scheduler import scheduler
#
# from datetime import datetime
# from flask import request
#
# import traceback
# import threading
#
#
#
# def RunConfig(device):
#     try:
#         print(f"{device['ip_address']} : Running Backup")
#
#         command = ''
#         device_type = device['device_type'].strip()
#         if device_type=='cisco_ios_xe':
#             device_type = 'cisco_xe'
#             command = 'show running-conf'
#         if device_type=='cisco_ios_xr':
#             device_type = 'cisco_xr'
#             command = 'show running-conf'
#         if device_type=='cisco_ios' or device_type=='cisco_xr' or device_type=='cisco_xe' or device_type=='cisco_asa' or device_type=='cisco_nxos' or device_type=='cisco_wlc' or device_type=='cisco_ftd':
#             command = 'show running-config'
#         elif device_type=='fortinet':
#             command = 'show full-configuration'
#         configurationPuller = Puller()
#
#         output = configurationPuller.poll(device,command)
#
#         # if configurationPuller.Success()==True:
#         #     return "Configuration Backup Successful",200
#         # elif configurationPuller.Exists() ==True:
#         #     return "Configuration Already Exists",500
#         # elif configurationPuller.FailedLogin()==True:
#         #     return "Failed to Login into Device",500
#         # else:
#         #     return "Something Went Wrong",500
#     except Exception as e:
#         print(f"{device['ip_address']} : Error While Running Backup")
#         traceback.print_exc()
#
#
#
# def StartPoll(devices):
#     try:
#         for device in devices:
#             th = threading.Thread(target=RunConfig, args=(device,))
#             th.start()
#     except Exception:
#         print(f"NCM Poll : Error")
#         traceback.print_exc()
#
#
#
#
# def NCMActiveDevices():
#     @scheduler.task('interval', id="ncmRun", seconds=60)
#     def NCMRun():
#         devices = []
#
#         try:
#             queryString = f"select IP_ADDRESS,DEVICE_TYPE,PASSWORD_GROUP,DEVICE_NAME from ncm_table where `STATUS`='Active';"
#             result = db.session.execute(queryString)
#
#             for row in result:
#                 objDict={}
#                 ip_address = row[0]
#                 device_type = row[1]
#                 password_group = row[2]
#                 device_name = row[3]
#
#                 objDict['ip_address'] = ip_address
#                 objDict['device_type'] = device_type
#                 objDict['device_name'] = device_name
#
#                 queryString2 = f"select USERNAME,PASSWORD from password_group_table where password_group='{password_group}';"
#                 result2 = db.session.execute(queryString2)
#
#                 if result2 is None:
#                     print(f"{objDict['ip_address']} : Error : Password Group Not Found")
#
#                 for row2 in result2:
#                     username = row2[0]
#                     password = row2[1]
#                     username = username.strip()
#                     password = password.strip()
#                     objDict['username'] = username
#                     objDict['password'] = password
#
#                 devices.append(objDict)
#
#         except Exception:
#             traceback.print_exc()
#             print("Error In NCM ACtive Devices", file=sys.stderr)
#
#         print(f"NCM Devices: {devices}",file=sys.stderr)
#         StartPoll(devices)
#
#
#
# @app.route("/runNCM", methods=['GET'])
# # @token_required
# def runNCM():
#     try:
#         print("\nNCM Started\n\n", file=sys.stderr)
#         NCMActiveDevices()
#         return "NCM Scheduler Has Been Started"
#     except Exception as e:
#         print("Error While Starting NCM Scheduler", file=sys.stderr)
#         error = "Something Went Wrong:", type(e).__name__, str(e)
#         return error
