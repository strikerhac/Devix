
from datetime import datetime
import sys, json
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data


from app.pullers.Greatbay.parsing import Parse
# from parsing import Parse

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
        
        sh_version = {"command":"uname -r \n","sleep":10, "template":"{{version | ORPHRASE }}"}
        
        config = {"command":"ifconfig \n","sleep":10, "template":"""{{ interfcae }}: flags={{flags}} metric 0 mtu {{ mtu }}
                                                                        media: {{media | ORPHRASE}}
                                                                        status: {{ status }}"""}
        command_list.append(sh_version)
        command_list.append(config)
        
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
                                            'serial_number': None, 
                                            'pn_code': None, 
                                            'hw_version': None, 
                                            "software_version": ver[0], 
                                            "desc": None, 
                                            "max_power": None, 
                                            "manufecturer": "GreatBay",
                                            "patch":None ,
                                            "status": "Production", 
                                            "authentication": "AAA"},
                                            'board':[],
                                            'sub_board':[],
                                            'sfp':[],
                                            'license':[],
                                            'status':'success'})
                
            self.get_sfps(host, data)
            print("Prime data is below", file=sys.stderr)
            print(f"{self.inv_data}", file=sys.stderr)
            self.inv_data[host['ip_address']].update({'status': 'success'})
            print(self.inv_data,file=sys.stderr)
            self.failed = uam_inventory_data(self.inv_data)
        except Exception as e:
            print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
            if host['ip_address'] in self.inv_data:
                self.inv_data[host['ip_address']].update({'status': 'error'})

           
    
    
    def get_sfps(self, host, sfps_results):
        try:
            sfps_data = []

            print(f"Getting sfp data...", file=sys.stderr)

            for sfp in sfps_results:
                sfp_data = {'port_name': sfp.get('port_name'),
                            'mode': sfp.get('mode'),
                            'speed': sfp.get('speed'),
                            'hw_version': None,
                            'serial_number': None,
                            'port_type': None,
                            'connector': None,
                            'wavelength':None,
                            'optical_direction_type': None,
                            'pn_code': None,
                            'status': sfp.get('status'),
                            'description': None,
                            'manufacturer': None,
                            'media_type': None}

                sfps_data.append(sfp_data)

            self.inv_data[host['ip_address']].update({"sfp": sfps_data})
        except Exception:
            self.inv_data[host['ip_address']].update({"sfp": []})

 
if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.64.194.244",
            "device_type": "greatbay",
            "username": "ciscoadmin",
            "password": "M0b1lyy@3Dn@790"
        }
        ]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = PrimePuller()
    print(json.dumps(puller.get_inventory_data(hosts)))