import sys
import threading
import traceback
# from app import db
from datetime import datetime

# from app.models.inventory_models import FIREWALL_VIP
from app.utils.db_utils import *
from netmiko import Netmiko


class FORTIGATEVIP(object):

    def __init__(self):
        self.connections_limit = 50
        self.failed_devices = []

    def FormatStringDate(self, date):
        # print(date, file=sys.stderr)
        try:

            if date is not None:
                result = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                return result

        except:
            result = datetime(2000, 1, 1)
            print("date format exception", file=sys.stderr)
            return result

    def InsertDBData(obj):
        try:
            configs.db.add(obj)
            configs.db.commit()
            return 200
        except Exception as e:
            configs.db.rollback()
            traceback.print_exc()
            print(
                f"Something else went wrong in Database Insertion: {e}", file=sys.stderr)
        return 500

    def UpdateDBData(obj):
        try:
            configs.db.flush()

            configs.db.merge(obj)
            configs.db.commit()
            return 200
        except Exception as e:
            configs.db.rollback()
            traceback.print_exc()
            print(
                f"Something else went wrong during Database Update: {e}", file=sys.stderr)
            return 500

    def addInventoryToDB(self, host, firewallVipData):
        # for ednExchange in ednExchange_data:

        for firewallVip in firewallVipData:
            try:
                firewallVipDb = FIREWALL_VIP()
                firewallVipDb.ip_address = host['ip_address']
                firewallVipDb.device_name = host['device_name']
                firewallVipDb.internal_ip = firewallVip.get('internal_ip')
                firewallVipDb.vip = firewallVip.get('vip')

                firewallVipDb.sport = firewallVip.get('sport')
                firewallVipDb.dport = firewallVip.get('dport')
                firewallVipDb.extintf = firewallVip.get('extintf')

                firewallVipDb.creation_date = host['time']
                firewallVipDb.modification_date = host['time']
                self.InsertDBData(firewallVipDb)
                print('Successfully added to the Database', file=sys.stderr)

            except Exception as e:
                # db.session.rollback()
                self.add_to_failed_devices(host['ip_address'], f"Failed to insert Data to DB " + str(e))
                print(f"Error while inserting data into DB {e}", file=sys.stderr)
                # self.add_to_failed_devices(host['ip_address'], f"Failed to insert Data to DB "+str(e))

    def get_inventory_data(self, hosts):
        threads = []
        for host in hosts:
            th = threading.Thread(target=self.poll, args=(host,))
            th.start()
            threads.append(th)
            if len(threads) == self.connections_limit:
                for t in threads:
                    t.join()
                threads = []

        else:
            for t in threads:  # if request is less than connections_limit then join the threads and then return data
                t.join()
            return ""

    def poll(self, host):
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 10
        c = 0
        is_login = False
        sw_type = str(host['sw_type']).lower()
        sw_type = sw_type.strip()
        while c < login_tries:
            try:
                device_type = host['sw_type']
                device = Netmiko(host=host['ip_address'], username=host['user'], password=host['pwd'],
                                 device_type=device_type, timeout=600, global_delay_factor=2)
                print(f"Success: logged in {host['ip_address']}")
                is_login = True
                break
            except Exception as e:
                c += 1
                login_exception = str(e)

        if is_login == False:
            print(f"Falied to login {host['ip_address']}", file=sys.stderr)
            pass
            # print(f"Falied to login {host['ip_address']}", file=sys.stderr)
            # self.add_to_failed_devices(host['ip_address'], "Failed to login to host")
            # self.add_failed_devices_to_db(host, f"Failed To Login")
            # #failedDB

        if is_login == True:
            print(f"Successfully Logged into Device {host['ip_address']}", file=sys.stderr)

            try:
                vipData = []
                print("Getting VIP", file=sys.stderr)
                vips = device.send_command('show firewall vip',
                                           textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/fortigate_show_firewall_vip.textfsm",
                                           use_textfsm=True)
                print(f"Vips are: {vips}", file=sys.stderr)
                if isinstance(vips, str):
                    vips = []
                    print(f"VIP for {host['ip_address']} not found {vips} ", file=sys.stderr)
                    raise Exception(f"VIP data not found " + str(vips))

                try:
                    print("Parsing Data", file=sys.stderr)
                    for vip in vips:
                        vipObj = {}

                        vipObj['internal_ip'] = vip['internal_ip']
                        vipObj['vip'] = vip['vip']
                        vipObj['sport'] = vip['sport']
                        vipObj['dport'] = vip['dport']
                        vipObj['extintf'] = vip['extintf']

                        vipData.append(vipObj)
                except Exception as e:
                    print("Exception in Parsing Data", file=sys.stderr)

                print("Puller Finished", file=sys.stderr)
                self.addInventoryToDB(host, vipData)
                print(vipData, file=sys.stderr)
            except Exception as e:
                traceback.print_exc()
                print(f"Error Occured in Getting VIP Data {e}", file=sys.stderr)

    def getFirewallVip(self, devices):
        puller = FORTIGATEVIP()
        hosts = []
        for device in devices:
            host = {
                "device_name": device["device_name"],
                "ip_address": device["ip_address"],
                "user": device["username"],
                "pwd": device["password"],
                "sw_type": device["device_type"],
                'time': self.FormatStringDate(device["time"]),

            }
            hosts.append(host)

        puller.get_inventory_data(hosts)
        print("Firewall VIP Fetch Completed", file=sys.stderr)


if __name__ == '__main__':
    hosts = []

    host = {
        "ip_address": "192.168.0.2",
        "user": "admin",
        "pwd": "Pakistan1947@#!",
        "sw_type": "fortinet"
    }
    # poll(host)

