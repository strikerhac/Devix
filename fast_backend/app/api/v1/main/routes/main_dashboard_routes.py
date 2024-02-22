from fastapi import FastAPI,APIRouter,Query
from starlette.responses import Response
from fastapi.responses import JSONResponse
import traceback
import sys
from decimal import Decimal
import json
from sqlalchemy import text , func
from datetime import datetime, timedelta
from app.core.config import configs
from app.models.ipam_models import *
from app.schema.base_schema import *
from app.schema.ipam_schema import *
#from app.core.config import configs
from app.models.atom_models import *
from app.models.ncm_models import *
#from app.schema.base_schema import *
from app.schema.ncm_schema import *
from app.api.v1.auto_discovery.auto_discovery_utils import *
from app.schema.base_schema import NameValueListOfDictResponseSchema, NameValueDictResponseSchema
from app.api.v1.monitoring.device.utils.monitoring_utils import *
from app.models.atom_models import *
from app.models.monitoring_models import *
from app.schema.monitoring_schema import *
from starlette.responses import Response
from app.api.v1.uam.utils.site_utils import *
from app.schema.site_rack_schema import *
from app.models.site_rack_models import *
from app.schema.validation_schema import Response200
from app.schema.response_schema import DeleteResponseSchema

router = APIRouter(
    prefix = '/main_dashboard',
    tags = ['main_dashboard']
)



@router.get('/main_top_10_subnet_ip_used', responses={
    200: {"model":dict},
    500: {"model": str}
}, summary="API to get top 10_subnet_ip_used",
description="API to get top_10_subnet_ip_used"
)
def top_10_subnet_ip_used():
    try:
        query = (
            "SELECT subnet_table.subnet_address, subent_usage_table.subnet_usage "
            "FROM subnet_table "
            "INNER JOIN subent_usage_table ON subnet_table.subnet_id = subent_usage_table.subnet_id"
        )

        result = configs.db.execute(query)
        print("result is::::::::::::::::", result, file=sys.stderr)
        
        subnet_address_list = []
        subnet_usage_list = []
        newsubnet_usage_list = []

        for row in result:
            print("row is::::::::::::::::::::::::::::", row, file=sys.stderr)
            subnet_address_list.append(row[0])
            subnet_usage_list.append(row[1])
        
        if len(subnet_address_list) <= 0:
            subnet_address_list = ["SubnetA", "subnetB", "Other"]
            subnet_usage_list= [0, 0, 0]
            obj_dict = {"subnet_address": subnet_usage_list, "subnet_usage": subnet_usage_list }
            print("obj dict is:::::::::::::::::::::::::", obj_dict, file=sys.stderr)
        else:
            for  usage in subnet_usage_list:
                if usage is None :
                    usage = '0.0'
                    newsubnet_usage_list.append(usage)
                else:
                    newsubnet_usage_list.append(usage)
            print(newsubnet_usage_list)
            subnets_data = list(zip(subnet_address_list, newsubnet_usage_list))
            sorted_subnets = sorted(subnets_data, key=lambda x: x[1], reverse=True)
            result_list = [{"subnet": subnet, "value": value} for subnet, value in sorted_subnets[:10]]
            
        print("obj dict is:::::::::::::::::::::::::", result_list, file=sys.stderr)
        return JSONResponse(content= result_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
           content =  "Error While Fetching The Data\nFor subnet_address and subnet_usage from subnet_table , subent_usage_table",
            status_code = 500,
        )
    



@router.get("/main_change-configuration-by-time", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary="API to get change-configuration-by-time",
description="API to get change-configuration-by-time"
)
async def ncm_change_summary_by_time():
    current_time = datetime.now()
    try:
        query = (f"SELECT COUNT(*) AS backup_count, "
                     f"DATE_FORMAT(config_change_date, '%m') "
                     f"AS month_interval FROM ncm_device_table "
                     f"WHERE config_change_date IS NOT NULL "
                     f"GROUP BY month_interval ORDER BY backup_count DESC;")

        result = configs.db.execute(query)
        print("result......",result , file =sys.stderr)
        name_list = []
        value_list = []
        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for row in result:
            print("row",row)
            
            #current_month_value = int(current_time.strftime('%m'))
            month_value =int(row[1])
            print("current_month", month_value)
            month_name = month_names[month_value]
            print("month_name",month_name)
            name_list.append(month_name)
            print(name_list)
            value_list.append(int(row[0]))
            print(value_list)
        
        
        if len(name_list) <= 0:
            # Adjust this logic based on your requirements
            # Here, it adds the current month and the previous month
            name_list.append('month')
            value_list.append(0)
            #name_list.append((current_time - timedelta(days=30)).strftime('%m'))
            #value_list.append(0)

        obj_dict = {"name": name_list, "value": value_list}

        return JSONResponse(content=obj_dict, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            "Error While Fetching The Data\nFor Configuration Change Count By Time Graph",
            500,
        )


@router.get("/main_top_vendors_for_discovery", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
}, 
summary ="API to get top vendors for discovery",
description = "API to get top vendors for discovery"
)

async def get_top_vendors_for_discovery():
    try:
        query_string = (f"SELECT vendor,COUNT(vendor) AS count FROM "
                        f"auto_discovery_table GROUP BY vendor ORDER BY count DESC LIMIT 10;")
        result = configs.db.execute(query_string)

        obj_list = []
        for row in result:
            #print(row[0])
            #print(row[1])
            obj_list.append({"name": row[0], "value": row[1]})
        print("objlist is::::::::::::::::::::::::::::", obj_list, file=sys.stderr)

        if  len(obj_list) <=0:
            obj_list=[{"name": "vender", "value": 0}]
            print("obj_list is::::::::::::::::::::::::::::", obj_list, file=sys.stderr)

            return   JSONResponse(content=obj_list, status_code=200)  

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)



@router.get("/main_snmp_status_graph", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary ="API to get snmp status graph",
description = "API to snmp status graph"
)
async def get_snmp_status_graph():
    try:
        query_string = (f"SELECT snmp_status, COUNT(snmp_status) FROM "
                        f"auto_discovery_table GROUP BY snmp_status;")
        result = configs.db.execute(query_string)

        enable = 0
        disable = 0
        obj_list =[]
        for row in result:
            if row[0] == "Enabled":
                enable += row[1]
            else:
                disable += row[1]

        obj_list = [
            {"name": "SNMP Enabled", "value": enable},
            {"name": "SNMP Disabled", "value": disable},
        ]

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)
    

@router.get("/main_credentials_graph", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary="API to get credentials graph",
description="API to get credentials graph"
)
async def get_credentials_graph():
    try:
       # obj_list = []

        obj_dict = {
            "name": ["SNMP V1/V2", "SNMP V3", "SSH Login"],
            "value": [0, 0, 0],
        }

       
        ssh_query = text("SELECT count(*) FROM password_group_table WHERE password_group_type='SSH';")
        ssh_result = configs.db.execute(ssh_query).scalar()
        obj_dict["value"][2] = ssh_result

        
        v1_v2_query = text("SELECT count(*) FROM snmp_credentials_table WHERE category='v1/v2';")
        v1_v2_result = configs.db.execute(v1_v2_query).scalar()
        obj_dict["value"][0] = v1_v2_result

        
        v3_query = text("SELECT count(*) FROM snmp_credentials_table WHERE category='v3';")
        v3_result = configs.db.execute(v3_query).scalar()
        obj_dict["value"][1] = v3_result

        #obj_list.append(obj_dict)

        if len(obj_dict) <= 0:
            return JSONResponse(content=obj_dict, status_code=200)

        return JSONResponse(content=obj_dict, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)




@router.get("/main_counts_per_vender", responses={
    200: {"model": List[TypeSummaryResponse]},
    500: {"model": str}
},
summary="API to get counts per vender",
description="API to get counts per vender"
)
async def type_summary():
    try:
        query = (
                f"SELECT atom_table.vendor, COUNT(*) AS counts "
                f"FROM  ipam_devices_fetch_table "
                f"INNER JOIN atom_table ON ipam_devices_fetch_table.atom_id = atom_table.atom_id "
                f"GROUP BY vendor;")

        #print("query string is::::::::::::::::::::::::",query=sys.stderr)
        result = configs.db.execute(query)
        print("reuslt is:::::::::::",result,file=sys.stderr)
        objt_list=[]

        for row in result:
            print("row is::::::::::::::::::::::", row, file=sys.stderr)
            print("row [0] is:::::::::::::::", row[0], file=sys.stderr)
            print("row[1] is:::::::::::::::::::", row[1], file=sys.stderr)
            objt_dict = {"vender": row[0],"counts": row[1]}
            print("obj dict is::::::::::::::::::::", objt_dict, file=sys.stderr)
            objt_list.append(objt_dict)
   

        print("objlist is:::::::::::::::::", objt_list, file=sys.stderr)
        return  JSONResponse(content=objt_list, status_code = 200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching subnet_state Counts from subnet_table",
            status_code = 500,
        )
    
@router.get("/main_phy_leaf_let",response_model=list[location]
            ,summary="API to get phy_leaf_let",
            description="API to get phy_leaf_let")
async def phy_leaflet(site_name : str = Query(...,description="Name of the site")):
    try:
        result = (
            configs.db.query(SiteTable)
            .filter(SiteTable.site_name == site_name)
            .all()
        )
        print("result in py leaflet is ::::::::::::::::::::::::::::::::",result,file=sys.stderr)
        response = []
        obj_dict ={}

        for site in result:
            print("site is::::::::::::::::::::::::::::::::::::::::::::::::::",site,file=sys.stderr)
            obj_dict = {"name":"site_name", "value":site.site_name,
                        "name":"city", "value":site.city}
            response.append(obj_dict)

        if not response:
            response ={"name":"site_name", "value":"none" ,
                        "name":"city", "value":"none"}

            return JSONResponse(content=response, status_code=200)
        
        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)




@router.get("/main_device_status", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary = "Use this API in UAM Devices pAge in device status overview to display the count of Production,Dismantled,Undefined devices ",
description = "Use this API in UAM Devices pAge in device status overview to display the count of Production,Dismantled,Undefined devices ")
async def device_status():
    try:
        obj_list = [
            {"name": "Production", "value": 0},
            {"name": "Dismantled", "value": 0},
            {"name": "Maintenance", "value": 0},
            {"name": "Undefined", "value": 0},
        ]

        query = f"select count(*) from uam_device_table;"
        result0 = configs.db.execute(query).scalar()
        if result0 != 0:
            query_string = (
                f"select count(status) from uam_device_table where STATUS='Production';"
            )
            result = configs.db.execute(query_string).scalar()

            query_string1 = (
                f"select count(status) from uam_device_table where STATUS='Dismantled';"
            )
            result1 = configs.db.execute(query_string1).scalar()

            query_string2 = f"select count(status) from uam_device_table where STATUS='Maintenance';"
            result2 = configs.db.execute(query_string2).scalar()

            query_string3 = (
                f"select count(status) from uam_device_table where STATUS='Undefined';"
            )
            result3 = configs.db.execute(query_string3).scalar()
            obj_list = [
                {"name": "Production", "value": round(((result / result0) * 100), 2)},
                {"name": "Dismantled", "value": round(((result1 / result0) * 100), 2)},
                {"name": "Maintenance", "value": round(((result2 / result0) * 100), 2)},
                {"name": "Undefined", "value": round(((result3 / result0) * 100), 2)},
            ]

        print(obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Uam Data", status_code=500)



@router.get("/main_memory_dashboard", responses={
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
        print("last_list.................",last_list,file=sys.stderr)
        if len(last_list) > 4:
            print("last_list.................",last_list,file=sys.stderr)
            return JSONResponse(content=last_list[0:4], status_code=200)
        else:
            return JSONResponse(content=last_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


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
    



'''@router.get("/main_location", responses={
    200: {"model": List[getLocationDevice]},
    500: {"model": str}
},
summary="API to get location devices ",
description="API to get location devices"
)
async def type_summary():
    try:
        query = (
                f"SELECT "
                f"site_table.site_id"
                f"rack_table.rack_id "
                f"atom_table.device_name "
                f"atom_table.onboard_status "
                f"atom_table.virtual  "  # Remove this line
                f"atom_table.device_name COUNT(*) AS device_counts "  # Add a comma after 'virtual'
                f"SUM(CASE WHEN atom_table.onboard_status = True THEN 1 ELSE 0 END) AS onboard_counts "
                f"SUM(CASE WHEN atom_table.virtual = 'virtual' THEN 1 ELSE 0 END) AS virtual_counts "
                f"SUM(CASE WHEN atom_table.virtual = 'non-virtual' THEN 1 ELSE 0 END) AS physical_counts "
                f"FROM atom_table "
                f"LEFT JOIN rack_table ON atom_table.atom_id = rack_table.atom_id "
                f"LEFT JOIN site_table ON rack_table.rack_id = site_table.rack_id "
                f"GROUP BY  site_table.site_id , rack_table.rack_id, atom_table.device_name, atom_table.onboard_status, atom_table.virtual;"
            )
                
        #print("query string is::::::::::::::::::::::::",query=sys.stderr)
        result = configs.db.execute(query)
        print("reuslt is:::::::::::",result,file=sys.stderr)
        objt_list=[]

        for row in result:
            print("row is::::::::::::::::::::::", row, file=sys.stderr)
            print("row [0] is:::::::::::::::", row[0], file=sys.stderr)
            print("row[1] is:::::::::::::::::::", row[1], file=sys.stderr)
            print("row[2] is:::::::::::::::::::", row[2], file=sys.stderr)
            print("row[3] is:::::::::::::::::::", row[3], file=sys.stderr)
            objt_dict = {{"name": "total_devices","values": row[0]}, {"name": "onboard_devices","values": row[1]},
                         {"name": "virtual","values": row[2]},{"name": "physical","values": row[3]}}
            print("obj dict is::::::::::::::::::::", objt_dict, file=sys.stderr)
            objt_list.append(objt_dict)


        if len(objt_list)<=0:
            objt_dict = {{"name": "total_devices","values": 0 }, {"name": "onboard_devices","values": 0},
                         {"name": "virtual","values": 0 },{"name": "physical","values": 0 }}
            objt_list.append(objt_dict)
            return  JSONResponse(content=objt_list, status_code = 200)


        print("objlist is:::::::::::::::::", objt_list, file=sys.stderr)
        return  JSONResponse(content=objt_list, status_code = 200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching subnet_state Counts from subnet_table",
            status_code = 500,
        )'''
    
    


@router.get("/main_location", responses={
    200: {"model": List[getLocationDevice]},
    500: {"model": str}
},
summary="API to get location devices",
description="API to get location devices"
)
async def type(region_name: str = Query(..., description="Region Name for filtering")):
    try:
        result = (
            configs.db.query(SiteTable,SiteTable.site_id)
            .filter(SiteTable.region_name == region_name)
            .first() 
        )
     
            


        print('site_id...............',result, file =sys.stderr)
        site_id = result.site_id
        obj_list = []
        '''result = (
                configs.db.query(
                    AtomTable,
                    RackTable,
                    SiteTable,
                    func.count(AtomTable.device_name).label("total_device_count"),
                    func.sum(func.case([(AtomTable.onboard_status == 1, 1)], else_=0)).label("onboard_status_count"),
                    func.sum(func.case([(AtomTable.virtual == 'virtual', 1)], else_=0)).label("virtual_count"),
                    func.sum(func.case([(AtomTable.virtual != 'virtual', 1)], else_=0)).label("non_virtual_count")
                )
                .join(RackTable, AtomTable.rack_id == RackTable.rack_id)
                .join(SiteTable, RackTable.site_id == SiteTable.site_id)
                .filter(SiteTable.site_id == site_id)
                .group_by(AtomTable.device_name, AtomTable.rack_id, AtomTable.onboard_status, AtomTable.virtual)
                .first()
            )'''
        result =(
            configs.db.query(AtomTable,
                    RackTable,
                    SiteTable,func.count(AtomTable.device_name).label("total_device_count"))
                    .join(RackTable, AtomTable.rack_id == RackTable.rack_id)
                    .join(SiteTable, RackTable.site_id == SiteTable.site_id)
                    .filter(SiteTable.site_id == site_id)
                    .group_by(AtomTable.device_name.isnot(None))
                    .first()


        )

        if result is None:
            total_device_count=0

        atom_table_instance, rack_table_instance, site_table_instance, total_device_count = result
        obj_list = [{"name":"devices","value":total_device_count}
        ]
        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Site Data", status_code=500)


@router.get("/main_device_status", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary = "Use this API in UAM Devices pAge in device status overview to display the count of Production,Dismantled,Undefined devices ",
description = "Use this API in UAM Devices pAge in device status overview to display the count of Production,Dismantled,Undefined devices ")
async def device_status():
    try:
        obj_list = [
            {"name": "Production", "value": 0},
            {"name": "Dismantled", "value": 0},
            {"name": "Maintenance", "value": 0},
            {"name": "Undefined", "value": 0},
        ]

        query = f"select count(*) from uam_device_table;"
        result0 = configs.db.execute(query).scalar()
        if result0 != 0:
            query_string = (
                f"select count(status) from uam_device_table where STATUS='Production';"
            )
            result = configs.db.execute(query_string).scalar()

            query_string1 = (
                f"select count(status) from uam_device_table where STATUS='Dismantled';"
            )
            result1 = configs.db.execute(query_string1).scalar()

            query_string2 = f"select count(status) from uam_device_table where STATUS='Maintenance';"
            result2 = configs.db.execute(query_string2).scalar()

            query_string3 = (
                f"select count(status) from uam_device_table where STATUS='Undefined';"
            )
            result3 = configs.db.execute(query_string3).scalar()
            obj_list = [
                {"name": "Production", "value": round(((result / result0) * 100), 2)},
                {"name": "Dismantled", "value": round(((result1 / result0) * 100), 2)},
                {"name": "Maintenance", "value": round(((result2 / result0) * 100), 2)},
                {"name": "Undefined", "value": round(((result3 / result0) * 100), 2)},
            ]

        print(obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Uam Data", status_code=500)
       