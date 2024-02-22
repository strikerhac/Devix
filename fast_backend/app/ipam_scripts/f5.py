import sys
import threading
import traceback
# from app import db
from datetime import datetime

# from app import db
# from app.models.inventory_models import F5 as F5DB
from app.utils.db_utils import *
from netmiko import Netmiko
from app.models.ipam_models import F5 as F5DB


class F5(object):
    print("F5 is started execution:::::::::::::::::::::::::::::::::::::::::::::::", file=sys.stderr)

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

    def addInventoryToDB(self, host, f5Data):
        # for ednExchange in ednExchange_data:
        print('host is:::::::::::::::::::::', host, file=sys.stderr)
        print("f5data::::::::::::::::::::::::::::::::", f5Data, file=sys.stderr)

        for f5 in f5Data:
            print("f5 is:::::::::::::::::::::::::::::", f5, file=sys.stderr)
            try:
                f5Db = F5DB()
                f5Db.ip_address = host['ip_address']
                f5Db.device_name = host['device_name']
                f5Db.vserver_name = f5.get('vserver_name')
                f5Db.vip = f5.get('vip')

                f5Db.pool_name = f5.get('pool_name')
                f5Db.pool_member = f5.get('pool_member')
                f5Db.service_port = f5.get('service_port')
                f5Db.node = f5.get('node')
                f5Db.monitor_value = f5.get('monitor_value')
                f5Db.monitor_status = f5.get('monitor_status')
                f5Db.lb_method = f5.get('lb_method')

                f5Db.creation_date = host['time']
                f5Db.modification_date = host['time']
                # InsertDBData
                InsertDBData(f5Db)
                print('Successfully added to the Database:::::::::::::::::::::', file=sys.stderr)

            except Exception as e:
                # db.session.rollback()
                print(f"Error while inserting data into DB {e}", file=sys.stderr)

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
        print("poll function is being executed::::::::::::::::::::::::::::::", file=sys.stderr)
        print("host os:::::::::::",host,file=sys.stderr)
        print(f"Connecting to {host['ip_address']}", file=sys.stderr)
        login_tries = 10
        c = 0
        is_login = False
        sw_type = str(host['device_type']).lower()
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

            # #failedDB

        if is_login == True:
            print(f"Successfully Logged into Device {host['ip_address']}", file=sys.stderr)

            try:
                vips = members = lbMode = monitorValue = []
                monitor = pool = lb_mode = monitor_value = ""
                f5Data = []
                print("Getting VIP", file=sys.stderr)
                vips = device.send_command('list ltm virtual all destination',
                                           textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/f5_ltm_list_ltm_virtual_all_destination.textfsm",
                                           use_textfsm=True)
                print(f"Vips are: {vips}", file=sys.stderr)
                if isinstance(vips, str):
                    vips = []
                    print(f"VIP for {host['ip_address']} not found {vips} ", file=sys.stderr)
                    raise Exception(f"VIP data not found " + str(vips))

                for vip in vips:

                    try:
                        print(f"Getting Pool for VIP {vip['vserver']}", file=sys.stderr)
                        poolObj = device.send_command(f"list ltm virtual {vip['vserver']}",
                                                      textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/f5_ltm_list_ltm_virtual_pool.textfsm",
                                                      use_textfsm=True)
                        if isinstance(poolObj, str):
                            pool = ""
                            print(f"Pool for {host['ip_address']} not found  ", file=sys.stderr)

                        else:
                            print(f"Pool is: {poolObj}", file=sys.stderr)
                            pool = poolObj[0].get('pool_name')

                    except Exception as e:
                        print(f"Exception Occurred in Getting Pool {e}", file=sys.stderr)

                    try:

                        print(f"Getting Pool Members for {pool}", file=sys.stderr)
                        members = device.send_command(f"list ltm pool {pool}",
                                                      textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/f5_ltm_list_ltm_pool_members.textfsm",
                                                      use_textfsm=True)
                        # print(f"Member is: {members}", file=sys.stderr)
                        if isinstance(members, str):
                            members = []
                            # print(f"Members for {host['ip_address']} not found", file=sys.stderr)

                        else:
                            if len(monitor) > 0:
                                if members[-1].get('monitor'):
                                    monitor = members[-1].get('monitor')
                                    del members[-1]
                                    for dic in members:
                                        print(monitor)
                                        dic["monitor"] = monitor

                        print(f"Member is: {members}", file=sys.stderr)
                    except Exception as e:
                        print(f"Exception Occurred in Getting Pool Members{e}", file=sys.stderr)

                    try:
                        print(f"Getting LB Modes for {pool}", file=sys.stderr)
                        lbMode = device.send_command(f"list ltm pool {pool} load-balancing-mode",
                                                     textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/f5_ltm_list_pool_load_balancing_mode.textfsm",
                                                     use_textfsm=True)
                        if isinstance(lbMode, str):
                            lbMode = []
                            # print(f"Members for {host['ip_address']} not found", file=sys.stderr)
                        else:
                            lb_mode = lbMode[0]['lb_mode']
                            print(f"LB Mode is: {lbMode}")
                    except Exception as e:
                        print(f"Exception Occurred in Getting LB Modes {e}", file=sys.stderr)

                    try:
                        if monitor:
                            print(f"Getting Monitor Value for {monitor}", file=sys.stderr)
                            monitorValue = device.send_command(f"list ltm monitor tcp {monitor}",
                                                               textfsm_template="app/pullers/ntc-templates/ntc_templates/templates/f5_ltm_list_pool_load_balancing_mode.textfsm",
                                                               use_textfsm=True)
                            if isinstance(monitorValue, str):
                                monitorValue = []
                                # monitorValue(f"Members for {host['ip_address']} not found", file=sys.stderr)
                            else:
                                monitor_value = monitorValue[0][monitor_value]
                                print(f"Monitor Value: {monitorValue}")
                    except Exception as e:
                        print(f"Exception Occurred in Getting Monitor Value {e}", file=sys.stderr)

                    try:
                        print("Parsing Data", file=sys.stderr)
                        for member in members:
                            f5Obj = {}
                            f5Obj['vserver_name'] = vip['vserver']

                            f5Obj['vip'] = vip['vip']
                            memberName = member['member_name']
                            memberName = memberName.split(':')
                            f5Obj['pool_name'] = pool
                            f5Obj['pool_member'] = memberName[0]
                            f5Obj['service_port'] = memberName[1]
                            f5Obj['node'] = member['node']
                            f5Obj['monitor_status'] = member['status']
                            f5Obj['lb_method'] = lb_mode
                            f5Obj['monitor_value'] = monitor_value

                            f5Data.append(f5Obj)
                    except Exception as e:
                        traceback.print_exc()
                        print(f"Exception in Parsing Data {e}", file=sys.stderr)
                self.addInventoryToDB(host, f5Data)
                # print("Puller Finished")
                print(f5Data, file=sys.stderr)
            except Exception as e:
                print(f"Error Occured in Getting F5 Data {e}", file=sys.stderr)

    def getF5(self, devices):
        puller = F5()
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
        print("F5 Fetch Completed", file=sys.stderr)


if __name__ == '__main__':
    hosts = []

    host = {
        "ip_address": "192.168.30.195",
        "user": "root",
        "pwd": "default",
        "sw_type": "f5_tmsh",
        # f5_tmsh
        # f5_ltm

    }
    F5.poll(host)
