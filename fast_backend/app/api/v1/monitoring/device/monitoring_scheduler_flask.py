from app.monitoring_device.monitoring_utils import *
from app.monitoring_device.common_puller import CommonPuller
from flask_apscheduler import APScheduler
from app import app, db
import sys

from datetime import datetime
from flask import request

import traceback
import threading


scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


def GenerateAlertMails():
    from datetime import datetime, timedelta
    from app.mail import send_mail

    print("\n### Generating Mails For Monitoring Alerts ###\n", file=sys.stderr)
    try:
        mailQuery = "select * from mail_credentials where status = 'active'"
        mail_cred = db.session.execute(mailQuery).fetchone()
        if mail_cred is None:
            return
        mail_cred = dict(mail_cred)
        print("\n---> Active Mail Credentials <---\n", file=sys.stderr)
        print(mail_cred, file=sys.stderr)

        query = "select * from alert_recipents_table where `CATEGORY`='Monitoring' and `STATUS`='Active';"
        recipents = []

        try:
            results = db.session.execute(query)
            for row in results:
                recipents.append(row[1])
        except Exception as e:
            traceback.print_exc()
            print(e, file=sys.stderr)

        print(f"Recipents : {recipents}", file=sys.stderr)

        # query = f"select * from alerts_table where DATE >= '{datetime.now()- timedelta(minutes=60)}' and MAIL_STATUS = 'no' and (ALERT_TYPE='critical' or CATEGORY = 'device_down');"
        query = f"select * from alerts_table where MAIL_STATUS = 'no' and (ALERT_TYPE='critical' or CATEGORY = 'device_down');"
        results = db.session.execute(query)

        # print(f"Total Alerts : {len(results)}", file=sys.stderr)

        for row in results:
            print(
                f"-----> Sendig Mail for alert id = {row[0]} <------\n", file=sys.stderr
            )

            try:
                # recipents = [
                # 'najam.hassan@nets-international.com',
                # 'hamza.zahid@nets-international.com',
                # 'muhammad.naseem@nets-international.com',
                # 'usama.islam@nets-international.com'
                # ]

                subject = f"MonetX - Monitoring Alert - {row[3]} | {row[4]}"
                msg = f"""
                Alert ID : {row[0]}\n
                IP Address : {row[1]}\n
                Description : {row[2]}\n
                Alert Type : {row[3]}\n
                Category : {row[4]}\n
                Alert Status : {row[5]}\n
                Date/Time : {row[8]}
                """

                # sending email
                print(
                    f"-----> Sendig Mail for alert id = {row[0]} <------\n",
                    file=sys.stderr,
                )

                send_mail(
                    send_from=mail_cred["MAIL"],
                    send_to=recipents,
                    subject=subject,
                    message=msg,
                    username=mail_cred["MAIL"],
                    password=mail_cred["PASSWORD"],
                    server=mail_cred["SERVER"],
                )

                query = f"update alerts_table set mail_status='yes' where alert_id = {row[0]};"
                db.session.execute(query)
                db.session.commit()

            except Exception as e:
                print("\n*** ERROR In Mail Generation ***\n", file=sys.stderr)
                traceback.print_exc()
                print(f"\n{e}\n", file=sys.stderr)

    except Exception as e:
        print("\n*** ERROR In Mail Generation ***\n")
        traceback.print_exc()
        print(f"\n{e}\n", file=sys.stderr)


def creatMonitoringPoll(devicePoll):
    threads = []
    for host in devicePoll:
        obj = CommonPuller()
        th = threading.Thread(target=obj.poll, args=(host,))
        th.start()
        threads.append(th)

    for thread in threads:
        thread.join()


def MonitoringOperations():
    iteration = 1
    while True:
        print(f"\n\n\n** Iteration : {iteration} **\n\n\n", file=sys.stderr)
        iteration = iteration + 1

        if iteration == 100000:
            iteration = 1

        # GenerateAlertMails()
        print(f"Running Monitoring Schedular\n", file=sys.stderr)

        try:
            results = (
                db.session.query(
                    Atom_Table, Monitoring_Devices_Table, Monitoring_Credentails_Table
                )
                .join(
                    Atom_Table, Atom_Table.atom_id == Monitoring_Devices_Table.atom_id
                )
                .join(
                    Monitoring_Credentails_Table,
                    Monitoring_Credentails_Table.monitoring_credentials_id
                    == Monitoring_Devices_Table.monitoring_credentials_id,
                )
                .all()
            )

            devicePoll = []
            for result in results:
                atom, monitoring_device, credentials = result
                try:
                    if credentials is None:
                        print(
                            f"{atom.ip_address} : Error - No SNMP Credentials",
                            file=sys.stderr,
                        )
                    else:
                        devicePoll.append(result)
                except Exception as e:
                    traceback.print_exc()

            try:
                creatMonitoringPoll(devicePoll)
                # GenerateAlertMails()
            except Exception:
                traceback.print_exc()

            # queryString1 = f"select * from alerts_table;"
            # alerts = db.session.execute(queryString1)
            # for alert in alerts:
            #     alert_manage(alert)
            # AlarmOperations()

        except Exception as e:
            print("Error in Monitoring Scheduler: ", str(e), file=sys.stderr)
            traceback.print_exc()


def RunningActiveDevices():
    # @scheduler.task('interval', id="testingpolls", seconds=300)
    try:
        monitoringThread = threading.Thread(target=MonitoringOperations)
        monitoringThread.start()
    except Exception:
        traceback.print_exc()


@app.route("/runa_ctive", methods=["GET"])
# @token_required
def runactivedevice():
    try:
        print("\n\nMonitoring Started\n\n", file=sys.stderr)
        RunningActiveDevices()
        return "Monitoring Has Been Started"
    except Exception as e:
        print("Error While Starting Monitoring", file=sys.stderr)
        error = "Something Went Wrong:", type(e).__name__, str(e)
        return error


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


@app.route("/test_puller", methods=["GET"])
def TestPuller():
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

    #     except Exception as e:
    #         traceback.print_exc()
    return "OK", 200


@app.route("/ping_test", methods=["GET"])
def PingShed():
    queryString = f"select ip_address from monitoring_devices_table;"
    results = db.session.execute(queryString)
    status = None
    for result in results:
        ip_address = result[0].strip()
        status = ping(ip_address)
        print(ip_address + " : " + status, file=sys.stderr)
        updatequery = f"update monitoring_devices_table set status = '{status}' where ip_address='{ip_address}';"
        db.session.execute(updatequery)
        db.session.commit()
    return "OK", 200


#
#
#
#
#
#
#
#
#
#


@app.route("/alarm_active")
# @token_required
def alarmactivedevice():
    try:
        # host = request.get_json()

        print(" I am in try block  of alarmactivedevices", file=sys.stderr)
        return "operation sucssesfull"
    except Exception as e:
        print(" I am in excp block  of alarmactivedevices", file=sys.stderr)

        error = "Something Went Wrong:", type(e).__name__, str(e)
        return error


def AlarmOperations():
    print(f"Data Fetching for alarms devices", file=sys.stderr)

    try:
        queryString = f"select * from alerts_table;"
        results = db.session.execute(queryString)
        for result in results:
            alert_manage(result)

    except Exception as e:
        error = "Something Went Wrong:", type(e).__name__, str(e)
        print(" I am in excp block  of alarm scheduler", error, file=sys.stderr)
        return error


# def alarms():
#         @scheduler.task('interval', id="testingalrams", seconds=60)#
#         Ala


def alert_manage(
    alert,
):  # (`IP_ADDRESS`,`DESCRIPTION`,,`ALERT_TYPE`,`MAIL_STATUS`,`DATE`)
    try:
        if alert[3] == "memory" or alert[3] == "cpu":
            temptime = datetime.strptime(
                (str(datetime.now()).split(".")[0]), "%Y-%m-%d %H:%M:%S"
            ) - datetime.strptime(alert[4], "%Y-%m-%d %H:%M:%S")
            time = temptime.total_seconds() / 60

            # if time > 5:
            #         # if alert[2]=="informational":
            #         #         des = f"""An automated alarm generated,{alert[0]} is utilizing more than 70% of cpu."""
            #         #         sqlquery = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`MAIL_STATUS`,`DATE`) values ('{alert[0]}','{des}','informal','no','{datetime.now()}');"
            #         #         db.session.execute(sqlquery)
            #         if  alert[2]=="informational" and alert[3]=="no":
            #                 #enter send mail function
            #                 des = f"""An automated alarm generated,{alert[0]} is utilizing more than 70% of cpu."""
            #                 sqlquery = f"insert into alerts_table (`IP_ADDRESS`,`DESCRIPTION`,`ALERT_TYPE`,`MAIL_STATUS`,`DATE`) values ('{alert[0]}','{des}','(critical','yes','{datetime.now()}');"
            #                 db.session.execute(sqlquery)
            if time >= 5:
                if alert[2] == "critical" and alert[3] == "no":
                    # enter send mail function
                    sqlquery = f"update alerts_table set alert_type='yes' where ip_address='{alert[1]}';"
                    db.session.execute(sqlquery)
                    sqlquery = f"update alerts_table set alert_type='yes' where ip_address='{alert[1]}';"
                    db.session.execute(sqlquery)

        if alert[3] == "device_down":
            if alert[3] == "no":
                # enter send mail function
                sqlquery = f"update alerts_table set mail_status='yes' where ip_address='{alert[1]}';"
                db.session.execute(sqlquery)
    except Exception as e:
        error = "Something Went Wrong:", type(e).__name__, str(e)
        print(error, file=sys.stderr)
        return error
