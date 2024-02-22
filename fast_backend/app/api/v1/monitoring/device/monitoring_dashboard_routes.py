from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.v1.monitoring.device.utils.monitoring_utils import *
from app.models.atom_models import *
from app.models.monitoring_models import *
from app.schema.monitoring_schema import *

router = APIRouter(
    prefix="/dashboard",
    tags=["monitoring_dashboard"],
)


@router.get("/get_snapshot", responses={
    200: {"model": list[SnapShotSchema]},
    500: {"model": str}
},summary="API to get snapshot",
description="API to snapshot")
def snapshot():
    try:
        query_string = (
            f"SELECT atom.`function`,COUNT(atom.`function`) "
            "FROM monitoring_devices_table INNER JOIN atom_table AS atom ON "
            "monitoring_devices_table.atom_id = atom.atom_id "
            "WHERE monitoring_devices_table.active='Active' GROUP BY atom.`function`;"
        )
        results = configs.db.execute(query_string)

        query_string1 = (
            "SELECT atom.`function`, COUNT(atom.`function`) FROM monitoring_alerts_table "
            "INNER JOIN monitoring_devices_table ON monitoring_devices_table.monitoring_device_id "
            "= monitoring_alerts_table.monitoring_device_id INNER JOIN atom_table as atom "
            "ON atom.atom_id = monitoring_devices_table.atom_id WHERE "
            "monitoring_alerts_table.creation_date > NOW() - INTERVAL 1 day "
            "GROUP BY atom.`function` ;"
        )
        results1 = configs.db.execute(query_string1)

        monitoring_data_dict = {}
        monitoring_data_dict1 = {}

        for MonitoringObj in results:
            monitoring_data_dict[MonitoringObj[0]] = MonitoringObj[1]

        for MonitoringObj in results1:
            monitoring_data_dict1[MonitoringObj[0]] = MonitoringObj[1]

        final = []
        for key, Value in monitoring_data_dict.items():
            print(key, Value, file=sys.stderr)
            try:
                final.append(
                    {
                        "name": key,
                        "devices": monitoring_data_dict[key],
                        "alarms": monitoring_data_dict1[key],
                    }
                )
            except Exception as e:
                print(e, file=sys.stderr)
                final.append(
                    {"name": key, "devices": monitoring_data_dict[key], "alarms": 0}
                )

        return JSONResponse(content=final, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_monitoring_heatmap", responses={
    200: {"model": list[MonitoringSpiralSchema]},
    500: {"model": str}
},summary="API to get monitoring_heatmap",
description="API to get monitoring_heatmap")
def monitoring_heatmap():
    try:
        sqlquery = ("SELECT COUNT(device_heatmap) FROM monitoring_devices_table "
                    "WHERE device_heatmap = 'Device Down';")
        service_down = configs.db.execute(sqlquery).scalar()

        sqlquery = ("SELECT COUNT(device_heatmap) FROM monitoring_devices_table "
                    "WHERE device_heatmap = 'Critical';")
        critical = configs.db.execute(sqlquery).scalar()

        sqlquery = ("SELECT COUNT(device_heatmap) FROM monitoring_devices_table "
                    "WHERE device_heatmap = 'Attention';")
        attention = configs.db.execute(sqlquery).scalar()
        # trouble variable

        sqlquery = ("SELECT COUNT(device_heatmap) FROM monitoring_devices_table "
                    "WHERE device_heatmap ='InActive';")
        no_monitoring = configs.db.execute(sqlquery).scalar()

        sqlquery = ("SELECT COUNT(device_heatmap) FROM monitoring_devices_table "
                    "WHERE device_heatmap ='Clear';")
        clear = configs.db.execute(sqlquery).scalar()

        sqlquery = ("SELECT count(DEVICE_HEATMAP) FROM monitoring_devices_table "
                    "WHERE DEVICE_HEATMAP ='Not Monitored';")
        not_monitored = configs.db.execute(sqlquery).scalar()

        # sqlquery = f"select count(ip_address) from monitoring_devices_table;"
        total = (
                service_down
                + critical
                + attention
                + no_monitoring
                + clear
                + not_monitored
        )
        obj_list = [
            {"fill": "#E2B200", "name": "Attention", "value": int(attention)},
            {"fill": "#C0C0C0", "name": "Not Monitored", "value": int(not_monitored)},
            {"fill": "#66B127", "name": "Clear", "value": int(clear)},
            {"fill": "#FF9A40", "name": "Critical", "value": int(critical)},
            {"fill": "#808080", "name": "InActive", "value": int(no_monitoring)},
            {"fill": "#DC3938", "name": "Device Down", "value": int(service_down)},
            {"fill": "#0504aa", "name": "Total", "value": int(total)},
        ]

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_device_status_map", responses={
    200: {"model": list[MonitoringMapSchema]},
    500: {"model": str}
},summary="API to get device status map",
description="API to get device status map")
def get_device_status_map():
    try:
        results = (
            configs.db.query(Monitoring_Devices_Table, AtomTable)
            .join(AtomTable, AtomTable.atom_id == Monitoring_Devices_Table.atom_id)
            .all()
        )

        node_list = []
        for device, atom in results:
            device_dict = {}
            device_dict["id"] = atom.ip_address
            device_dict["label"] = atom.ip_address
            device_dict["status"] = device.device_heatmap
            device_dict["function"] = atom.function

            node_list.append(device_dict)

        for dic in node_list:
            dic["title"] = f"{dic['id']}\n{dic['status']}"

            dic["image"] = "./img/" + dic["function"] + ".svg"

        static_node = {
            "function": "MonetX",
            "image": "MonetX",
            "label": "MonetX",
            "id": "1",
            "status": "N/A",
            "title": "MonetX",
        }

        node_list.append(static_node)
        response = {"nodes": node_list}
        edges_list = []
        for dic in node_list:
            objDict = {}
            ip_address = dic["id"]
            status = dic["status"]
            if status == "Clear":
                status = "#5AB127"
            elif status == "Active":
                status = "#90EE90"
            elif status == "InActive":
                status = "#A8A6A6"
            elif status == "Attention":
                status = "#E2B200"
            elif status == "Not Monitored":
                status = "#D7D7D7"
            elif status == "Critical":
                status = "#FF9A40"
            elif status == "Device Down":
                status = "#DC3938"
            elif status == "N/A":
                status = "None"
            else:
                status = "#D7D7D7"
            if "#" in status:
                objDict["id"] = ip_address
                objDict["from"] = "1"
                objDict["to"] = ip_address
                objDict["color"] = {"color": status}

                edges_list.append(objDict)

        response["edges"] = edges_list
        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return "Something Went Wrong!", 500


@router.get("/get_top_interfaces", responses={
    200: {"model": list[TopInterfacesSchema]},
    500: {"model": str}
},summary="API to get top interfaces",
description="API to get top interfaces")
def get_top_interfaces():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
        import "influxdata/influxdb/schema"\
        from(bucket: "monitoring")\
        |> range(start: -1d)\
        |> filter(fn: (r) => r["_measurement"] == "Interfaces")\
        |> schema.fieldsAsCols()\
        |> sort(columns: ["_time"], desc: true)\
        |> unique(column: "Interface_Name")\
        |> yield(name: "unique")'
        result = query_api.query(org="monetx", query=query)
        results = []
        print(result)
        for table in result:
            for record in table.records:
                obj_dict = {}
                if record["Download"]:
                    try:
                        obj_dict["ip_address"] = record["IP_ADDRESS"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        obj_dict["device_name"] = record["DEVICE_NAME"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        obj_dict["interface_name"] = record["Interface_Name"]
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        obj_dict["download_speed"] = round(
                            float(record["Download"]), 2
                        )
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    try:
                        if record["Upload"]:
                            obj_dict["upload_speed"] = round(
                                float(record["Upload"]), 2
                            )
                    except Exception as e:
                        print("error", str(e), file=sys.stderr)
                        continue

                    results.append(obj_dict)
        print(results)
        sorted_list = sorted(results, key=lambda k: k["download_speed"], reverse=True)
        print(sorted_list)
        output = {}
        for v in sorted_list:
            if "interface_name" in v:
                interface_name = v["interface_name"]
                output[interface_name] = v

        output = list(output.values())
        print(output)
        if len(output) > 9:
            return JSONResponse(content=output[0:9], status_code=200)
        else:
            return JSONResponse(content=output, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_cpu_dashboard", responses={
    200: {"model": list[CpuDashboardSchema]},
    500: {"model": str}
},summary="API to get cpu dashboard",
description="API to get cpu dashboard")
def cpu_stats_fetching():
    try:
        query_api = configs.client.query_api()
        query = f'import "strings"\
        import "influxdata/influxdb/schema"\
        from(bucket: "monitoring")\
         |> range(start:-1d)\
         |> filter(fn: (r) => r["_measurement"] == "Devices")\
         |> last()\
         |> schema.fieldsAsCols()'

        result = query_api.query(org="monetx", query=query)
        results = []

        for table in result:
            for record in table.records:
                obj_dict = {}
                try:
                    if record["CPU"]:
                        try:
                            if record["IP_ADDRESS"]:
                                obj_dict["ip_address"] = record["IP_ADDRESS"]
                        except Exception as e:
                            print("error", str(e), file=sys.stderr)
                            continue

                        try:
                            if record["FUNCTION"]:
                                obj_dict["function"] = record["FUNCTION"]
                        except Exception as e:
                            print("error", str(e), file=sys.stderr)
                            continue

                        try:
                            if record["CPU"]:
                                obj_dict["cpu"] = float(record["CPU"])
                        except Exception as e:
                            print("error", str(e), file=sys.stderr)
                            obj_dict["cpu"] = float(0)
                            continue

                        try:
                            if record["DEVICE_NAME"]:
                                obj_dict["device_name"] = record["DEVICE_NAME"]
                        except Exception as e:
                            print("error", str(e), file=sys.stderr)
                            continue

                        results.append(obj_dict)
                    else:
                        continue
                except Exception:
                    continue

        final_list = []
        cpu_list = sorted(results, key=lambda k: k["cpu"], reverse=True)
        ip_list = []

        for dct in cpu_list:
            if dct["ip_address"] in ip_list:
                pass
            else:
                final_list.append(dct)
                ip_list.append(dct["ip_address"])
        last_list = [x for x in final_list if not (x.get("cpu") < 0.1)]

        if len(last_list) > 4:
            return JSONResponse(content=last_list[0:4], status_code=200)
        else:
            return JSONResponse(content=last_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_memory_dashboard", responses={
    200: {"model": list[MemoryDashboardSchema]},
    500: {"model": str}
},summary="API to get memory dashboard ",
description="API to get memory dashboard")
def memory_stats_fetching():
    try:
        query_api = configs.client.query_api()
        query = 'import "strings"\
        import "influxdata/influxdb/schema"\
        from(bucket: "monitoring")\
            |> range(start:-1d)\
            |> filter(fn: (r) => r["_measurement"] == "Devices")\
            |> last()\
            |> schema.fieldsAsCols()'

        result = query_api.query(org="monetx", query=query)
        results = []

        for table in result:
            for record in table.records:
                obj_dict = {}
                try:
                    if record["IP_ADDRESS"]:
                        obj_dict["ip_address"] = record["IP_ADDRESS"]
                except Exception as e:
                    print("error", str(e), file=sys.stderr)
                    continue

                try:
                    if record["FUNCTION"]:
                        obj_dict["function"] = record["FUNCTION"]
                except Exception as e:
                    print("error", str(e), file=sys.stderr)
                    continue

                try:
                    if record["Memory"]:
                        obj_dict["memory"] = float(record["Memory"])
                except Exception as e:
                    print("error", str(e), file=sys.stderr)
                    obj_dict["memory"] = float(0)
                    continue

                try:
                    if record["DEVICE_NAME"]:
                        obj_dict["device_name"] = record["DEVICE_NAME"]
                except Exception as e:
                    print("error", str(e), file=sys.stderr)
                    continue

                results.append(obj_dict)
                print(result, file=sys.stderr)

        memorylist = sorted(results, key=lambda k: k.get("memory", 0), reverse=True)
        final_list = []
        ip_list = []
        i = 0
        for dct in memorylist:
            if dct["ip_address"] in ip_list:
                pass
            else:
                final_list.append(dct)
                ip_list.append(dct["ip_address"])
        last_list = [
            x
            for x in final_list
            if x.get("memory") is not None and (x.get("memory") >= 0.1)
        ]

        if len(last_list) > 4:
            return JSONResponse(content=last_list[0:4], status_code=200)
        else:
            return JSONResponse(content=last_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)



