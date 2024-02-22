from netmiko import Netmiko
from datetime import datetime
import sys, json
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data
from app.utils.failed_utils import addFailedDevice


class A10Puller(object):
    
    def __init__(self):
        self.inv_data = {}
        self.connections_limit = 50
        self.failed = False
    def get_inventory_data(self, hosts):
        threads =[]
        
        for host in hosts:
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
            return self.failed
        

    def poll(self, host):
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 3
        c = 0
        is_login = False
        login_exception = None
        while c < login_tries :
            try:
                device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=host['device_type'], timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}", file=sys.stderr)
                is_login = True
                break
            except Exception as e:
                c+=1
                login_exception = str(e)
                self.failed = True                
        if is_login==False:
            print(f"Failed to login {host['ip_address']}", file=sys.stderr)
            self.inv_data[host['ip_address']] = {"error":"Login Failed"}
            date = datetime.now()
            self.failed = True
            addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'UAM')
            # file_name = time.strftime("%d-%m-%Y")+".txt"
            # failed_device=[]
            #Read existing file
            # try:
            #     with open('app/failed/ims/'+file_name,'r',encoding='utf-8') as fd:
            #         failed_device= json.load(fd)
            # except:
            #     pass
            #Update failed devices list
            
            # failed_device.append({"ip_address": host['ip_address'],"date":  time.strftime("%d-%m-%Y"), "time": time.strftime("%H-%M-%S"), "reason":login_exception})
            # try:
            #     with open('app/failed/ims/'+file_name, 'w', encoding='utf-8') as fd:
            #         fd.write(json.dumps(failed_device))
            # except Exception as e:
            #     print(e)
            #     print("Failed to update failed devices list", file=sys.stderr)

        if is_login==True:
            try:       
                print("getting version", file=sys.stderr)
                ver = device.send_command("show version", textfsm_template='app/pullers/ntc-templates/ntc_templates/templates/a10_show_version.textfsm', use_textfsm=True)
                print(f"data is {ver}", file=sys.stderr)
                
                version = ver[0]['version']
                patch = ver[0]['build']
                serial = ver[0]['serial'] 
                if host['ip_address'] not in self.inv_data:
                    self.inv_data[host['ip_address']] = {}
                    
                    self.inv_data[host['ip_address']].update({'device':
                                                {'ip_addr': host['ip_address'], 
                                                'serial_number': serial, 
                                                'pn_code': None, 
                                                'hw_version': None, 
                                                "software_version": version, 
                                                "desc": None, 
                                                "max_power": None, 
                                                "manufecturer": "Cisco",
                                                "patch_version":patch ,
                                                "status": "Production", 
                                                "authentication": "AAA"},
                                                'board':[],
                                                'sub_board':[],
                                                'sfp':[],
                                                'license':[],
                                                'status':'success'})

                print("A10 data is below", file=sys.stderr)
                print(f"{self.inv_data}", file=sys.stderr)
                self.inv_data[host['ip_address']].update({'status': 'success'})
                print(self.inv_data,file=sys.stderr)
                self.failed = uam_inventory_data(self.inv_data)
            except Exception as e:
                print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
                if host['ip_address'] in self.inv_data:
                    self.inv_data[host['ip_address']].update({'status': 'error'})
                    
        if is_login:device.disconnect()

           

 
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.42.192.4",
            "device_type": "a10",
            "username": "srv00282",
            "password": "99maAF5smUt61397"
        }
        ]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = A10Puller()
    print(json.dumps(puller.get_inventory_data(hosts)))