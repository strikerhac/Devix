import sys

from app.api.v1.monitoring.device.utils.common_puller import *
from ping3 import ping,verbose_ping

def UpdateMonitoringDevice(MonitoringObj, row, update):
    try:
        credentials = ''
        MonitoringObj = dict(MonitoringObj)
        print("MOnitoring object is::::::::::::::::::::::::::;",MonitoringObj,file=sys.stderr)
        monitoring_id_exsist = configs.db.query(Monitoring_Devices_Table).filter_by(monitoring_device_id = MonitoringObj['monitoring_device_id']).first()
        if monitoring_id_exsist:
            print("Monitoring device id exsist:::::::::::::::::::")
            print("procedding to next step")
            atom_id_in_monitoring = monitoring_id_exsist.atom_id
            atom_id_exsist = configs.db.query(AtomTable).filter_by(atom_id = atom_id_in_monitoring).first()
            monitoring_credential_exsist = configs.db.query(Monitoring_Credentails_Table).filter_by(monitoring_credentials_id = MonitoringObj['monitoring_credentials_id']).first()
            if monitoring_credential_exsist:
                monitoring_category = monitoring_credential_exsist.category
                monitoring_crednetials_profile_name = monitoring_credential_exsist.profile_name
                credentials = monitoring_category+"-"+monitoring_crednetials_profile_name
                monitoring_id_exsist.monitoring_credentials_id = monitoring_credential_exsist.monitoring_credentials_id
            if atom_id_exsist:
                atom_id = atom_id_exsist.atom_id
                print("atom id is::::::::::::::::::::::::::",atom_id,file=sys.stderr)
            else:
                return f"No Atom ID Against the Monitoring ID {monitoring_id_exsist}", 400
            status = ping(atom_id_exsist.ip_address)[0]
            print("status is:::::::::::::::::::::::::::",file=sys.stderr)
            monitoring_id_exsist.atom_id = atom_id
            monitoring_id_exsist.active ='Active'

            # print("monitoring active is::::::::::::::::::::::::::::::::::;", Monitoringdb.active, file=sys.stderr)
            monitoring_id_exsist.device_heatmap = 'Active'
            if monitoring_id_exsist.active == "Active":
                    monitoring_id_exsist.status = status
            else:
                    monitoring_id_exsist.status = ""
            UpdateDBData(monitoring_id_exsist)
            monitoring_device_object = {
                    "monitoring_device_id":monitoring_id_exsist.monitoring_device_id,
                    "ip_address":atom_id_exsist.ip_address,
                    "device_name":atom_id_exsist.device_name,
                    "device_type":atom_id_exsist.device_type,
                    "vendor":atom_id_exsist.vendor,
                    "function":atom_id_exsist.function,
                    "active":monitoring_id_exsist.active,
                    "status":monitoring_id_exsist.status,
                    "credentials":credentials,
                    "ping_status":monitoring_id_exsist.ping_status,
                    "snmp_status":monitoring_id_exsist.snmp_status
                }
            data = {
                "data":monitoring_device_object,
                "message":f"{atom_id_exsist.device_name} : Updated successfully"
            }
            print("data is:::::::::::::::::::::::::::::::::::",data,file=sys.stderr)
            return data
        else:
            return "No Monitoring Device ID found",400
    except Exception as e:
        traceback.print_exc()
        print("Error Occured While Updating the Monitoring device")

def AddMonitoringDevice(MonitoringObj, row, update):
    # return "Currently Device Can Not Be Added Directly In Monitoring", 500
    try:
        print("monitoring device is:::::::::::::::::::::::::::::::::::::::::",MonitoringObj,file=sys.stderr)
        MonitoringObj = dict(MonitoringObj)
        print("Monitoring Obj in deict is:::::::",MonitoringObj,file=sys.stderr)
        if "ip_address" not in MonitoringObj.keys():
            return f"Row {row} : Ip Address Is Missing", 400

        if MonitoringObj["ip_address"] is None:
            return f"Row {row} : Ip Address Can Not Be Empty", 400

        MonitoringObj["ip_address"] = MonitoringObj["ip_address"].strip()
        if MonitoringObj["ip_address"] == "":
            return f"Row {row} : Ip Address Can Not Be Empty", 400

        atom = configs.db.query(AtomTable).filter_by(
            ip_address=MonitoringObj["ip_address"]
        ).first()
        atom_id = atom.atom_id
        if atom is None:
            return f"{MonitoringObj['ip_address']} : Ip Address Not Found In Atom", 500

    except Exception:
        traceback.print_exc()
        return "Exception", 500

    MonitoringObj["active"] = MonitoringObj["active"].title()
    print(MonitoringObj, file=sys.stderr)
    status = ping(MonitoringObj["ip_address"])[0]

    # ip = MonitoringObj['ip_address']
    # ip_test = ip.split(".")
    # for i in ip_test:
    #     if int(i) > 255:
    #         return "Wrong IP Address", 500
    #     else:
    #         pass

    Monitoringdb = Monitoring_Devices_Table()
    if "ip_address" in MonitoringObj:
        Monitoringdb.ip_address = MonitoringObj["ip_address"]
    if MonitoringObj["device_name"] == "":
        MonitoringObj["device_name"] = "NA"
    else:
        Monitoringdb.device_name = MonitoringObj["device_name"]
    Monitoringdb.source = "Atom"
    Monitoringdb.atom_id = atom_id
    print("Monitoring is:::::::::::::::::::::::::::::::::",file=sys.stderr)
    Monitoringdb.vendor = MonitoringObj["vendor"]
    print("Monitoring vendor is",Monitoringdb.vendor,file=sys.stderr)
    Monitoringdb.device_type = MonitoringObj["device_type"]
    print("Monitoring device type is:::::::::::::::::::",Monitoringdb.device_type,file=sys.stderr)
    Monitoringdb.function = MonitoringObj["function"]
    print("Monitoring device function is:::::::::",Monitoringdb.function,file=sys.stderr)
    Monitoringdb.credentials = MonitoringObj["credentials"]
    print("Monitoring credentials are:::::::::::::::::::::",Monitoringdb.credentials,file=sys.stderr)
    Monitoringdb.active = MonitoringObj["active"]
    print("monitoring active is::::::::::::::::::::::::::::::::::;",Monitoringdb.active,file=sys.stderr)
    Monitoringdb.device_heatmap = MonitoringObj["active"]
    print("Monitoring active is::::::::::::::::::::::",Monitoringdb.device_heatmap,file=sys.stderr)
    if MonitoringObj["active"] == "Active":
        Monitoringdb.status = status
    else:
        Monitoringdb.status = "NA"

    id = None
    queryString = f"select monitoring_device_id from monitoring_devices_table where atom_id='{atom_id}';"
    result = configs.db.execute(queryString)
    print("result for the query string in monitoring is:::::::::::::::::",result,file=sys.stderr)
    for row in result:
        print("row is:::::::::::::::::::::::::::",row,file=sys.stderr)
        id = row[0]
        print("id is:::::::::::::::::::::::::::::::::::::::",id,file=sys.stderr)
    if id == None:
        InsertDBData(Monitoringdb)
        print("Inserted ", MonitoringObj["ip_address"], file=sys.stderr)
        return "Inserted Successfully", 200
    else:
        Monitoringdb.monitoring_device_id = id
        UpdateDBData(Monitoringdb)
        print("Updated ", MonitoringObj["monitoring_device_id"], file=sys.stderr)

        return "Updated Successfully", 200


def get_device_monitoring_data(data):
    function = data['function']
    device_type = None
    if "device_type" in data:
        if data["device_type"] is not None:
            data["device_type"] = str(data["device_type"]).strip()
            if data['device_type'] != "":
                device_type = data["device_type"]

    query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start:-60d)\
                |> filter(fn: (r) => r["_measurement"] == "Devices")\
                |> filter(fn: (r) => r["FUNCTION"] == "{function}")\
                |> last()\
                |> schema.fieldsAsCols()'

    if device_type is not None:
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start:-60d)\
                |> filter(fn: (r) => r["_measurement"] == "Devices")\
                |> filter(fn: (r) => r["FUNCTION"] == "{function}")\
                |> filter(fn: (r) => r["DEVICE_TYPE"] == "{device_type}")\
                |> last()\
                |> schema.fieldsAsCols()'
    return get_device_influx_data(query)


def get_interface_monitoring_data(data):
    function = data['function']
    device_type = None
    if "device_type" in data:
        if data["device_type"] is not None:
            data["device_type"] = str(data["device_type"]).strip()
            if data['device_type'] != "":
                device_type = data["device_type"]

    query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "{function}")\
                |> schema.fieldsAsCols()\
                |> sort(columns: ["_time"], desc: true)\
                |> unique(column: "Interface_Name")\
                |> yield(name: "unique")'
    print("query is:::::::::::::::::::::::::::::::::::::::::",query,file=sys.stderr)
    if device_type is not None:
        query = f'import "strings"\
                import "influxdata/influxdb/schema"\
                from(bucket: "monitoring")\
                |> range(start: -60d)\
                |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
                |> filter(fn: (r) => r["FUNCTION"] == "{function}")\
                |> filter(fn: (r) => r["DEVICE_TYPE"] == "{device_type}")\
                |> schema.fieldsAsCols()\
                |> sort(columns: ["_time"], desc: true)\
                |> unique(column: "Interface_Name")\
                |> yield(name: "unique")'
        print("query is:::::::::::::::::::::::::::::::::::::::::::::::",query,file=sys.stderr)
    return get_interface_influx_data(query)


def get_device_influx_data(query):
    query_api = configs.client.query_api()
    result = query_api.query(org="monetx", query=query)
    resultList = []
    finalList = []
    try:
        for table in result:
            for record in table.records:
                try:
                    objDict = {}
                    try:
                        if record["IP_ADDRESS"]:
                            objDict["ip_address"] = record["IP_ADDRESS"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["FUNCTION"]:
                            objDict["function"] = record["FUNCTION"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["Response"]:
                            objDict["response"] = record["Response"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["STATUS"]:
                            objDict["status"] = record["STATUS"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["Uptime"]:
                            objDict["uptime"] = record["Uptime"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["VENDOR"]:
                            objDict["vendor"] = record["VENDOR"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["CPU"]:
                            objDict["cpu"] = record["CPU"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["Memory"]:
                            objDict["memory"] = record["Memory"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["PACKETS_LOSS"]:
                            objDict["packets"] = record["PACKETS_LOSS"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["DEVICE_NAME"]:
                            objDict["device_name"] = record["DEVICE_NAME"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["INTERFACES"]:
                            objDict["interfaces"] = record["INTERFACES"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["Date"]:
                            objDict["date"] = record["Date"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["DEVICE_DESCRIPTION"]:
                            objDict["device_description"] = record["DEVICE_DESCRIPTION"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["DISCOVERED_TIME"]:
                            objDict["discovered_time"] = record["DISCOVERED_TIME"]

                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["DEVICE_TYPE"]:
                            objDict["device_type"] = record["DEVICE_TYPE"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    resultList.append(objDict)

                except Exception:
                    traceback.print_exc()

        finalList = sorted(resultList, key=lambda k: k["date"], reverse=False)

    except Exception:
        traceback.print_exc()

    return finalList


def get_interface_influx_data(query):
    query_api = configs.client.query_api()
    result = query_api.query(org="monetx", query=query)
    resultList = []
    finalList = []
    try:
        for table in result:
            for record in table.records:
                try:
                    objDict = {}
                    objDict = {}
                    print(record, file=sys.stderr)
                    try:
                        if record["IP_ADDRESS"]:
                            objDict["ip_address"] = record["IP_ADDRESS"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["DEVICE_NAME"]:
                            objDict["device_name"] = record["DEVICE_NAME"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["FUNCTION"]:
                            objDict["function"] = record["FUNCTION"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["Status"]:
                            objDict["interface_status"] = record["Status"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["VENDOR"]:
                            objDict["vendor"] = record["VENDOR"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["Download"] == None or record["Download"] == "":
                            objDict["download_speed"] = 0
                        else:
                            objDict["download_speed"] = round(
                                float(record["Download"]), 2
                            )
                    except Exception as e:
                        objDict["download_speed"] = 0
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["Upload"] == None or record["Upload"] == "":
                            objDict["upload_speed"] = 0
                        else:
                            objDict["upload_speed"] = round(float(record["Upload"]), 2)
                    except Exception as e:
                        objDict["upload_speed"] = 0
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if (
                                record["Interface_Name"] == None
                                or record["Interface_Name"] == ""
                        ):
                            continue
                        else:
                            objDict["interface_name"] = record["Interface_Name"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue
                    try:
                        if record["Interface_Des"]:
                            objDict["interface_description"] = record["Interface_Des"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass

                    try:
                        if record["Date"]:
                            objDict["date"] = record["Date"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["DEVICE_NAME"]:
                            objDict["device_name"] = record["DEVICE_NAME"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass
                    try:
                        if record["DEVICE_TYPE"]:
                            objDict["device_type"] = record["DEVICE_TYPE"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        pass

                    resultList.append(objDict)

                except Exception:
                    traceback.print_exc()

        finalList = list(
            {
                dictionary["interface_name"]: dictionary for dictionary in resultList
            }.values()
        )

    except Exception:
        traceback.print_exc()

    return finalList



def ping(ip):
    try:
        response_time = ping3.ping(str(ip))
        if response_time is not None:
            # , str(int(response_time * 1000)), "0"
            return "Up"
        else:
            # , "NA", "100"
            return "Down"
    except Exception as e:
        traceback.print_exc()
        return "Down", "NA", "100"