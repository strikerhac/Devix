from ipaddress import ip_address
import secrets
import traceback
from unicodedata import name
from netmiko import Netmiko,ConnectHandler
import paramiko
from datetime import datetime
import re, sys, time, json
import threading
from app.core.config import *
from app.utils.failed_utils import FailedDevicesTable
import os
def FormatDate(date):
    #print(date, file=sys.stderr)
    if date is not None:
        result = date.strftime('%d-%m-%Y')
    else:
        #result = datetime(2000, 1, 1)
        result = datetime(1, 1, 2000)

    return result

class RestorePuller(object):

    def __init__(self):
        self.inv_data = {}
        self.connections_limit = 50
        self.stack_priority= 0
        self.stack_switch= ""
        self.failed = False
        self.response1 = False
        self.response2 = False
        self.response3 = False
    # def get_inventory_data(self, hosts,command):
    #     threads =[]
    #     print('THIS IS INVENTORY DATA',file=sys.stderr)
    #     for host in hosts:
    #         th = threading.Thread(target=self.poll, args=(host,command))
    #         th.start()
    #         threads.append(th)
    #         if len(threads) == self.connections_limit:
    #             for t in threads:
    #                 t.join()
    #             threads =[]

    #     else:
    #         for t in threads: # if request is less than connections_limit then join the threads and then return data
    #             t.join()

    #         return self.failed


    def poll(self, host,device_type,date):
        print('HOST IS :',type(host),file=sys.stderr)
        print(f"Connecting to {host['ip_address']}")
        login_tries = 3
        c = 0
        is_login = False
        login_exception = None
        while c < login_tries :
            try:
                device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=device_type, timeout=600, global_delay_factor=2, banner_timeout=300)
                print(device,file=sys.stderr)
                print(f"Success: logged in {host['ip_address']}",file=sys.stderr)
                is_login = True
                break
            except Exception as e:
                c +=1
                print(f"Failed to login {host['ip_address']}",file=sys.stderr)
                login_exception = str(e)
        if is_login==False:
            self.inv_data[host['ip_address']] = {"error":"Login Failed"}
            date = datetime.now()
            self.failed = True
            #faled devices table
            FailedDevicesTable(host['ip_address'],date,host['device_type'],login_exception,'NCM')
            self.response3 = True
        if is_login==True:

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host['ip_address'], username=host['username'], password=host['password'])


            print(f"Successfully Logged into device {host['device_type']}", file=sys.stderr)

            # device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=host['device_type'], timeout=600, global_delay_factor=2)
            # device.send_command('config t')
            file_name = ""
            queryString = f"select FILE_NAME from ncm_history_table where IP_ADDRESS='{host['ip_address']}' AND CONFIGURATION_DATE='{date}';"
            result =configs.db.execute(queryString)
            for row in result:
                file_name+=row[0]
            if file_name!="":

                cwd = os.getcwd()
                configPath = f"{cwd}/app/configuration_backups/{file_name}.cfg"
                # config_commands = ""
                # with open(configPath, 'r') as file:
                #     config_commands = file.read().splitlines()


                # output = net_connect.send_config_set(config_commands)
                # output = net_connect.send_config_from_file(configPath)

                sftp = ssh_client.open_sftp()
                sftp.put(configPath, 'temporary_config_file')

                ssh_client.exec_command('configure replace temporary_config_file')



                # Close the SFTP session
                sftp.close()



                # Close the SSH connection
                ssh_client.close()

                # print("Restorted ",file=sys.stderr)

                # device.send_config_from_file(config_file=configPath)
                print("Configuration Restored Successfully",file=sys.stderr)
                self.response1 = True
            else:
                self.response2 = True
    def Success(self):
        return self.response1

    def FileDoesNotExist(self):
        return self.response2
    def FailedLogin(self):

        return self.response3