from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Query
from app.api.v1.monitoring.device.utils.alerts_utils import *
from app.schema.monitoring_schema import *

router = APIRouter(
    prefix="/alerts",
    tags=["monitoring_alerts"]
)


# @app.route("/updateMonitoringAlertCPUThreshold", methods=["POST"])
# @token_required
# def updateMonitoringAlertCPUThreshold(user_data):
#     try:
#         pass
#     except Exception as e:
#         print("Error While Updating Monitoring CPU Alert Threshold", file=sys.stderr)
#         traceback.print_exc()
#
#
@router.get("/get_monitoring_alerts", responses={
    200: {"model": list[MonitoringAlertSchema]},
    500: {"model": str}
},
summary="Use this API in Monitoring module ALerts Page to list down all alerts in table.This API is of get method",
description="Use this API in Monitoring module ALerts Page to list down all alerts in table.This API is of get method"

)
async def low_alerts():
    try:
        # alert_level: str = Query(..., description="alert level of the device of the device")
        # alert_level = str(alert_level).lower()
        return JSONResponse(content=get_level_alert(), status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Alerts", status_code=500)


@router.get("/alert_status", responses={
    200: {"model": list[AlertStatusSchema]},
    500: {"model": str}
},
summary="Use this API in the monitoring alert page to alert status count",
description= "Use this API in the monitoring alert page to alert status count"
)
async def alert_status():
    try:
        obj_list = []
        response_dict = {
            "total": 0,
            "critical": 0,
            "informational": 0,
            "device_down": 0,
        }
        query_string = (f"SELECT COUNT(*) FROM monitoring_alerts_table "
                        f"WHERE modification_date > NOW() - INTERVAL 1 DAY;")
        response_dict["total"] = configs.db.execute(query_string).scalar()

        query_string = (f"SELECT alert_type, COUNT(alert_type) FROM monitoring_alerts_table"
                        f" WHERE modification_date > NOW() - INTERVAL 1 DAY GROUP BY alert_type;")
        results = configs.db.execute(query_string)

        for result in results:
            if str(result[0]) == "critical":
                response_dict["critical"] = result[1]
            elif str(result[0]) == "informational":
                response_dict["informational"] = result[1]
            elif str(result[0]) == "device_down":
                response_dict["device_down"] = result[1]
        if not response_dict:
            obj_list = [{"name":"total","value":0} , {"name":"critical","value":0 },{"name":"informational","value":0},{"name":"device_down","value":0}]

            return JSONResponse(content=obj_list, status_code=200)

        obj_list=[{"name":"total","value":response_dict["total"]} , {"name":"critical","value":response_dict["critical"] },{"name":"informational","value":response_dict["informational"]},{"name":"device_down","value":response_dict["device_down"]}]

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_ip_alerts", responses={
    200: {"model": list[MonitoringAlertSchema]},
    500: {"model": str}
},
summary="Use this API to be used in monitoring alerts page to display the alert based on ip click.This API is of get method but requires ip_address as an query parameter",
description="Use this API to be used in monitoring alerts page to display the alert based on ip click.This API is of get method but requires ip_address as an query parameter"
)
async def get_ip_alerts(ip: str = Query(..., description="IP address of the device")):
    try:
        monitoring_alert_list = []

        results = (
            configs.db.query(
                Monitoring_Alerts_Table, Monitoring_Devices_Table, AtomTable
            )
            .join(
                Monitoring_Devices_Table,
                Monitoring_Devices_Table.monitoring_device_id
                == Monitoring_Alerts_Table.monitoring_device_id,
            )
            .join(AtomTable, AtomTable.atom_id == Monitoring_Devices_Table.atom_id)
            .filter(AtomTable.ip_address == ip)
            .all()
        )

        for alert, device, atom in results:
            monitoring_alert_dict = {"alarm_id": alert.monitoring_alert_id,
                                     "ip_address": atom.ip_address,
                                     "description": alert.description,
                                     "alert_type": alert.alert_type,
                                     "category": alert.category,
                                     "alert_status": alert.alert_status,
                                     "mail_status": alert.mail_status,
                                     "date": alert.modification_date}

            monitoring_alert_list.append(monitoring_alert_dict)

        return JSONResponse(content=monitoring_alert_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.post("/get_monitoring_alerts_by_ip_address", responses={
    200: {"model": list[MonitoringAlertSchema]},
    500: {"model": str}
},
summary="Use this API to be used in monitoring alerts page to display the alert based on ip click.This API is of get method but requires ip_address as an query parameter",
description="Use this API to be used in monitoring alerts page to display the alert based on ip click.This API is of get method but requires ip_address as an query parameter"
)
async def get_ips_alerts(ip: MonitoringAlertsByIpAddress):
    try:
        monitoring_alert_list = []

        results = (
            configs.db.query(
                Monitoring_Alerts_Table, Monitoring_Devices_Table, AtomTable
            )
            .join(
                Monitoring_Devices_Table,
                Monitoring_Devices_Table.monitoring_device_id
                == Monitoring_Alerts_Table.monitoring_device_id,
            )
            .join(AtomTable, AtomTable.atom_id == Monitoring_Devices_Table.atom_id)
            .filter(AtomTable.ip_address == ip.ip_address)
            .all()
        )

        for alert, device, atom in results:
            monitoring_alert_dict = {"alarm_id": alert.monitoring_alert_id,
                                     "ip_address": atom.ip_address,
                                     "description": alert.description,
                                     "alert_type": alert.alert_type,
                                     "category": alert.category,
                                     "alert_status": alert.alert_status,
                                     "mail_status": alert.mail_status,
                                     "date": alert.modification_date}

            monitoring_alert_list.append(monitoring_alert_dict)

        return JSONResponse(content=monitoring_alert_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)
