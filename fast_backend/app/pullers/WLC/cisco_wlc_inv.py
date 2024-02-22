import traceback
from netmiko import Netmiko
import re, sys, time
import threading
from app.api.v1.uam.utils.uam_db_utils import uam_inventory_data

# from app import db
from app.models.uam_models import *

def InsertData(obj):
    #add data to db
        try:
            #obj.creation_date= datetime.now(tz)
            #obj.modification_date= datetime.now(tz)
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            print(f"Something else went wrong in Database Insertion {e}", file=sys.stderr)

        return True

def UpdateData(obj):
    #add data to db
    #print(obj, file=sys.stderr)
    try:
        #obj.modification_date= datetime.now(tz)
        db.session.merge(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        print(f"Something else went wrong in Database Updation {e}", file=sys.stderr)
    
    return True
class WLCPuller(object):
    
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
    
    
    def addInventoryToDB(self, host, ap): 
        
        try:
            apObj= APS_TABLE()

            apObj.ap_ip= ap['ip_addr']
            apObj.ap_name= ap['ap_name']
            apObj.serial_number= ap['serial_number']
            apObj.ap_model= ap['pn_code']
            apObj.hardware_version= ap['hw_version']
            apObj.software_version= ap['software_version']
            # apObj.manufacturer = ap['manufecturer']
            # apObj.status= "Registered" #ap['status']
            apObj.controller_name= host['ip_address']
            apObj.description = ap['desc']
            # apObj.modification_date = host['time']
        

            
            ap = APS_TABLE.query.with_entities(APS_TABLE.ap_id).filter_by(ap_name=apObj.ap_name).filter_by(controller_name=apObj.controller_name).first()
            if ap:
                apObj.ap_id= ap[0]
                apObj.modification_date=datetime.now()
                UpdateData(apObj)
            else:
                apObj.creation_date = datetime.now()
                apObj.modification_date=datetime.now()
                InsertData(apObj)
                
            print(f"%%%%%%%%%%%",apObj,file=sys.stderr)


            print("Successfully Added AP Data in DB ", file=sys.stderr)
        except Exception as e:
            print(f"Failed in Database Operation {e}", file=sys.stderr)
    
    def poll(self, host):
        host['device_type'] = 'cisco_wlc_ssh'
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
                login_exception= str(e)
                print(f"Failed to login {host['ip_address']}", file=sys.stderr)
                
        if is_login==False:
            self.inv_data[host['ip_address']] = {"error":"Login Failed"}
            self.failed = True
            date = datetime.now()
            # addFailedDevice(host['ip_address'],date,host['device_type'],login_exception,'UAM')
            
            
        if is_login==True:
            
            try:
                print("getting version", file=sys.stderr)
                device.send_command("config paging disable")
                ver = device.send_command("show sysinfo", use_textfsm=True)
                version = ver[0]['product_version'] if ver else ''
            except:
                print("version not found", file=sys.stderr)
                version = ''
                
            
            # get all Access points(APs) detail
            # show ap summary = > text fsm exists
            # show ap inventory all=> inventory for all aps
            # show ap image all => for ap version => textfsm exists
            print("getting inventory....", file=sys.stderr)
            c = 0
            while c < 3:      #trying 3 times of inventory if gets failed
                print(f"Inventory try {c}", file=sys.stderr)
                try:
                    inv = device.send_command('show inventory', use_textfsm=True)
                    break
                except Exception as e:
                    print(f"Inventory Exception is {e}", file=sys.stderr)
                    c +=1
                    time.sleep(1.5)

            try:
                print("Inventory fetched...", file=sys.stderr)
                if host['ip_address'] not in self.inv_data:
                    self.inv_data[host['ip_address']] = {}
                for index, data in enumerate(inv):
                    if ('chassis' in data['description'].lower()) or ('chassis' in data['name'].lower()):
                        self.inv_data[host['ip_address']].update({'device':
                                                    {'ip_addr': host['ip_address'], 
                                                    'serial_number': data['sn'], 
                                                    'pn_code': data['pid'], 
                                                    'hw_version': data['vid'], 
                                                    "software_version": version, 
                                                    "desc": data['description'], 
                                                    "max_power": None, 
                                                    "manufecturer": "Cisco", 
                                                    "status": "production", 
                                                    "authentication": None}})
                        inv.pop(index)
                        break
                    
                self.get_boards(host, inv, version)   
                self.get_sub_boards(host, inv)
                self.get_sfps(host, device)
                self.get_license(host, device)
                self.get_aps(host, device)
                self.inv_data[host['ip_address']].update({'status': 'success'})
                print(self.inv_data,file=sys.stderr)
                self.failed = uam_inventory_data(self.inv_data)
            except Exception as e:
                print(f"Inventory not found Exception detail==>{e}", file=sys.stderr)
                traceback.print_exc()
                if host['ip_address'] in self.inv_data:
                    self.inv_data[host['ip_address']].update({'status': 'error'})
                self.failed = True

            if is_login: device.disconnect()

    def get_boards(self,host, inventory, sw):
        try:
            sfp_sub_modules = ['sfp','gls','cpak','cfp', 'mpa' ,'glc', 'sx']
            board_data = []
            for inv in inventory:
                is_sfp = False
                for sf in sfp_sub_modules:
                    if (sf in inv['pid'].lower()) or (sf in inv['descr'].lower()):
                        is_sfp = True
                        
                if is_sfp==False:
                    board_data.append({
                                        "board_name": inv['description'],
                                        "serial_number": inv['sn'],
                                        "pn_code": inv['pid'],
                                        "hw_version": inv['vid'],
                                        "slot_id": inv['name'],
                                        "status": "active",
                                        "software_version": sw,
                                        "description": inv['description']
                                        })
            
            self.inv_data[host['ip_address']].update({'board': board_data})
        except Exception:
            self.inv_data[host['ip_address']].update({'board': []})
        
    def get_sub_boards(self, host, inventory):
        try:
            sub_modules=['mpa']
            sub_board_data = []
            for inv in inventory:
                is_sub_board = False
                pid = inv['pid'].lower()
                for sm in sub_modules:
                    if sm in pid:
                        is_sub_board=True
                        
                if is_sub_board:
                    sub_board_type = re.findall(r'mpa-(\w+)',pid) #need correction get from descr
                    slot_number = re.findall(r'[0-9a-zA-Z]*\/', inv['name'])
                    slot_number = "".join([x for index, x in enumerate(slot_number) if index<2])
                    sub_slot_n = inv['name'].split(' ')
                    sub_board_data.append({'subboard_name': inv['name'],
                                            'subboard_type':sub_board_type[0].upper() if sub_board_type else '',
                                            'slot_number':slot_number,
                                            'subslot_number':sub_slot_n[-1] if sub_slot_n else '',
                                            'hw_version': inv['vid'],
                                            'serial_number': inv['sn'],
                                            'pn_code':inv['pid'],
                                            'status':'active',
                                            'description': inv['description']
                                            })
            self.inv_data[host['ip_address']].update({'sub_board': sub_board_data})
        except Exception:
            self.inv_data[host['ip_address']].update({'sub_board': []})


    def get_sfps(self, host, device):
        try:
            sfps_data = []
            sfps = device.send_command("debug fastpath cfgtool --dump.sfp", textfsm_template='app/pullers/ntc-templates/ntc_templates/templates/cisco_wlc_ssh_debug_fastpath_cfgtool_dumpsfp.textfsm',  use_textfsm = True)

            
            for inv in sfps:
                port_type= re.findall(r'\(.*\)|\s*(.*)\s*', inv['transceiver_type'])
                port_type = list(filter(None, port_type))
                if ("NOT_SUPPORTED" not in inv['transceiver_type']):
                    sfp_data = {'port_name': inv['port'],
                                'mode': '',
                                'speed': '',
                                'hw_version': inv['rev'],
                                'serial_number': inv['sn'].lstrip('0'),
                                'port_type': port_type[0],
                                'connector': '',
                                'wavelength':'',
                                'optical_direction_type':'',
                                'pn_code':inv['pid'],
                                'status':'',
                                'description': '',
                                'manufacturer': inv['vendor'],
                                'media_type': ''}
                    sfps_data.append(sfp_data)

            self.inv_data[host['ip_address']].update({"sfp":sfps_data})
        except Exception as e:
            print(f"SFPs error occured {e}", file=sys.stderr)
            self.inv_data[host['ip_address']].update({"sfp":[]})


    def get_license(self, host, device):
        try:
            print("Getting license")
            license = device.send_command('show license all', use_textfsm=True)
            all_license = []
            for lic in license:
                if lic['feature']:
                    all_license.append({
                                        "name": lic['feature'],
                                        "description": lic['feature'],
                                        "activation_date": None,
                                        "expiry_date": lic['period_left'],
                                        "grace_period": None,
                                        "serial_number": None,
                                        "status": 'production' if 'Active' in lic['state'] else 'decommissioned',
                                        "capacity": None,
                                        "usage": None,
                                        "pn_code": None
                                    })
            self.inv_data[host['ip_address']].update({"license":all_license})
        except Exception:
            print("License not found", file=sys.stderr)
            self.inv_data[host['ip_address']].update({"license":[]})
        
    def get_aps(self, host, device):
        # dfObj = pd.DataFrame(columns=['IP', 'AP Name', 'Serial Number',	'PN Code',	'Hardware Version',	'Software Version',	'Description',	'Manufecturer'])
        obj_in=0
        try:
            print("Getting Aps data", file=sys.stderr)
            all_aps=[]
            print("Sending command: show ap summary", file=sys.stderr)
            ap_summary = device.send_command('show ap summary', use_textfsm=True)
            print("Sending command: show ap inventory all", file=sys.stderr)
            ap_inv = device.send_command('show ap inventory all', use_textfsm=True)
            print("Sending command: show ap image all", file=sys.stderr)
            ap_image = device.send_command('show ap image all', use_textfsm=True)
            print(f"@@@@ AP Sumary: {ap_summary}",file=sys.stderr)
            print(f"@@@@ AP Inv: {ap_inv}",file=sys.stderr)
            print(f"@@@@ AP Img: {ap_image}",file=sys.stderr)
            for s in ap_summary:
                for inv in ap_inv:
                    if inv['ap_name'].strip()==s['ap_name'].strip():
                        for ver in ap_image:
                            if ver['ap_name'].strip()==s['ap_name'].strip():
                                # all_aps.append({'aps':
                                ap_data = {'ip_addr': s['ip'], 
                                    'ap_name':s['ap_name'],
                                    'serial_number': inv['sn'], 
                                    'pn_code': s['ap_model'], 
                                    'hw_version': inv['vid'], 
                                    "software_version": ver['primary_image'], 
                                    "desc": inv['description'], 
                                    "max_power": None, 
                                    "manufecturer": "Cisco", 
                                    "status": "production", 
                                    "authentication": None}
                                # dfObj.loc[obj_in,'IP'] = s['ip']
                                # dfObj.loc[obj_in, 'AP Name'] = s['ap_name']
                                # dfObj.loc[obj_in,'Serial Number'] = inv['sn']
                                # dfObj.loc[obj_in,'PN Code'] =  s['ap_model']
                                # dfObj.loc[obj_in,'Hardware Version'] =  inv['vid']
                                # dfObj.loc[obj_in,'Software Version'] = ver['primary_image'] 
                                # dfObj.loc[obj_in,'Description'] = inv['description']
                                # obj_in+=1
                                # if s['ip'] not in self.inv_data:
                                #     self.inv_data[s['ip']] = {}
                                # self.inv_data[s['ip']].update({"aps":all_aps})
                                
                                # self.inv_data[s['ip']].update({'status': 'success'})
                                # self.inv_data[s['ip']].update({'board': []})
                                # self.inv_data[s['ip']].update({'sfp': []})
                                # self.inv_data[s['ip']].update({'license': []})
                                # self.inv_data[s['ip']].update({'sub_board': []})
                                self.addInventoryToDB(host, ap_data)
                                break #ap_image loop breal
                        break #ap_inv loop break
            print(f"%%%%%%%%%%%%%%",self.inv_data,file=sys.stderr)
            # rand= random.randint(0,100)
            # ip=host['ip_address']
            # writer = pd.ExcelWriter(f'temp/WLC1 {ip}.xlsx') #, engine='xlsxwriter')
            # # write dataframe to excel
            # dfObj.to_excel(writer, sheet_name='Ap1')
            # writer.save()
            # print('DataFrame is written successfully to Excel File.', file=sys.stderr)  
            # self.inv_data[host['ip_address']].update({"aps":all_aps})
        except Exception as e:
            print("Aps data not found", file=sys.stderr)
            traceback.print_exc()
            self.inv_data[host['ip_address']].update({"aps":[]})

if __name__ == '__main__':
    hosts = [
        {
            "ip_address": "10.64.252.92",
            "device_type": "cisco-wlc",
            "username": "ednbo",
            "password": "KsaEDN#$$789$B"
        }
        ]
    print('Started at: '+datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    puller = WLCPuller()
    print(puller.get_inventory_data(hosts))