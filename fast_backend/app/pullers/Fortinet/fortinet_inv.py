import traceback
from netmiko import Netmiko
from datetime import datetime
import re, sys, time
import threading
from dateutil.parser import parse
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data
from app.utils.failed_utils import addFailedDevice



class FortinetPuller(object):
    
    def __init__(self):
        self.inv_data = {}
        self.connections_limit = 50
        self.failed=False
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
        print(f"Connecting to {host['ip_address']}",  file=sys.stderr)
        login_tries = 5
        c = 0
        is_login = False
        login_exception = None
        while c < login_tries :
            try:
                device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=host['device_type'], timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}",  file=sys.stderr)
                is_login = True
                break
            except Exception as e:
                c +=1
                login_exception = str(e)
                print(e, file=sys.stderr)
        if is_login==False:
            print(f"Failed to login {host['ip_address']}",  file=sys.stderr)
            self.inv_data[host['ip_address']] = {"error":"Login Failed"}
            date = datetime.now()
            addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'UAM')
            self.failed = True
            # file_name = time.strftime("%d-%m-%Y")+".txt"
            # failed_device=[]
            # #Read existing file
            
            # try:
            #     with open('app/failed/ims/'+file_name,'r',encoding='utf-8') as fd:
            #         failed_device= json.load(fd)
            # except:
            #     pass
            # #Update failed devices list
            
            # failed_device.append({"ip_address": host['ip_address'],"date":  time.strftime("%d-%m-%Y"), "time": time.strftime("%H-%M-%S"), "reason":login_exception})
            # try:
            #     with open('app/failed/ims/'+file_name, 'w', encoding='utf-8') as fd:
            #         fd.write(json.dumps(failed_device))
            # except Exception as e:
            #     print(e)
            #     print("Failed to update failed devices list", file=sys.stderr)
            
        if is_login==True:    
            # try:
            #     print("getting version")
            #     ver = device.send_command("show version", use_textfsm=True)
            #     version = ver[0]['version'] if ver else ''
            # except:
            #     print("version not found")
            #     version = ''
            #     hardware = ''
            # try:
            #     print("getting max_power")
            #     max_power = device.send_command("show environment power", use_textfsm=True) #need confirmation
            #     max_power = max_power[0]['power_capacity_one'] if max_power else None
            # except Exception as e:
            #     print("Power not found")
            #     max_power = None

            print("getting inventory....",  file=sys.stderr)
            device.send_command('a')   #accept warning
            c = 0
            while c < 3:      #trying 3 times of inventory if gets failed
                print(f"Inventory try {c}",  file=sys.stderr)
                try:
                    inv = device.send_command('get system status', use_textfsm=True)
                    break
                except Exception as e:
                    print(e)
                    c +=1
                    time.sleep(1.5)

            try:
                print("Inventory fetched...",  file=sys.stderr)
                if host['ip_address'] not in self.inv_data:
                    self.inv_data[host['ip_address']] = {}

                for data in inv:
                    self.inv_data[host['ip_address']].update({'device':
                                                {'ip_addr': host['ip_address'], 
                                                'serial_number': data.get('serial_number'), 
                                                'pn_code': data['system_part_number'], 
                                                'hw_version': None, 
                                                "software_version": data['version'], 
                                                "desc": data['hostname'], 
                                                "max_power": None, 
                                                "manufecturer": "Fortinet", 
                                                "status": "Production", 
                                                "authentication": "AAA"}})

                
                self.get_sfps(host, inv, device)
                self.get_license(host, device)
                self.inv_data[host['ip_address']].update({'status': 'success'})
                self.inv_data[host['ip_address']].update({'board': []})
                self.inv_data[host['ip_address']].update({'sub_board': []})
                self.failed = uam_inventory_data(self.inv_data)
                print(self.inv_data,file=sys.stderr)
            except Exception as e:
                traceback.print_exc()
                print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
                if host['ip_address'] in self.inv_data:
                    self.inv_data[host['ip_address']].update({'status': 'error'})
                self.failed = True

            if is_login: device.disconnect()
            

    def get_sfps(self, host, inventory, device):
        try:
            sfps_data = []
            print(f"Getting sfp data..." ,file=sys.stderr)
            sfps = device.send_command('get system interface transceiver', use_textfsm=True)
            for sfp in sfps:
                sfp_data = {'port_name': sfp.get('port_name'),
                            'mode': None,
                            'speed': None,
                            'hw_version': None,
                            'serial_number': sfp['serial_number'].lstrip('0'),
                            'port_type': sfp.get('port_type'),
                            'connector': None,
                            'wavelength':None,
                            'optical_direction_type':None,
                            'pn_code':sfp.get('part_number'),
                            'status':'Production',
                            'description': sfp.get('name'),
                            'manufacturer': sfp.get('vendor'),
                            'media_type': None}
                sfps_data.append(sfp_data)

            self.inv_data[host['ip_address']].update({"sfp":sfps_data})
            print(self.inv_data,file=sys.stderr)
        except Exception as e:
            print(f"Exception occured in getting SFPS: {e}", file=sys.stderr)
            self.inv_data[host['ip_address']].update({"sfp":[]})


    def get_license(self, host, device):
        try:
            print("Getting license")
            license = device.send_command('diag auto update versions', use_textfsm=True)
            all_license = []
            for lic in license:
                desc = re.findall(r'([a-zA-Z0-9 ]*)', lic['name'])
                desc = "".join([x for x in desc if x])
                if lic.get('featureid'):
                    dt = parse(lic['last_update'])
                    last_update = dt.strftime('%Y-%m-%d')
                    dt2 = parse(lic['expiry_date'])
                    expiry = dt2.strftime('%Y-%m-%d')
                    all_license.append({
                                        "name": lic['name'],
                                        "description":  None if desc=='' else desc,
                                        "activation_date": last_update,
                                        "expiry_date": expiry,
                                        "grace_period": None,
                                        "serial_number": None,
                                        "status": 'Production',
                                        "capacity": None,
                                        "usage": None,
                                        "pn_code": None
                                    })
            self.inv_data[host['ip_address']].update({"license":all_license})
            print(self.inv_data,file=sys.stderr)
        except Exception:
            print("License not found",  file=sys.stderr)
            self.inv_data[host['ip_address']].update({"license":[]})


# if __name__ == '__main__':
#     hosts = [
#         {
#             #"host": "10.64.93.204",
#             "ip_address": "10.64.93.153",# "10.14.93.30",
#             "device_type": "fortinet",
#             "username": "srv00280",
#             "password": "1a3X#eEW3$40vPN%"
#         }]
#     print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
#     puller = FortinetPuller()
#     print(json.dumps(puller.get_inventory_data(hosts)))