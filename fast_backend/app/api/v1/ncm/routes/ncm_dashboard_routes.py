import traceback
from datetime import timedelta

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import sys
from app.core.config import configs
from app.models.atom_models import *
from app.models.ncm_models import *
from app.schema.base_schema import *
from app.schema.ncm_schema import *

router = APIRouter(
    prefix="/ncm_dashboard",
    tags=["ncm_dashboard"]
)


@router.get("/ncm-change-summery-by-time", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary = "API to get the ncm change summary by time",
description="API to get the ncm change summary by time "
)
async def ncm_change_summery_by_time():
    current_time = datetime.now()
    pre_time = datetime.now() - timedelta(days=1)
    print("pre time is:::::::::::::::::::::::::::", pre_time, file=sys.stderr)
    try:
        query = (f"SELECT COUNT(*) AS backup_count, "
                 f"DATE_FORMAT(config_change_date, '%Y-%m-%d %H:00:00') "
                 f"AS hour_interval FROM ncm_device_table "
                 f"WHERE config_change_date IS NOT NULL "
                 f"GROUP BY hour_interval ORDER BY backup_count DESC LIMIT 5;")

        result = configs.db.execute(query)
        print("result")

        name_list = []
        value_list = []
        for row in result:
            name_list.append(row[1])
            value_list.append(int(row[0]))

        if len(name_list) <= 0:
            for i in range(5):
                temp_time = current_time - timedelta(hours=i)
                name_list.append(f"{temp_time.date()} {temp_time.hour}:00")
                value_list.append(0)

        obj_dict = {"name": name_list, "value": value_list}

        return JSONResponse(content=obj_dict, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            "Error While Fetching The Data\nFor Configuration Change Count By Time Graph",
            500,
        )


@router.get("/ncm_change_summery_by_device", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary="API to get the ncm change summary by device",
description="API to get the ncm change summary by device"
)
async def ncm_change_summery_by_device():
    pre_time = datetime.now() - timedelta(days=1)
    print("pre time", pre_time,file=sys.stderr)

    try:
        name_list = []
        value_list = []
        query = ("SELECT count(*) AS backup_count, atom_table.vendor "
                 "FROM ncm_device_table INNER JOIN atom_table "
                 "ON ncm_device_table.atom_id = atom_table.atom_id "
                 "GROUP BY atom_table.vendor")

        print("Executing query:", query, file=sys.stderr)
        result = configs.db.execute(query)
        print("results is::::::::::::::::::::::::",result,file=sys.stderr)
        restls = result
        print("rets are:::::::::::::::::::::::::::::::::::::",restls,file=sys.stderr)
        for row in result:
            print("row in result is::::::::::::::::::", row, file=sys.stderr)
            if row[1] is None:
                name_list.append("Undefined")

            elif row[1] == "":
                name_list.append("Undefined")
            else:
                name_list.append(row[1])

            value_list.append(int(row[0]))
        print("name list is::::::::::::::::::::::::::::", name_list, file=sys.stderr)
        print("value list is::::::::::::::::::::::::::::", value_list, file=sys.stderr)
        if len(name_list) <= 0:
            name_list = ["Cisco", "Huawei", "Juniper", "Fortinet", "Other"]
            value_list = [0, 0, 0, 0, 0]

        obj_dict = dict(zip(name_list, value_list))
        print("obj dict is:::::::::::::::::::::::::",obj_dict,file=sys.stderr)

        return JSONResponse(content=obj_dict, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            "Error While Fetching The Data\nFor Configuration Change Count By Device Garph",
            500,
        )


@router.get("/ncm_alarm_summery", responses={
    200: {"model": list[NcmAlarmSchema]},
    500: {"model": str}
},
summary="API to show the NCM alarm summary",
description="API to show the NCM alarm summary"
)
async def ncm_alarm_summery():
    try:
        # Execute the query
        results = (
            configs.db.query(NCM_Alarm_Table, NcmDeviceTable, AtomTable)
            .join(
                NcmDeviceTable,
                NCM_Alarm_Table.ncm_device_id == NcmDeviceTable.ncm_device_id
            )
            .join(
                AtomTable,
                AtomTable.atom_id == NcmDeviceTable.atom_id
            )
            .filter(NCM_Alarm_Table.alarm_status == "Open")
            .all()
        )

        # Check the number of results
        print(f"Number of alarms fetched: {len(results)}", file=sys.stderr)

        objList = []
        alarm_count = 0
        for alarm, ncm, atom in results:
            try:
                alarm_count += 1
                print(f"Processing alarm #{alarm_count}", file=sys.stderr)

                # Create a dictionary for the current alarm
                obj_dict = {
                    "ip_address": atom.ip_address,
                    "device_name": atom.device_name,
                    "alarm_category": alarm.alarm_category,
                    "alarm_title": alarm.alarm_title,
                    "alarm_description": alarm.alarm_description,
                    "alarm_status": alarm.alarm_status,
                    "creation_date": alarm.creation_date.isoformat(),
                    "modification_date": alarm.modification_date.isoformat(),
                    "resolve_remarks": alarm.resolve_remarks,
                    "mail_status": alarm.mail_status,
                    "date": alarm.creation_date.date().isoformat(),
                    "time": alarm.creation_date.time().isoformat()
                }

                objList.append(obj_dict)

            except Exception as e:
                print(f"Error processing alarm #{alarm_count}: {e}", file=sys.stderr)

        print(f"Total alarms processed: {alarm_count}", file=sys.stderr)

        # Check if all alarms are processed
        if alarm_count != len(results):
            print(f"Warning: Not all alarms were processed. Processed: {alarm_count}, Fetched: {len(results)}", file=sys.stderr)

        return JSONResponse(content=objList, status_code=200)

    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(
            f"Error While Fetching The Data\nFor Configuration Change Count By Time Graph: {e}",
            500,
        )






@router.get('/ncm_device_summary_by_fucntion',responses={
    200:{"model":list[GetNcmDecivesCountByFucntionSchema]},
    500:{"model":str}
},
summary="API to show the device summary on ncm by function in table",
description="API to show the device summary on ncm by in table"
)
def ncm_device_summary_by_fucntion():
    try:
        query = f"SELECT atom_table.device_type, atom_table.`function`, atom_table.`vendor`,COUNT(*) AS device_count FROM ncm_device_table INNER JOIN atom_table ON ncm_device_table.atom_id = atom_table.atom_id GROUP BY atom_table.device_type, atom_table.`function`,atom_table.`vendor`;"
        result = configs.db.execute(query)
        print("result is::::::::::::::::",result,file=sys.stderr)
        objList = []
        for row in result:
            print("row is::::::::::::::::::::::::::::",row,file=sys.stderr)
            objDict = {}
            objDict["device_type"] = row[0]
            objDict["function"] = row[1]
            objDict['vendor'] = row[2]
            objDict["device_count"] = row[3]
            objList.append(objDict)
        print("obj list is:::::::::::::::::::::::",objList,file=sys.stderr)
        return objList
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured WHile adding ncm device",status_code=500)




# @app.route("/perFunctionCountNcm", methods=["GET"])
# @token_required
# def PerFunctionCountNcm(user_data):
#     try:
#         queryString = f"SELECT AtomTable.`FUNCTION`, COUNT(AtomTable.`FUNCTION`) FROM NcmDeviceTable INNER JOIN AtomTable ON NcmDeviceTable.atom_id = AtomTable.atom_id GROUP  BY AtomTable.`FUNCTION`;"
#         result = db.session.execute(queryString)
#         objList = []
#         for row in result:
#             objDict = {}
#             function = row[0]
#             count = row[1]
#             objDict["name"] = function
#             objDict["value"] = count
#             objList.append(objDict)
#         return jsonify(objList), 200
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return "Server Error", 500
#
#
# @app.route("/ncmBackupCounts", methods=["GET"])
# @token_required
# def NcmBackupCounts(user_data):
#     try:
#         results = NcmDeviceTable.query.all()
#
#         not_backup = 0
#         fail = 0
#         success = 0
#         for ncm in results:
#             if ncm.backup_status is None:
#                 not_backup += 1
#             elif ncm.backup_status is False:
#                 fail += 1
#             elif ncm.backup_status is True:
#                 success += 1
#
#         objDict = {
#             "backup_successful": success,
#             "backup_failure": fail,
#             "not_backup": not_backup,
#         }
#
#         return objDict, 200
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return str(e), 500
#
#
#
#
# @app.route("/ncmAlarmDashboard", methods=["GET"])
# @token_required
# def NCMAlarmDashboard(user_data):
#     try:
#         query = f"SELECT * FROM failed_devices_table t1  WHERE t1.date = (SELECT MAX(t2.date) FROM failed_devices_table t2 WHERE t2.ip_address = t1.ip_address and module ='NCM')  AND t1.module = 'NCM';"
#         return "OK", 200
#     except Exception as e:
#         traceback.print_exc()
#         return "Error While Fetching The Data\nFor Configuration Summery Garph", 500
#
#
# @app.route("/ncmDeviceSummryDashboard", methods=["GET"])
# @token_required
# def NCMDeviceSummryDashboard(user_data):
#     if True:
#         try:
#             query = f"SELECT AtomTable.device_type, AtomTable.`function`, COUNT(*) AS device_count FROM NcmDeviceTable INNER JOIN AtomTable ON NcmDeviceTable.atom_id = AtomTable.atom_id GROUP BY AtomTable.device_type, AtomTable.`function`;"
#             result = db.session.execute(query)
#             objList = []
#             for row in result:
#                 objDict = {}
#                 objDict["device_type"] = row[0]
#                 objDict["function"] = row[1]
#                 objDict["device_count"] = row[2]
#                 objList.append(objDict)
#
#             return jsonify(objList), 200
#         except Exception as e:
#             traceback.print_exc()
#             return "Error While Fetching The Data\nFor Configuration Summery Garph", 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#

#
#
#
#
#200: {"model": list[NCMBackupSummaryConfiguration]},


@router.get("/ncm_backup_summery_dashboard", responses={
    200: {"model": dict},
    500: {"model": str}
},
summary="API to show the ncm backup summary",
description="API to show the ncm backup summary"
)
async def ncm_backup_summery_dashboard():
    try:
        results = configs.db.query(NcmDeviceTable).all()
        print("result is:::::::::::::::::::::::",results,file=sys.stderr)
        not_backup = 0
        fail = 0
        success = 0

        for ncm in results:
            if ncm.backup_status is None:
                not_backup += 1
            elif ncm.backup_status is False:
                fail += 1
            elif ncm.backup_status is True:
                success += 1

        objList = {
            "backup_successful": success,
            "backup_failure": fail,
            "not_backup": not_backup
        }
        print("obj list is::::::::::::::::::::::",objList,file=sys.stderr)
        return JSONResponse(content=objList, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Data", status_code=500)

# /
#/    


@router.get('/get_ncm_alarm_by_category_graph',responses={
    200:{"model":list[GetNcmAlarmCategoryGraph]},
    500:{"model":str}
},
summary="API for getting NCM Alarm category",
description="API to get the ncm alarm category by graph"
)
def ncm_alarm_by_category():
    try:


        configuratoin_query = f"SELECT count(*) FROM ncm_alarm_table  WHERE alarm_category='Configuration';"
        configuration_result = configs.db.execute(configuratoin_query).scalar()

        login_query = f"SELECT count(*) FROM ncm_alarm_table WHERE alarm_category='Login';"
        login_result = configs.db.execute(login_query).scalar()

        open_query = f"SELECT count(*) FROM ncm_alarm_table WHERE alarm_status='Open';"
        open_result = configs.db.execute(open_query).scalar()

        close_query = f"SELECT count(*) FROM ncm_alarm_table WHERE alarm_status='Close';"
        close_result = configs.db.execute(close_query).scalar()

        print("configuration query result is::::::::::::::::::::",configuration_result,file=sys.stderr)
        print("login query result is::::::::::::::::::::::::::::",login_result,file=sys.stderr)
        print("open query result is::::::::::::::::::::::::::::::",open_query,file=sys.stderr)
        print("close query result is::::::::::::::::::::::::::::::",close_result,file=sys.stderr)

        total_count = configuration_result + login_result + open_result + close_result

        print("toal count of all result is:::::::::::::::::::",total_count,file=sys.stderr)

        alarm_category_list = [
            {
                "name":"Configuration",
                "value":configuration_result
            },
            {
                "name":"Login",
                "result":login_result
            },
            {
                "name":"Open",
                "value":open_result
            },
            {
                "name":"Close",
                "value":close_result
            },
            {
                "name":total_count,
            }
        ]

        return alarm_category_list


    except Exception as e:
        traceback.print_exc()


@router.get("/get_vendors_in_ncm", responses={
    200:{"model":GetNcmVendorSchema},
    500:{"model":str}
},
summary="API to get the vendor  in ncm",
description="API to get the vendor in ncm"
)
async def ncm_vendor_count():
    try:
        queryString = (f"SELECT atom_table.vendor, COUNT(*), "
                        f"DATE_FORMAT(ncm_device_table.config_change_date, '%H:%i:%s') AS config_change_time, "
                        f"CAST(DATE(ncm_device_table.config_change_date) AS CHAR) AS config_date "
                        f"FROM ncm_device_table "
                        f"INNER JOIN atom_table ON ncm_device_table.atom_id = atom_table.atom_id "
                        f"GROUP BY vendor, config_change_time, config_date ;")
        print("query string is::::::::::::::::::::::::",queryString,file=sys.stderr)
        result = configs.db.execute(queryString)
        print("reuslt is:::::::::::",result,file=sys.stderr)
        #obj_list = []
        names=[]
        time=[]
        date =[]
        values=[]


        '''for row in result:
            print("row is::::::::::::::::::::::",row,file=sys.stderr)
            print("row [0] is:::::::::::::::",row[0],file=sys.stderr)
            print("row[1] is:::::::::::::::::::",row[1],file=sys.stderr)
            obj_dict = {"name": row[0], "value": row[1]}
            print("obj dict is::::::::::::::::::::",obj_dict,file=sys.stderr)
            if row[0] is None:
                obj_dict["name"] = "Other"'''

        for row in result:
            print("row is::::::::::::::::::::::", row, file=sys.stderr)
            print("row [0] is:::::::::::::::", row[0], file=sys.stderr)
            print("row[1] is:::::::::::::::::::", row[1], file=sys.stderr)
            
            print("config_change_time is:::::::::::::::::::", row[2], file=sys.stderr)
            print("config_date is:::::::::::::::::::", row[3], file=sys.stderr)
            #bj_dict = {"name": row[0], "value": row[1], "config_change_time": row[2]}
            #print("obj dict is::::::::::::::::::::", obj_dict, file=sys.stderr)
            names.append(row[0])
            values.append(row[1])
            time.append(row[2])
            date.append(row[3])
            
            #if row[0] is None:
                #obj_dict["name"] = "Other"        

            #obj_list.append(obj_dict)
            obj_list ={"names": names, "time": time, "date": date, "values": values }
        print("objlist is:::::::::::::::::",obj_list,file=sys.stderr)
        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse("Server Error While Fetching Data", status_code=500)
