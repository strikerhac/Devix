from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app.api.v1.monitoring.device.utils.monitoring_utils import *
from app.api.v1.monitoring.device.utils.alerts_utils import *
from app.api.v1.monitoring.device.utils.puller_utils import *
from app.api.v1.monitoring.device.utils.common_puller import *
from app.api.v1.monitoring.device.utils.ping_parse import *
import sys
import traceback
from datetime import  datetime
import threading
from app.api.v1.monitoring.device.utils.scheduler import *



router = APIRouter(
    prefix="/monitoring_scheduler",
    tags=["monitoring_scheduler"]
)

scheduler = Scheduler()

def job_to_execute():
    print("jon executed at:::",datetime.now(),file=sys.stderr)


scheduler.add_job(
    func=job_to_execute,
    trigger=CronTrigger(hour=12, minute=27),
    id='job_two'
)

def GenerateAlertMail():
    pass




monitoring_status = {"is_running": False}
def create_monitoring_poll(devicePoll):
    try:
        threads = []
        for host in devicePoll:
            print("host in create monitoring poll is:::::::::::::",host,file=sys.stderr)
            Obj = CommonPuller()
            print("Obj for the monitoring poll is::::::::::::::::::::",Obj,file=sys.stderr)
            thread = threading.Thread(
                target=Obj.poll,
                args=(host,)
            )
            print("thread is:::::::::::::::::",thread,file=sys.stderr)
            thread.start()
            threads.append(thread)

        for th in threads:
            th.join()
    except Exception as e:
        traceback.print_exc()
        print("Error While Creating Monitoring POll",str(e))


def monitoring_operations():
    try:
        # iterations= 1
        # while True:
        #     print(f"Iteration : {iterations}",file=sys.stderr)
        #     iterations = iterations + 1
        #
        #     if iterations == 100000:
        #         iterations = 1

        # Generating Alerts
        print(f"Running Monitoring Scheduler::",file=sys.stderr)
        try:
            results= (
                configs.db.query(AtomTable,Monitoring_Devices_Table,Monitoring_Credentails_Table
                ).join(
                    AtomTable,AtomTable.atom_id == Monitoring_Devices_Table.atom_id
                ).join(
                    Monitoring_Credentails_Table,
                    Monitoring_Credentails_Table.monitoring_credentials_id == Monitoring_Devices_Table.monitoring_credentials_id,
                ).all()
            )
            print(" result in monitoring scheduler is::::::::::::",results,file=sys.stderr)

            devicePolls = []
            for result in results:
                atom, monitoring_device, credentials = result
                print("result is::::::::::::::::",result,file=sys.stderr)
                print(f"Atom Is:: {atom}, MOnitoring device is {monitoring_device},credentials are {credentials}",file=sys.stderr)
                try:
                    if credentials is None:
                        print(
                            f"{atom.ip_address} : Error - No SNMP Credentials",
                            file=sys.stderr
                        )
                    else:
                        devicePolls.append(result)
                except Exception as e:
                    traceback.print_exc()
            try:
                create_monitoring_poll(devicePolls)
            except Exception as e:
                traceback.print_exc()
        except Exception as e:
            traceback.print_exc()
    except Exception as e:
        print("Error In Monitoring Scheduler:::",str(e),file=sys.stderr)
        traceback.print_exc()


def running_active_devices():
    global monitoring_status
    try:

        monitoringThread = threading.Thread(target=monitoring_operations)
        print("Monitoring thread is::::::::::::::",monitoringThread,file=sys.stderr)
        print("thread activated::::::::::::::",file=sys.stderr)
        monitoringThread.start()
        monitoring_status["is_running"] = True
    except Exception as e:
        traceback.print_exc()
        print("Error WHile running active devices",str(e))
        monitoring_status["is_running"] = False


@router.get('/run_active',
            responses = {
                200:{"model":str},
                500:{"model":str}
            },
            description="Use this api to start monitoring",
            summary="Use this api to start the monitoring"
)
async def run_active_devices():
    try:
        success_list = []
        error_list =[]
        data = []
        print("\n\nMonitoring Started\n\n",file=sys.stderr)
        running_active_devices()
        if monitoring_status["is_running"]:
            result =get_monitoring_data()
            print("result fr the run active is:::",result,file=sys.stderr)
            data.append(result)
            success_list.append("Monitoring Has Been Started")
        else:
            error_list.append("Error in start monitoring")
        responses = {
            "data":data,
            "success_list":success_list,
            "error_list":error_list,
            "success":len(success_list),
            "error":len(error_list)
        }
        return responses

    except Exception as e:
        print("Error Occured While Monitoring Active",str(e),file=sys.stderr)
        traceback.print_exc()
        print("Error oCcured while run active devices",str(e))
        return JSONResponse(content="Error While Monitoring Startup",status_code=500)

def get_monitoring_data():
    try:
        monitoring_device_data = {}
        monitoring_device_query = configs.db.query(Monitoring_Devices_Table).all()
        if monitoring_device_query:
            for data in monitoring_device_query:
                atom_device_query = configs.db.query(AtomTable).filter_by(atom_id = data.atom_id).first()
                if atom_device_query:
                    monitoring_device_data['ip_address'] = atom_device_query.ip_address
                    monitoring_device_data['function'] = atom_device_query.function
                    monitoring_device_data['vendor'] = atom_device_query.vendor
                    monitoring_device_data['device_type'] = atom_device_query.device_type
                    monitoring_device_data['device_name'] = atom_device_query.device_name
                else:
                    print("No Atom device found",file=sys.stderr)
                monitoring_credentials_query = configs.db.query(Monitoring_Credentails_Table).filter_by(monitoring_credentials_id = data.monitoring_credentials_id).first()
                if monitoring_credentials_query:
                    monitoring_device_data['credentials'] = monitoring_credentials_query.category+"-"+monitoring_credentials_query.profile_name
                else:
                    print("Monitoring credentials notfound::::",file=sys.stderr)
                monitoring_device_data['snmp_status'] = data.snmp_status
                monitoring_device_data['ping_status'] = data.ping_status
                monitoring_device_data['active'] = data.active
                monitoring_device_data['source'] = data.source
        return monitoring_device_data


    except Exception as e:
        traceback.print_exc()
        print("Error in get monitoring_data::::",str(e))

# host = ['0', '192.168.0.2', 'fortinet', '3', '4', '5', '6', '7', '8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'public', '161']
# host = ['0', '192.168.10.36', 'cisco_ios', '3', '4', '5', '6', '7', '8', '9', '10',
#         '11', '12', '13', 'v3', '15', '16', '17', '18', 'public', '161','NETS','NETSAUTH','NETSENCR','SHA','AES']
# host = ['0', '192.168.0.55', 'cisco_ios_xe', '3', '4', '5', 'Cisco', 'Switch', '8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'NetsDevTeam@2021', '161']
# host = ['0', '192.168.0.5', 'cisco_ios', '3', '4', '5', 'Cisco', 'Switch', '8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'NetsDevTeam@2021', '161']
# host = ['0', '192.168.18.126', 'Windows', '3', '4', '5', 'Microsoft', 'VM','8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'public', '161']
# host = ['0', '10.212.134.202', 'Windows', '3', '4', '5', 'Microsoft', 'VM','8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'public', '161']
# host = ['0', '10.68.3.5', 'extream', '3', '4', '5', '6', '7', '8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'ReadOnlyAtheeb_MPLS', '161']
# host = ['0', '91.147.128.26', 'cisco_ios', 'Edge_Ro-1', '4', '5', '6', '7', '8', '9', '10',
#         '11', '12', '13', 'v1/v2', '15', '16', '17', '18', 'public', '161']
host = [
    "0",
    "192.168.10.36",
    "cisco_ios",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "v3",
    "15",
    "16",
    "17",
    "18",
    "public",
    "161",
    "nets",
    "netsauth",
    "netsencr",
    "SHA-128",
    "AES",
]


@router.post('/test_puller',
             responses = {
                 200:{"model":str},
                 500:{"model":str}
             },
             description="Test puller API",
             summary="Test puller api"
)
async def test_puller():
    try:
        puller = CommonPuller()
        puller.poll(host)
        # queryString = f"select * from alerts_table;"
        # results = db.session.execute(queryString)
        # for result in results:
        #     difference = datetime.now() - result[8]
        #     print(result[8])
        #     print(difference.total_seconds())

        # queryString = f"select * from monitoring_devices_table where active='Active';"
        # results = db.session.execute(queryString)

        # for result in results:
        #     try:

        #         community_string = f"select * from monitoring_credentials_table where profile_name='{result[4]}';"
        #         community_result = db.session.execute(community_string)
        #         community = None
        #         for communityv in community_result:
        #             community = communityv[:]

        #         result = list(result) + list(community)

        #         if community is not None:
        #             creatMonitoringPoll(CommonPuller,result)
        #         else:
        #             print(f"{result[1]}: Error : No SNMP Credentials")
        return JSONResponse(content="Test Puller Exceuted",status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content = "Error In Test Puller",status_code=500)


@router.get('/ping_test',responses={
    200:{"model":str},
    500:{"model":str}
})
async def ping_testing():
    try:
        monitoringDevice = configs.db.query(Monitoring_Devices_Table).all()
        for devices in monitoringDevice:
            atom_exsist = configs.db.query(AtomTable).filter_by(atom_id = devices.atom_id).first()
            if atom_exsist:
                ipaddress = atom_exsist.ip_address.strip()
                print("ip address in pring test is::::::::::::::",ipaddress,file=sys.stderr)
                status = ping(ipaddress)
                print("ip address is:::"+ipaddress+ " : "  + status,file=sys.stderr)
                devices.ping_status = status
                UpdateDBData(monitoringDevice)
        return JSONResponse(content="Ping tested Executed",status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content = "Error in Ping test is",status_code=500)

def alarm_operations():
    try:
        print(f"Data Fetching for Alarm devices:::",file=sys.stderr)
        monitoring_alerts = configs.db.query(Monitoring_Alerts_Table).all()
        for alerts in monitoring_alerts:
            alert_manage(alerts)
    except Exception as e:
        traceback.print_exc()

def alert_manage(alert):# (`IP_ADDRESS`,`DESCRIPTION`,,`ALERT_TYPE`,`MAIL_STATUS`,`DATE`)
    try:
        if alert[3] == "memory" or alert[3] == "cpu":
            temptime = datetime.strptime(
                (str(datetime.now()).split(".")[0]), "%Y-%m-%d %H:%M:%S"
            ) - datetime.strptime(alert[4], "%Y-%m-%d %H:%M:%S")
            time = temptime.total_seconds() / 60

            if time >= 5:
                if alert[2] == "critical" and alert[3] == "no":
                    query1 = configs.db.query(AtomTable).filter_by(ip_address=alert[1]).first()
                    if query1:
                        query2 = configs.db.query(Monitoring_Devices_Table).filter_by(atom_id=query1.atom_id).first()
                        if query2:
                            query3 = configs.db.query(Monitoring_Alerts_Table).filter_by(monitoring_device_id=query2.monitoring_device_id).first()
                            if query3:
                                query3.alert_type = "yes"
                                UpdateDBData(query3)  # Commit changes to the database

        if alert[3] == "device_down":
            if alert[3] == "no":
                query1 = configs.db.query(AtomTable).filter_by(ip_address=alert[1]).first()
                if query1:
                    query2 = configs.db.query(Monitoring_Devices_Table).filter_by(atom_id=query1.atom_id).first()
                    if query2:
                        query3 = configs.db.query(Monitoring_Alerts_Table).filter_by(monitoring_device_id=query2.monitoring_device_id).first()
                        if query3:
                            query3.mail_status = "yes"
                            UpdateDBData(query3)  # Commit changes to the database

    except Exception as e:
        traceback.print_exc()