from fastapi import FastAPI,APIRouter,Query
from starlette.responses import Response
from fastapi.responses import JSONResponse
import traceback
import sys
from datetime import timedelta
from app.core.config import configs
from app.models.ipam_models import *
from app.schema.base_schema import *
from app.schema.ipam_schema import *

#boto3==1.34.30




router = APIRouter(
    prefix = '/ipam_dashboard',
    tags = ['ipam_dashboard']
)


@router.get("/tcp_open_ports", responses={
    200: {"model": PortsValue},
    500: {"model": str}
},
summary="API to get all ports and their obj_list from ip_table",
description="API to get all ports and their obj_list from ip_table"
)
async def tcp_open_ports():
    

    try:
        port_list = []
        port_value =[]
        obj_list=[]
        
        query = (
            "SELECT open_ports, COUNT(open_ports) AS frequency "
            "FROM ip_table "
            "GROUP BY open_ports"
        )

        print("Executing query:", query, file=sys.stderr)
        result = configs.db.execute(query)
        print("results is::::::::::::::::::::::::", result, file=sys.stderr)

        for row in result:
            print("row in result is::::::::::::::::::", row, file=sys.stderr)

            # If the open_ports is None or an empty string, consider it as "None"
            #port = "None" if row[0] is None or row[0] == "" else row[0]

            port_list.append(row[0])
            port_value.append(int(row[1]))

        print("port list is::::::::::::::::::::::::::::", port_list, file=sys.stderr)
        print("port value is::::::::::::::::::::::::::::", port_value, file=sys.stderr)
        if len(port_list) <= 0:
            port_list = ["PortA", "PortB", "PortC", "Other"]
            port_value = [0, 0, 0, 0]


        obj_list=[{"name":port_list,
                   "value":port_value}]    

        
        print("obj dict is:::::::::::::::::::::::::", obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching The Data\nFor Port List and Frequency from ip_table",
            status_code = 500,
        )

        




@router.get("/ip_availability_summary", responses={
    200: {"model": IpAddressobjlist},
    500: {"model": str}
},
summary="API to get status obj_list from ip_table",
description="API to get status obj_list from ip_table"
)
async def ip_availability_summary():
    try:
        query = (
            "SELECT "
            "COUNT(CASE WHEN status = 'available' THEN 1 ELSE NULL END) AS available_ip, "
            "COUNT(CASE WHEN status = 'used' THEN 1 ELSE NULL END) AS used_ip, "
            "COUNT(DISTINCT ip_address) AS total_ip "
            "FROM ip_table"
        )

        print("Executing query:", query, file=sys.stderr)
        result = configs.db.execute(query)
        print("results is::::::::::::::::::::::::", result, file=sys.stderr)

        available_ip = 0
        used_ip = 0
        total_ip = 0

        for row in result:
            print("row in result is::::::::::::::::::", row, file=sys.stderr)

            # Update the obj_list by adding the values from the current row
            available_ip += row[0]
            used_ip += row[1]
            total_ip += row[2]
        
        obj_list = {
            "total_ip": total_ip,
            "used_ip": used_ip,
            "available_ip": available_ip,
        }

        print("status obj_list are::::::::::::::::::::::::::::", obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code =200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching Status obj_list from ip_table",
            status_code = 500,
        )






@router.get("/dns_summary", responses={
    200: {"model": list[ResponseDNSSummary]},
    500: {"model": str}
},
summary="API to get DNS summary status",
description="API to get DNS summary"
)
async def DNS_Summary():
    try:
        query = (
            "SELECT "
            "COUNT(CASE WHEN status = 'available' AND ip_dns = 'Not Found' THEN 1 END) AS not_resolved_ip, "
            "COUNT(CASE WHEN status = 'used' AND ip_dns != 'Not Found' THEN 1 END) AS resolved_ip, "
            "COUNT(DISTINCT ip_address) AS total_ip "
            "FROM ip_table"
        )

        print("Executing query:", query, file=sys.stderr)
        result = configs.db.execute(query)
        print("results is::::::::::::::::::::::::", result, file=sys.stderr)

        not_resolved_ip = 0
        resolved_ip = 0
        obj_list =[]

        for row in result:
            print("row in result is::::::::::::::::::", row, file=sys.stderr)

            # Update the obj_list by adding the values from the current row
            not_resolved_ip += row[0]
            resolved_ip += row[1]
            # total_ip += row["total_ip"]


        obj_list =[
            {"name":"not_resolved_ip","value":not_resolved_ip},
            {"name":"resolved_ip","value": resolved_ip}]
    

        print("status obj_list are::::::::::::::::::::::::::::", obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code =200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching Status obj_list from ip_table",
            status_code = 500,
        )



@router.get("/subnet_summary", responses={
    200: {"model": list[SubnetSummaryResponse]},
    500: {"model": str}
},
summary="API to get subnet_summary",
description="API to get subnet_summary"
)
async def subnet_summary():
    try:
        query = (
            "SELECT "
            "COUNT(CASE WHEN subnet_state = 'manual' THEN 1 ELSE NULL END) AS manually_added, "
            "COUNT(CASE WHEN subnet_state = 'discovered' THEN 1 ELSE NULL END) AS discovered_added, "
            "COUNT(subnet_state) AS total_count "
            "FROM subnet_table"
        )

        print("Executing query:", query, file=sys.stderr)
        result = configs.db.execute(query)
        print("results is::::::::::::::::::::::::", result, file=sys.stderr)
        obj_list =[]

        manually_added = 0
        discovered_added = 0
        # total_count = 0

        for row in result:
            print("row in result is::::::::::::::::::", row, file=sys.stderr)

            # Update the obj_list by adding the values from the current row
            manually_added += row[0]
            discovered_added += row[1]
            #total_count += row[2]
            
            
        obj_list = [{
            "name":"manually_added","value": manually_added},{
            "name":"discovered_added" ,"value": discovered_added} ]
       
        print("subnet_state obj_list are::::::::::::::::::::::::::::", obj_list, file=sys.stderr)
        return JSONResponse(content=obj_list, status_code = 200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching subnet_state obj_list from subnet_table",
            status_code = 500,
        )


@router.get("/type_summary", responses={
    200: {"model": List[TypeSummaryResponse]},
    500: {"model": str}
},
summary="API to get type_summary",
description="API to get type_summary"
)
async def type_summary():
    try:
        query = (
                f"SELECT atom_table.vendor, COUNT(*) AS obj_list "
                f"FROM  ipam_devices_fetch_table "
                f"INNER JOIN atom_table ON ipam_devices_fetch_table.atom_id = atom_table.atom_id "
                f"GROUP BY vendor;")

        #print("query string is::::::::::::::::::::::::",query=sys.stderr)
        result = configs.db.execute(query)
        print("reuslt is:::::::::::",result,file=sys.stderr)
        objt_list=[]
        print("result...............",result , file = sys.stderr)

        for row in result:
            print("row is::::::::::::::::::::::", row, file=sys.stderr)
            print("row [0] is:::::::::::::::", row[0], file=sys.stderr)
            print("row[1] is:::::::::::::::::::", row[1], file=sys.stderr)
            objt_dict = {"vender": row[0],"obj_list": row[1]}
            print("obj dict is::::::::::::::::::::", objt_dict, file=sys.stderr)
            objt_list.append(objt_dict)
   

        print("objlist is:::::::::::::::::", objt_list, file=sys.stderr)
        return  JSONResponse(content=objt_list, status_code = 200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            content = "Error While Fetching subnet_state obj_list from subnet_table",
            status_code = 500,
        )
    


@router.get('/top_10_subnet_ip_used', responses={
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
    

