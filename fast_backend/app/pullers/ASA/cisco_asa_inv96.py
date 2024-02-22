
from datetime import datetime
import sys, json
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data

from app.pullers.ASA.parsing import Parse
# from parsing import Parse
class ASA96Puller(object):
    
    def __init__(self):
        self.inv_data = {}
        self.connections_limit = 50
        
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
            return self.inv_data
        

    def poll(self, host):
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        parse_output = Parse()
        command_list = []
        ver = {"command":"show version \n\n","sleep":2, "template":"asa_show_version"}
        command_list.append(ver)
        
        data = parse_output.perform(host['ip_address'], host['username'], host['password'], command_list)
        ver = None
        serial = None
        for x in data:
            if x.get('version'):
                ver = x['version'][0]
            if x.get('serial'):
                serial = x['serial'][0]
                    
        try:        
            if host['ip_address'] not in self.inv_data:
                self.inv_data[host['ip_address']] = {}
                data = []
                
                self.inv_data[host['ip_address']].update({'device':
                                            {'ip_addr': host['ip_address'], 
                                            'serial_number': serial[1], 
                                            'pn_code': None, 
                                            'hw_version': None, 
                                            "software_version": ver[0], 
                                            "desc": 'Cisco Adaptive Security Appliance', 
                                            "max_power": None, 
                                            "manufecturer": 'Cisco Adaptive Security Appliance',
                                            "patch":None,
                                            "status": "Production", 
                                            "authentication": "AAA"},
                                            'board':[],
                                            'sub_board':[],
                                            'sfp':[],
                                            'license':[],
                                            'status':'success'})

            print("asa data is below", file=sys.stderr)
            print(f"{self.inv_data}", file=sys.stderr)
            self.inv_data[host['ip_address']].update({'status': 'success'})
            print(self.inv_data,file=sys.stderr)
            self.failed = uam_inventory_data(self.inv_data)
        except Exception as e:
            print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
            if host['ip_address'] in self.inv_data:
                self.inv_data[host['ip_address']].update({'status': 'error'})

           

 
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.14.93.56",
            "device_type": "cisco_asa",
            "username": "srv00280",
            "password": "1a3X#eEW3$40vPN%"
        }
        ]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = ASA96Puller()
    print(json.dumps(puller.get_inventory_data(hosts)))