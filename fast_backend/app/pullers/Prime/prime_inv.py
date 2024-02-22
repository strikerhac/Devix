
from datetime import datetime
import sys, json
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data



from app.pullers.Prime.parsing import Parse

class PrimePuller(object):
    
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
        yes_key = {"command":"yes \n","sleep":10, "template":""}
        sh_version = {"command":"show version \n","sleep":10, "template":"prime_show_version"}
        termlength = {"command":"\n","sleep":2}
        sh_inventory = {"command":"show inventory \n","sleep":10, "template":"prime_show_inventory"}
        
        command_list.append(yes_key)
        command_list.append(sh_version)
        command_list.append(termlength) 
        command_list.append(sh_inventory)
        data = parse_output.perform(host['ip_address'], host['username'], host['password'], command_list, host)
        
        ver = None
        inventory = None
        
        for x in data:
            if x.get('show version'):
                ver = x['show version'][0]
            if x.get('show inventory'):
                    inventory = x['show inventory'][0]
                    
        try:        
            if host['ip_address'] not in self.inv_data:
                self.inv_data[host['ip_address']] = {}
                data = []
                
                self.inv_data[host['ip_address']].update({'device':
                                            {'ip_addr': host['ip_address'], 
                                            'serial_number': inventory[4], 
                                            'pn_code': inventory[2], 
                                            'hw_version': inventory[3], 
                                            "software_version": ver[0], 
                                            "desc": inventory[1], 
                                            "max_power": None, 
                                            "manufecturer": "Cisco",
                                            "patch":ver[1] ,
                                            "status": "Production", 
                                            "authentication": "AAA"},
                                            'board':[],
                                            'sub_board':[],
                                            'sfp':[],
                                            'license':[],
                                            'status':'success'})

            print("Prime data is below", file=sys.stderr)
            print(f"{self.inv_data}", file=sys.stderr)
            self.inv_data[host['ip_address']].update({'status': 'success'})
            self.failed = uam_inventory_data(self.inv_data)
        except Exception as e:
            print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
            if host['ip_address'] in self.inv_data:
                self.inv_data[host['ip_address']].update({'status': 'error'})

           

 
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.64.194.244",
            "device_type": "prime",
            "username": "ciscoadmin",
            "password": "M0b1lyy@3Dn@790"
        },
        {
            "ip_address": "10.14.98.188",
            "device_type": "prime",
            "username": "ciscoadmin",
            "password": "M0b1lyy@3Dn@790"
        }
        ]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = PrimePuller()
    print(json.dumps(puller.get_inventory_data(hosts)))