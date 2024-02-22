import requests
import sys, json
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

class PulseSecurePuller(object):
    
    def __init__(self):
        self.inv_data = {}
        self.connections_limit = 50

    def get_inventory_data(self, hosts):
        threads =[]
        for host in hosts:
            # self.poll(host)
            th = threading.Thread(target=self.poll, args=(host,))
            th.start()
            threads.append(th)
            if len(threads) == self.connections_limit: 
                for t in threads:
                    t.join()
                threads =[]
        
        else:
            for t in threads: # if request is less than connections_limit then join the threads and then return data
                t.join()
            return self.inv_data

    def poll(self, host):
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        
        try:
            base_url = f"https://10.64.93.150"
            system_path = '/api/v1/system/system-information' 
            url = base_url + system_path 
            
            api_key = '7rngji1Ycbhh92ZRIe2dHmMVBeHDT3rRDNs+q4nnbM4='
            
            print('getting system info ', file=sys.stderr)
            
            response = requests.request('GET', url, auth=(api_key, ''), verify=False, timeout=10)
            #print (response.json())
            if response.ok:
                data = response.json()
                if host['ip_address'] not in self.inv_data:
                    self.inv_data[host['ip_address']]= {'device':
                                                  {'ip_addr': host['ip_address'], 
                                                    'serial_number': data['system-information']['serial-number'], 
                                                    'hw_version':  data['system-information']['hardware-model'], 
                                                    "software_version": data['software-inventory']['software']['version'] , 
                                                    "patch_version": data['software-inventory']['software']['build'],
                                                    'pn_code': None, 
                                                    "status": 'Production',
                                                    "desc": data['system-information']['host-name'], 
                                                    "max_power": None,
                                                    "manufecturer": "PulseSecure",
                                                    "authentication": "AAA"},
                                                    'board':[],
                                                    'sub_board':[],
                                                    'sfp':[],
                                                    'license':[],
                                                    'status':'success'}
                                                    
                    print(f"{self.inv_data}", file=sys.stderr)
                    self.failed = uam_inventory_data(self.inv_data)
            else:
                print(f"Connection failed {host['ip_address']}", file=sys.stderr)
                
                
                raise Exception
        except Exception as e:
            print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
            date = datetime.now()
            addFailedDevice(host['ip_address'],date,host['device_type'],str(e),'UAM')
            # file_name = time.strftime("%d-%m-%Y")+".txt"
            # failed_device=[]
            # #Read existing file
            
            # try:
            #     with open('app/failed/ims/'+file_name,'r',encoding='utf-8') as fd:
            #         failed_device= json.load(fd)
            # except:
            #     pass
            # #Update failed devices list
            
            # failed_device.append({"ip_address": host['ip_address'],"date":  time.strftime("%d-%m-%Y"), "time": time.strftime("%H-%M-%S"), "reason":str(e)})
            # try:
            #     with open('app/failed/ims/'+file_name, 'w', encoding='utf-8') as fd:
            #         fd.write(json.dumps(failed_device))
            # except Exception as e:
            #     print(e)
            #     print("Failed to update failed devices list", file=sys.stderr)

                
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.64.165.117",
            "device_type": "pulse_secure",
            "username": "srv00280",
            "password": "1a3X#eEW3$40vPN%"
        }]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = PulseSecurePuller()
    print(json.dumps(puller.get_inventory_data(hosts)))


