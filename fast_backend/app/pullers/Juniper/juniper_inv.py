import traceback
from netmiko import Netmiko
from datetime import datetime
import re, sys, time, json
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data


class JuniperPuller(object):
    
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
            print(f"SELF DOT FAILED IS {self.failed}",file=sys.stderr)
            return self.failed
        

    def poll(self, host):
        host['device_type'] = 'juniper'
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 3
        c = 0
        is_login = False
        login_exception= None
        while c < login_tries :
            try:
                device = Netmiko(host=host['ip_address'], username=host['username'], password=host['password'], device_type=host['device_type'], timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}", file=sys.stderr)
                is_login = True
                break
            except Exception as e:
                c +=1
                print(f"Falied to login {host['ip_address']}", file=sys.stderr)
                login_exception= str(e)
                
                
        if is_login==False:
            self.inv_data[host['ip_address']] = {"error":"Login Failed"}
            date = datetime.now()
            self.failed = True
            addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'UAM')
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
            #     print("Failed to update failed devices list:"+str(e), file=sys.stderr)
            
            
        if is_login==True:    

            print("getting inventory....", file=sys.stderr)
            c = 0
            while c < 3:      #trying 3 times of inventory if gets failed
                print(f"Inventory try {c}", file=sys.stderr)
                try:
                    inv = device.send_command('show chassis hardware |no-more', textfsm_template=f"app/pullers/ntc-templates/ntc_templates/templates/juniper_junos_show_chassis_hardware.textfsm",use_textfsm=True)  
                    print(inv,file=sys.stderr)
                    break
                except:
                    c +=1
                    time.sleep(1.5)

            try:
                print("Inventory fetched...")
                if host['ip_address'] not in self.inv_data:
                    self.inv_data[host['ip_address']] = {}
                for index, data in enumerate(inv):
                    if ('chassis' in data['name'].lower()) or ('chassis' in data.get('ch_name').lower()):
                        self.inv_data[host['ip_address']].update({'device':
                                                    {'ip_addr': host['ip_address'], 
                                                    'serial_number': data['serial'] if not data['serial']=='' else data.get('ch_serial'), 
                                                    'pn_code': data['pid'] if not data['pid']=='' else None, 
                                                    'hw_version': None, 
                                                    "software_version": data['version'] if not data['version']=='' else None, 
                                                    "desc": data.get('desc') if not data.get('desc')=='' else data.get('ch_desc') , 
                                                    "max_power": None, 
                                                    "manufecturer": "Juniper", 
                                                    "status": "Production", 
                                                    "authentication": "AAA"}})
                        inv.pop(index)
                        break
                    
                self.get_boards(host, inv)   
                self.get_sub_boards(host, inv)
                self.get_sfps(host, inv)
                self.get_license(host, device)

                self.inv_data[host['ip_address']].update({'status': 'success'})
                print(self.inv_data,file=sys.stderr)
                
                self.failed = uam_inventory_data(self.inv_data)
                
            except Exception as e:
                traceback.print_exc()
                self.failed = True
                print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
                if host['ip_address'] in self.inv_data:
                    self.inv_data[host['ip_address']].update({'status': 'error'})

            if is_login: device.disconnect()

        else:
            self.failed = True
        


    def get_boards(self,host, inventory):
        try:
            sfp_sub_modules = ['midplane','board','pem','fpc']
            board_data = []
            for inv in inventory:
                is_sfp = False
                for sf in sfp_sub_modules:
                    if (sf in inv['name'].lower()):
                        is_sfp = True
                        
                if is_sfp==True and inv.get('name'):
                    board_data.append({
                                        "board_name": inv['name'],
                                        "serial_number": inv['serial'],
                                        "pn_code":inv.get('pid',None),
                                        "hw_version": None,
                                        "slot_id": inv.get('name') if inv.get('name') else inv.get('slot'),
                                        "status": "Production",
                                        "software_version": inv.get('version'),
                                        "description": inv.get('desc')
                                        })
            
            self.inv_data[host['ip_address']].update({'board': board_data})
        except Exception:
            self.inv_data[host['ip_address']].update({'board': []})
        

    def get_sub_boards(self, host, inventory):
        try:
            sub_modules=['wan mezz']
            sub_board_data = []
            for inv in inventory:
                is_sub_board = False
                name = inv['name'].lower()
                for sm in sub_modules:
                    if sm in name:
                        is_sub_board=True
                        
                if is_sub_board:
                    if inv.get('name'):
                        sub_board_data.append({'subboard_name': inv['name'],
                                                'subboard_type':None,
                                                'slot_number':None,
                                                'subslot_number':None,
                                                'hw_version': None,
                                                'software_version':inv['version'],
                                                'serial_number': inv['serial'],
                                                'pn_code':inv.get('pid',None),
                                                'status':'Production',
                                                'description': inv['desc']
                                                })
            self.inv_data[host['ip_address']].update({'sub_board': sub_board_data})
        except Exception:
            self.inv_data[host['ip_address']].update({'sub_board': []})


    def get_sfps(self, host, inventory):
        try:
            sfps_data = []
            print(f"Getting sfp data..." ,file=sys.stderr)
            for inv in inventory:
                if 'Xcvr' in inv['name']:
                    modes= {'LR':'single-mode','SR':'multimode','LH':'single-mode','LX':'single-mode', 'SX':'multimode'}
                    mode = ''
                    for key, value in modes.items():
                        if key in inv['pid'] or key in inv['desc']:
                            mode = value
                            break
                        
                    speed = re.findall(r'-(\d+G)-', inv.get('desc'))
                    speed = speed[0] if speed else "1G"
                    sfp_data = {'port_name': inv.get('name'),
                                'mode': mode if mode else None,
                                'speed': speed,
                                'hw_version': None,
                                'serial_number': inv['serial'].lstrip('0'),
                                'port_type': None,
                                'connector': None,
                                'wavelength':None,
                                'optical_direction_type':None,
                                'pn_code':inv.get('desc'),
                                'status':'Production',
                                'description': inv['desc'],
                                'manufacturer': None,
                                'media_type': None}
                    sfps_data.append(sfp_data)

            self.inv_data[host['ip_address']].update({"sfp":sfps_data})
        except Exception:
            self.inv_data[host['ip_address']].update({"sfp":[]})


    def get_license(self, host, device):
        try:
            print("Getting license")
            license = device.send_command('show system license', use_textfsm=True)
            all_license = []
            for lic in license:
                desc = re.findall(r'([a-zA-Z0-9 ]*)', lic['feature'])
                desc = "".join([x for x in desc if x])
                if lic.get('feature'):
                    all_license.append({
                                        "name": desc,
                                        "description":  None if desc=='' else desc,
                                        "activation_date": "2000-01-01",
                                        "expiry_date":'2000-01-01',
                                        "grace_period": None,
                                        "serial_number": None,
                                        "status": 'Production',
                                        "capacity": None,
                                        "usage": None,
                                        "pn_code": None
                                    })
            self.inv_data[host['ip_address']].update({"license":all_license})
        except Exception:
            print("License not found", file=sys.stderr)
            self.inv_data[host['ip_address']].update({"license":[]})

   
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.64.255.4",
            "device_type": "juniper",
            "username": "srv00280",
            "password": "1a3X#eEW3$40vPN%"
        }]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = JuniperPuller()
    print(json.dumps(puller.get_inventory_data(hosts)))