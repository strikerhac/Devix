import sys
import traceback

from app.utils.date import get_date_helper
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import influxdb_client
from app.api.v1.monitoring.device.utils.monitoring_utils import *
from app.models.monitoring_models import *
from app.schema.monitoring_schema import *
from influxdb_client.client.util.date_utils import *
from datetime import datetime
router = APIRouter(
    prefix="/devices",
    tags=["monitoring_devices"],
)


@router.get("/get_all_monitoring_vendors", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary="Use this API in the Monitoring device page to list down the vendors which are associated in monitoring table",
description="Use this API in the Monitoring device page to list down the vendors which are associated in monitoring table"

)
async def get_all_monitoring_vendors():
    try:
        query_string = (f"SELECT vendor,COUNT(*) FROM monitoring_devices_table "
                        f"INNER JOIN atom_table ON monitoring_devices_table.atom_id = "
                        f"atom_table.atom_id  GROUP BY vendor;")
        result = configs.db.execute(query_string)

        obj_list = []
        for row in result:
            obj_dict = {"name": row[0], "value": row[1]}

            if row[0] is None:
                obj_dict["name"] = "Other"

            obj_list.append(obj_dict)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_all_monitoring_functions", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary="Use this API in Monitoring device page to display the name of device function and its value which are stored in monitoring device table ",
description= "Use this API in Monitoring device page to display the name of device function and its value which are stored in monitoring device table "
            )
async def get_all_monitoring_functions():
    try:
        query_string = (f"SELECT `function`,count(*) FROM monitoring_devices_table INNER "
                        f"JOIN atom_table ON monitoring_devices_table.atom_id = "
                        f"atom_table.atom_id GROUP BY `function`;")
        result = configs.db.execute(query_string)
        obj_list = []

        for row in result:
            objDict = {"name": row[0], "value": row[1]}
            obj_list.append(objDict)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.post("/add_monitoring_device", responses={
    200: {"model": str},
    400: {"model": str},
    500: {"model": str}
},
summary= "Use this API in motioring device table to edit the device based on the monitoring_device_id",
description="Use this API in motioring device table to edit the device based on the monitoring_device_id"
             )
async def add_monitoring_device(monitoring_obj:UpdateMonitoringDeviceSchema):
    try:

        msg = UpdateMonitoringDevice(monitoring_obj, 0, False)
        print("mesag is::::::::::::::::::::::::::::::",msg,file=sys.stderr)
        # print("status is:::::::::::::::::::::::::::::::::::::::::::::::::",status,file=sys.stderr)
        return JSONResponse(content=msg, status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.post("/add_monitoring_devices", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
})
def add_monitoring_devices(monitoring_objs):
    try:
        success_list = []
        error_list = []

        row = 0
        for monitoringObj in monitoring_objs:
            row = row + 1
            msg, status = AddMonitoringDevice(monitoringObj, row, True)

            if status == 200:
                success_list.append(msg)
            else:
                error_list.append(msg)

        responseDict = {
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        return JSONResponse(content=responseDict, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_all_monitoring_devices", responses={
    200: {"model": list[MonitoringDeviceSchema]},
    500: {"model": str}
},
summary= "Use this API in device page to list down all the device in Monitoring devices page table",
description= "Use this API in device page to list down all the device in Monitoring devices page table",
            )
async def get_all_monitoring_devices():
    try:
        monitoring_obj_list = []
        results = (
            configs.db.query(Monitoring_Devices_Table, AtomTable)
            .join(AtomTable, Monitoring_Devices_Table.atom_id == AtomTable.atom_id)
            .order_by(Monitoring_Devices_Table.creation_date.desc())  # Sorting added here
            .all()
        )

        for MonitoringObj, atom in results:
            snmp_cred = ""
            category = ""
            credentials_str = ""

            if MonitoringObj.monitoring_credentials_id is not None:
                credentials = configs.db.query(Monitoring_Credentails_Table).filter_by(
                    monitoring_credentials_id=MonitoringObj.monitoring_credentials_id
                ).first()

                if credentials:
                    snmp_cred = credentials.profile_name if credentials.profile_name else ""
                    category = credentials.category if credentials.category else ""

                    if category and snmp_cred:
                        credentials_str = category + "-" + snmp_cred
                    elif category:
                        credentials_str = category
                    elif snmp_cred:
                        credentials_str = snmp_cred

            monitoring_data_dict = {
                "monitoring_device_id": MonitoringObj.monitoring_device_id,
                "ip_address": atom.ip_address,
                "device_type": atom.device_type,
                "device_name": atom.device_name,
                "vendor": atom.vendor,
                "function": atom.function,
                "source": MonitoringObj.source,
                "profile_name": snmp_cred,
                "active": MonitoringObj.active,
                "status": MonitoringObj.ping_status,
                "credentials": credentials_str,
                "snmp_status": MonitoringObj.snmp_status,
                "ping_status": MonitoringObj.ping_status,
                "category": category,
                "monitoring_credentials_id": MonitoringObj.monitoring_credentials_id,
                "creation_date": str(MonitoringObj.creation_date),
                "modification_date": str(MonitoringObj.modification_date),
            }
            monitoring_obj_list.append(monitoring_data_dict)

        return JSONResponse(content=monitoring_obj_list, status_code=200)

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(content={"error": "Server Error While Fetching Monitoring Devices"}, status_code=500)


@router.get("/get_atom_in_monitoring", responses={
    200: {"model": list[AtomInMonitoringSchema]},
    500: {"model": str}
},
summary = "Use this API in device page while adding device to list down all the device which are in atom in Monitoring module",
description = "Use this API in device page while adding device to list down all the device which are in atom in Monitoring module",
)
async def get_atom_in_monitoring():
    try:
        monitoring_obj_list = []
        atoms = configs.db.query(AtomTable).all()

        for atom in atoms:
            monitoringDevice = configs.db.query(Monitoring_Devices_Table).filter_by(
                atom_id=atom.atom_id
            ).first()

            if monitoringDevice is None:
                monitoring_obj_list.append(
                    {
                        "atom_id":atom.atom_id,
                        "ip_address": atom.ip_address,
                        "device_name": atom.device_name,
                        "device_type": atom.device_type,
                        "vendor":atom.vendor
                    }
                )

        return JSONResponse(content=monitoring_obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Atom Data",
                            status_code=500)





@router.post("/add_atom_in_monitoring", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
},
summary="Use this API in monitoring module in device page to add device from atom",
description="Use this API in monitoring module in device page to add device from atom"
)
async def add_atom_in_monitoring(ip_list: list[AddAtomInMonitoringSchema]):
    try:
        print("type for the add atom in monitoring is:::::::", type(ip_list), file=sys.stderr)

        data = []
        success_list = []
        error_list = []

        for ip in ip_list:
            atom_id = ip.atom_id
            credentials_category = ""
            credentials_id = ip.monitoring_credentials_id
            credentials_exsists = configs.db.query(Monitoring_Credentails_Table).filter_by(monitoring_credentials_id = credentials_id).first()
            if credentials_exsists:
                credentials_category = credentials_exsists.category+"-"+credentials_exsists.profile_name
            print(f"Processing atom_id: {atom_id}, credentials_id: {credentials_id}", file=sys.stderr)

            atom = configs.db.query(AtomTable).filter_by(atom_id=atom_id).first()

            if atom is None:
                error_msg = f"{atom_id} : Device Not Found In Atom"
                error_list.append(error_msg)
                print(error_msg, file=sys.stderr)
                continue

            monitoringDevice = configs.db.query(Monitoring_Devices_Table).filter_by(atom_id=atom.atom_id).first()
            ping_response = ping(atom.ip_address)
            ping_status = ' '.join(map(str, ping_response))
            print("ping response is:::::::::::::::",ping_status,file=sys.stderr)
            if monitoringDevice is None:
                monitoringDevice = Monitoring_Devices_Table()
                monitoringDevice.atom_id = atom.atom_id
                monitoringDevice.ping_status = ping_status
                monitoringDevice.monitoring_credentials_id = credentials_id
                monitoringDevice.snmp_status = "Active"
                monitoringDevice.active = "Active"
                monitoringDevice.source = 'Atom'

                if InsertDBData(monitoringDevice) == 200:
                    print("Data Inserted to the DB", file=sys.stderr)
                    monitoring_device_dict = {
                        "monitoring_device_id": monitoringDevice.monitoring_device_id,
                        "source": monitoringDevice.source,
                        "active": monitoringDevice.active,
                        "ping_status": monitoringDevice.ping_status,
                        "active_id": monitoringDevice.active_id,
                        "device_heatmap": monitoringDevice.device_heatmap,
                        "monitoring_credentials_id": monitoringDevice.monitoring_credentials_id,
                        "snmp_status": monitoringDevice.snmp_status,
                        "ip_address":atom.ip_address,
                        "vendor":atom.vendor,
                        "function":atom.function,
                        "device_name":atom.device_name,
                        "device_type":atom.device_type,
                        "credentials":credentials_category
                    }
                    data.append(monitoring_device_dict)
                    success_msg = f"{atom_id} : Device Added Successfully"
                    success_list.append(success_msg)
                    print(success_msg, file=sys.stderr)
                else:
                    error_msg = f"{atom_id} : Error While Inserting Device"
                    error_list.append(error_msg)
                    print(error_msg, file=sys.stderr)

            else:
                error_msg = f"{atom_id} : Device Already Exist In Monitoring"
                error_list.append(error_msg)
                print(error_msg, file=sys.stderr)

        response_dict = {
            "data": data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        return JSONResponse(content=response_dict, status_code=200)

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg, file=sys.stderr)


    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Atom Data",
                            status_code=500)

@router.post('/delete_monitoring_devices',
             responses = {
                 200:{"model":str}
             })
async def delete_device_in_monitoring(ips: List[str]):
    try:
        data = []
        success_list = []
        error_list = []

        org = os.getenv("INFLUXDB_ORG", "monetx")
        bucket = os.getenv("INFLUXDB_BUCKET", "monitoring")
        delete_api = configs.client.delete_api()

        date_helper = get_date_helper()
        start = "1970-01-01T00:00:00Z"
        stop = date_helper.to_utc(datetime.now())
        for ip in ips:
            is_device_exsists = configs.db.query(AtomTable).filter_by(ip_address=ip).first()
            if is_device_exsists:
                monitoring_device_query = configs.db.query(Monitoring_Devices_Table).filter_by(atom_id = is_device_exsists.atom_id).first()
                if monitoring_device_query:
                    for measurement in ["Devices", "Interfaces"]:
                        predicate = f'_measurement="{measurement}" AND IP_ADDRESS="{ip}"'
                        delete_api.delete(start, stop, bucket=bucket, org=org, predicate=predicate)
                    data.append(monitoring_device_query.monitoring_device_id)
                    DeleteDBData(monitoring_device_query)
                    success_list.append("Device Delete successfully")
                else:
                    error_list.append("No device IP found")

        responses = {
            "data":data,
            "success_list":success_list,
            "error_list":error_list,
            "success":len(success_list),
            "error":len(error_list)
        }
        return responses
    except Exception as e :
        traceback.print_exc()

#
# @app.route("/deleteDeviceInMonitoring", methods=["POST"])
# @token_required
# def deleteAtomInMonitoring(user_data):
#     if True:
#         try::
#             from app import client
#
#             org = "monetx"
#             bucket = "monitoring"
#             delete_api = client.delete_api()
#             """
#             Delete Data
#             """
#             date_helper = get_date_helper()
#             start = "1970-01-01T00:00:00Z"
#             stop = date_helper.to_utc(datetime.now())
#             MonitoringObj = request.get_json()
#             print(
#                 "#####printing data returned by delete api",
#                 MonitoringObj,
#                 file=sys.stderr,
#             )
#             for mid in MonitoringObj:
#                 queryString = (
#                     f"DELETE FROM monitoring_devices_table WHERE IP_ADDRESS='{mid}';"
#                 )
#                 db.session.execute(queryString)
#                 db.session.commit()
#                 predicatereq1 = f'_measurement="Devices" AND IP_ADDRESS ="{mid}"'
#                 predicatereq2 = f'_measurement="Interfaces" AND IP_ADDRESS ="{mid}"'
#                 delete_api.delete(
#                     start,
#                     stop,
#                     bucket=f"{bucket}",
#                     org=f"{org}",
#                     predicate=predicatereq1,
#                 )
#                 delete_api.delete(
#                     start,
#                     stop,
#                     bucket=f"{bucket}",
#                     org=f"{org}",
#                     predicate=predicatereq2,
#                 )
#             return "Response deleted", 200
#         except Exception as e:
#             traceback.print_exc()
#             return "Something Went Wrong!", 500

#
@router.post("/get_device_filter_date", responses={})
async def get_device_filter_date(data_list: list[GetFunctionDataSchema]):
    try:
        final_list = []
        for data in data_list:
            final_list.append(get_device_monitoring_data(data))

        return JSONResponse(content=final_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return "Error While Fetching Data", 500


@router.post("/get_interface_filter_date", responses={})
async def get_interface_filter_date(data_list: list[GetFunctionDataSchema]):
    try:
        final_list = []
        for data in data_list:
            print("data in get interface filtered date is:::::::::::::::::::::",data,file=sys.stderr)
            final_list.append(get_interface_monitoring_data(data))

        return JSONResponse(content=final_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return "Error While Fetching Data", 500

#
# @app.route("/deleteMonitoringdata", methods=["POST"])
# def DeleteMonitoringData():
#     try:
#         org = "monetx"
#         bucket = "monitoring"
#         measurement = "Devices"
#         ip_address = "192.168.0.2"
#         url = f"http://localhost:8086/api/v2/delete?org={org}&bucket={bucket}"
#         headers = {
#             "Authorization": "nItzto4Hc22kXuLsawB76lhKPM-wbK1DAQc7uBiFpYUCntoHDE6TC-uGeezzx7S89fyClKv2YXLfDi15Ujhn5A==",
#             "Content-Type": "application/json",
#         }
#         data = {
#             "start": "-60d",
#             "predicate": f'measurement="{measurement}" AND IP_ADDRESS="{ip_address}"',
#         }
#
#         requests.post(url, headers=headers, data=data)
#
#         return "deleted"
#
#     except Exception as e:
#         print(
#             "printing exception while deleteing data in influxdb",
#             str(e),
#             file=sys.stderr,
#         )
#         return str(e)
#
#
# @app.route("/deleteAllMonitoringdata", methods=["GET"])
# def DeleteAllMonitoringData():
#     try:
#         org = "monetx"
#         bucket = "monitoring"
#         from app import client
#
#         from influxdb_client import InfluxDBClient
#
#         delete_api = client.delete_api()
#
#         """
#         Delete Data
#         """
#         date_helper = get_date_helper()
#         start = "1970-01-01T00:00:00Z"
#         stop = date_helper.to_utc(datetime.now())
#         delete_api.delete(
#             start, stop, f'_measurement="Devices"', bucket=f"{bucket}", org=f"{org}"
#         )
#         delete_api.delete(
#             start, stop, f'_measurement="Interfaces"', bucket=f"{bucket}", org=f"{org}"
#         )
#
#         """
#         Close client
#         """
#         return "deleted"
#
#     except Exception as e:
#         print(
#             "printing exception while deleteing data in influxdb",
#             str(e),
#             file=sys.stderr,
#         )
#         return str(e)
#
#
# @app.route("/deleteIPMonitoringdata", methods=["GET"])
# def DeleteIPMonitoringData():
#     try:
#         from app import client
#
#         org = "monetx"
#         bucket = "monitoring"
#
#         from influxdb_client import InfluxDBClient
#
#         predicatereq1 = f'_measurement="Devices" AND IP_ADDRESS ="{ip_address}"'
#         predicatereq2 = f'_measurement="Interfaces" AND IP_ADDRESS ="{ip_address}"'
#
#         delete_api = client.delete_api()
#
#         """
#         Delete Data
#         """
#         date_helper = get_date_helper()
#         start = "1970-01-01T00:00:00Z"
#         stop = date_helper.to_utc(datetime.now())
#         delete_api.delete(
#             start, stop, bucket=f"{bucket}", org=f"{org}", predicate=predicatereq1
#         )
#         delete_api.delete(
#             start, stop, bucket=f"{bucket}", org=f"{org}", predicate=predicatereq2
#         )
#
#         """
#         Close client
#         """
#         return "deleted"
#
#     except Exception as e:
#         print(
#             "printing exception while deleteing data in influxdb",
#             str(e),
#             file=sys.stderr,
#         )
#         return str(e)
#
#
# @app.route("/deleteMonitoringAlerts", methods=["POST"])
# @token_required
# def DeleteMonitoringAlerts(user_data):
#     if True:
#         try:
#             monitoringObj = request.get_json()
#             response = False
#             queryString = f"delete from alerts_table where IP_ADDRESS='{monitoringObj['ip_address']}';"
#             db.session.execute(queryString)
#             db.session.commit()
#             response = True
#             if response:
#                 return (
#                     f"Alerts Deleted Successfully for {monitoringObj['ip_address']}",
#                     200,
#                 )
#             else:
#                 return "Deletion was Unsuccessful", 500
#         except Exception as e:
#             print(str(e), file=sys.stderr)
#             traceback.print_exc()
#             return str(e), 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#
# @app.route("/possibleReasonForAlerts", methods=["POST"])
# @token_required
# def PossibleReasonForAlerts(user_data):
#     if True:
#         try:
#             monitoringObj = request.get_json()
#             output = ""
#             description = (monitoringObj["description"]).lower()
#             if "of cpu" in description:
#                 output = "High CPU due to a broadcast storm\nHigh CPU due to BGP scanner\nHigh CPU Utilization in Exec and Virtual Exec Processes\nHigh CPU due to Non-Reverse Path Forwarding (RPF) traffic\nHigh CPU due to Multicast"
#
#             elif "memory" in description:
#                 output = "Memory leaks\nProcesses running on a device to see what’s using memory\nMemory size not large enough to support OS image (if you upgraded recently)\nMemory fragmentation"
#
#             elif "offline" in description:
#                 output = "Power outage or brownout\nUpstream switch or router on the network is also having issues\nDevice misconfiguration\nICMP traffic to device blocked\nEmergency maintenance\nHardware malfunction\nCrash related to the operating system\nDevice removed from network"
#             if output == "":
#                 return "Nothing to Display", 500
#
#             else:
#                 print(output, file=sys.stderr)
#                 return output, 200
#         except Exception as e:
#             print(str(e), file=sys.stderr)
#             traceback.print_exc()
#             return str(e), 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401

@router.get('/testin_influx_db')
def testing_influx():
    try:
        query_api = configs.client.query_api()
        print("query api is::::::::::::::::", query_api, file=sys.stderr)

        # Add the organization parameter to the write_api initialization
        write_api = configs.client.write_api(org="monetx", write_options=SYNCHRONOUS)
        print("write api is:::", write_api, file=sys.stderr)

        dictionary = {
            "measurement": "Monitoring Devices testing",
            "tags": {
                "DEVICE_NAME": "output['device_name']",
                "STATUS": "output['status']",
                "IP_ADDRESS": "host[1]",
                "FUNCTION": "host[2]",
                "VENDOR": "host[6]",
            },
            "time": datetime.utcnow().isoformat(),
            "fields": {
                "INTERFACES": 22,
                "DISCOVERED_TIME": datetime.utcnow().isoformat(),
                "DEVICE_DESCRIPTION": "output['device_description']",
                "CPU": "output['cpu']",
                "Memory": "output['memory']",
                "PACKETS_LOSS": "output['packets']",
                "Response": "output['response']"
            }
        }
        print("dictorinary is:::::::::::",dictionary,file=sys.stderr)
        try:
            print("writing to the disk is in process")
            write_api.write(org='monetx',bucket='monitoring', record=dictionary)
            print("Data written to disk", file=sys.stderr)
            return dictionary
        except Exception as e:
            traceback.print_exc()
            print("Error writing to disk:", str(e), file=sys.stderr)
            return {"error": str(e)}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@router.post('/get_interface_band',responses = {
    200:{"model":Response200},
    500:{"model":str}
},
description="API to get the interface band on the IP address click Interface Band on the IP address click",
summary="API to get the interface band on the IP address.Getting Interface Band on the IP address click"
)
def get_interface_band(ips:InterfaceBandScema):
    try:
        ip_address = ips['ip_address']
        org = 'monetx'
        query_api = configs.client.query_api()
        print("query api is:::::::::::;",query_api,file=sys.stderr)
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -1d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["IP_ADDRESS"] == "{ip_address}")\
                |> schema.fieldsAsCols()'
        result = query_api.query(org='monetx', query=query)
        print("result is:::::::::::::::::::::::::",result,file=sys.stderr)
        result = []
        data = {}
        objectDict = {}
        upload = []
        download = []
        all =[]
        final = []
        try:
            for table in result:
                for record in table:
                    print("table  in result is:::::::::::::::",table,file=sys.stderr)
                    print("record in tbale is:::::::::::::::::",record,file=sys.stderr)
                    if record['Interface_Name'] == ips['interface_name']:
                        print(f"Record Against the Interface Name is::{ips['interface_name']}",file=sys.stderr)
                        obj2 = {}
                        try:
                            obj2['date'] = datetime.strptime(record['Date'], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
                            print("obj 2 dict is::::::",obj2['date'],file=sys.stderr)
                        except Exception as e:
                            traceback.print_exc()
                            obj2['date'] =""

                        if record['Download']:
                            download.append(round(float(record['Download']),2))
                            obj2['name'] = record['Interface_Name']
                            obj2['download'] = round(float(record['Download']),2)

                        if record['Upload']:
                            upload.append(round(float(
                                record['Upload']
                            ),2))
                            obj2['upload'] = round(float(record['Uplaod']),2)
                            obj2['total'] = round(
                                float(record['Upload'])+float(record['Download']),2
                            )
                            all.append(obj2['total'])
                        result.append(obj2)
            objectDict['All'] = result[1:]
            print(f"Download is:::::::{download},upload is:::::::{upload},all is::::::::::::{all}",file=sys.stderr)
            if len(download)>0 and len(upload)>0:
                final.append({"bandwidth":"Download","min":min(download),"max":max(download),"avg":round(sum(download)/len(download),2)})
                final.append({"bandwidth": "Upload", "min": min(upload), "max": max(upload),
                              "avg": round(sum(upload) / len(upload), 2)})
                final.append(
                    {"bandwidth": "Average", "min": min(all), "max": max(all), "avg": round(sum(all) / len(all), 2)})
                objectDict['table'] = final
            elif len(download) == 0 or len(upload) == 0:
                final.append({"bandwidth": "Download", "min": 0, "max": 0, "avg": 0})
                final.append({"bandwidth": "Upload", "min": 0, "max": 0, "avg": 0})
                final.append({"bandwidth": "Average", "min": 0, "max": 0, "avg": 0})
            message = f"Interface Band Executed Successfully"
            data['data'] = objectDict
            data['message'] = message
            return JSONResponse(content=data,status_code=200)
        except Exception as e:
            traceback.print_exc()
    except Exception as e:
        traceback.print_exc()

# @router.post('/delete_monitoring_devices',responses={
#     200:{"model":DeleteResponseSchema},
#     400:{"model":str},
#     500:{"model":str}
# },
# summary="API to delete monitoring devices",
# description="API to delete monitoring devices"
# )
# def delete_monitoring_devices(device_ids:list[str]):
#     try:
#         deleted_ids = []
#         success_list = []
#         error_list = []
#
#         org = "monetx"
#         bucket = "monitoring"
#         delete_api = configs.client.delete_api()
#         """
#             Delete Data
#         """
#
#         data_helper = get_date_helper()
#         start = "1970-01-01T00:00:00Z"
#         stop = data_helper.to_utc(datetime.now())
#
#         for device_id in device_ids:
#             device_exsist = configs.db.query(Monitoring_Devices_Table).filter_by(monitoring_device_id = device_id).first()
#             if device_exsist:
#                 print("device exsist is:::::::::::::::",device_exsist,file=sys.stderr)
#                 atom_exsist = configs.db.query(AtomTable).filter_by(atom_id = device_exsist.atom_id).first()
#                 print("atom exsist is::::::::::::::::::::",atom_exsist,file=sys.stderr)
#                 if atom_exsist:
#                     ip_address = atom_exsist.ip_address
#                     predicatereq1 = f"_measurement=\"Devices\" AND IP_ADDRESS =\"{ip_address}\""
#                     predicatereq2 = f"_measurement=\"Interfaces\" AND IP_ADDRESS =\"{ip_address}\""
#                     delete_api.delete(
#                         start,stop,bucket=f'{bucket}',org=f'{org}',predicate=predicatereq1
#                     )
#                     delete_api.delete(
#                         start, stop, bucket=f'{bucket}', org=f'{org}', predicate=predicatereq2
#                     )
#                     deleted_ids.append(device_id)
#                     DeleteDBData(device_id)
#                     print("Monitoring devices from sql and influx deleted successfully",file=sys.stderr)
#                     success_list.append(f"{device_id} : Deleted Successfully")
#                 else:
#                     error_list.append(f"{device_exsist.atom_id} : Not Found ")
#             else:
#                 error_list.append(f"{device_id} : Not Found")
#         print("Data is:::::::::::::::::",deleted_ids,file=sys.stderr)
#         print("success list is::::::::::::::",success_list,file=sys.stderr)
#         print("error list is:::::::::::::::::::;",error_list,file=sys.stderr)
#         responses = {
#             "data":deleted_ids,
#             "success_list":success_list,
#             "error_list":error_list,
#             "success":len(success_list),
#             "error":len(error_list)
#         }
#         return responses
#     except Exception as e:
#         traceback.print_exc()
#         return JSONResponse(content="Error Occured While Deleting Monitoring devvices",status_code=500)