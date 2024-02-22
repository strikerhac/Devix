from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1.auto_discovery.auto_discovery_utils import *
from app.schema.base_schema import NameValueListOfDictResponseSchema, NameValueDictResponseSchema

router = APIRouter(
    prefix="/auto_discovery_dashboard",
    tags=["auto_discovery_dashboard"],
)


@router.get("/get_top_os_for_discovery", responses={
    200: {"model": list[NameValueListOfDictResponseSchema]},
    500: {"model": str}
},
summary="API to get top os for discovery ",
description=" API to get os for discovery"

)
async def get_top_os_for_discovery():
    try:
        query_string = (f"SELECT os_type,COUNT(os_type) AS count FROM "
                        f"auto_discovery_table GROUP BY OS_TYPE "
                        f"ORDER BY count DESC LIMIT 10;")
        result = configs.db.execute(query_string)
        print(result)
        obj_list = []
        for row in result:
            print("results is::::::::::::::::::::::::",  row[0], file=sys.stderr)
            print("results is::::::::::::::::::::::::",  row[1], file=sys.stderr)

            obj_list.append({"name": row[0], "value": row[1]})
        if  len(obj_list) <=0:
            obj_list=[{"name": "os", "value": 0}]
            print("obj_list is::::::::::::::::::::::::::::", obj_list, file=sys.stderr)
            return   JSONResponse(content=obj_list, status_code=200)  

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_top_vendors_for_discovery", responses={
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


@router.get("/get_snmp_status_graph", responses={
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



'''@router.get("/get_credentials_graph", responses={
    200: {"model": list[NameValueDictResponseSchema]},
    500: {"model": str}
},
summary ="API to get credentials graph ",
description = "API to get credentials graph"
)
async def get_credentials_graph():
    try:
        obj_list=[]
        obj_dict = {
            "name": ["SNMP V1/V2", "SNMP V3", "SSH Login"],
            "value": [0, 0, 0],
        }

        query_string = (f"SELECT snmp_version, COUNT(snmp_version) FROM "
                        f"auto_discovery_table GROUP BY snmp_version;")
        result = configs.db.execute(query_string)

        for row in result:
            if (row[0]) == "SNMPv2-MIB":
                obj_dict["value"][0] = row[1]
            elif (row[0]) == "SNMPv3-MIB":
                obj_dict["value"][1] = row[1]

        query_string = (f"SELECT ssh_status, COUNT(ssh_status) FROM "
                        f"auto_discovery_table GROUP BY ssh_status;")
        ssh_query = f"SELECT count(*) FROM password_group_table where password_group_type=='SSH';"
        ssh_result = configs.db.query(ssh_query).scalar()
        result1 = configs.db.execute(ssh_result)


        v1_v2_query = f"SELECT count(*) FROM  snmp_credentials_table where category=='v1/v2';"
        v1_v2_result = configs.db.query(ssh_query).scalar()
        result2 = configs.db.execute(v1_v2_result)

        v3_query = f"SELECT count(*) FROM  snmp_credentials_table where category=='v3';"
        v3_result = configs.db.query(ssh_query).scalar()
        result2 = configs.db.execute(v3_result)
        credentials_dict = [
            {
                "name":"v1_v2",
                "value":ssh_result
            }
        ]
        for row in result:
            if (row[0]) == "True":
                obj_dict["value"][2] = row[1]
        obj_list = ["name":]
        
        if  len(obj_dict) <=0:
            obj_list=[{
            "name": ["SNMP V1/V2", "SNMP V3", "SSH Login"],
            "value": [0, 0, 0]}]
            print("obj_list is::::::::::::::::::::::::::::", obj_list, file=sys.stderr)
            return   JSONResponse(content=obj_list, status_code=200)  
        obj_list=[obj_dict]
        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)'''



'''@router.get("/get_credentials_graph", responses={
    200: {"model": list[NameValueDictResponseSchema]},
    500: {"model": str}
},
summary="API to get credentials graph",
description="API to get credentials graph"
)
async def get_credentials_graph():
    try:
        obj_list = []

        # Initialize obj_dict with default values
        obj_dict = {
            "name": ["SNMP V1/V2", "SNMP V3", "SSH Login"],
            "value": [0, 0, 0],
        }

        # Query SSH count
        ssh_query = text("SELECT count(*) FROM password_group_table WHERE password_group_type='SSH';")
        ssh_result = configs.db.query(ssh_query).scalar()
        obj_dict["value"][2] = ssh_result

        # Query SNMP v1/v2 count
        v1_v2_query = f"SELECT count(*) FROM snmp_credentials_table WHERE category='v1/v2';"
        v1_v2_result = configs.db.query(v1_v2_query).scalar()
        obj_dict["value"][0] = v1_v2_result

        # Query SNMP v3 count
        v3_query = f"SELECT count(*) FROM snmp_credentials_table WHERE category='v3';"
        v3_result = configs.db.query(v3_query).scalar()
        obj_dict["value"][1] = v3_result

        obj_list.append(obj_dict)

        if len(obj_list) <= 0:
            return JSONResponse(content=obj_list, status_code=200)

        return JSONResponse(content=obj_list, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)'''


#from sqlalchemy import text

@router.get("/get_credentials_graph", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary="API to get credentials graph",
description="API to get credentials graph"
)
async def get_credentials_graph():
    try:
        obj_list = []

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

@router.get("/get_top_functions_for_discovery", responses={
    200: {"model": NameValueDictResponseSchema},
    500: {"model": str}
},
summary ="API to get get top functions for discovery ",
description = "API to get get top functions for discovery "
)
async def get_top_functions_for_discovery():
    try:
        query_string = (f"SELECT `function`,COUNT(`function`) AS count FROM "
                        f"auto_discovery_table GROUP BY `function` ORDER BY count DESC LIMIT 5;")
        result = configs.db.execute(query_string)

        '''obj_dict = {"name": [], "value": []}
        for row in result:
            obj_dict["name"].append(row[0].capitalize())
            obj_dict["value"].append(row[1])

        return JSONResponse(content=obj_dict, status_code=200)'''
        obj_list = {}
        name=[]
        value=[]
        for row in result:
            name.append(row[0].capitalize())
            value.append(row[1])
        obj_list = {"name": name, "value": value}

        print("result..................",obj_list,file=sys.stderr)    
        if len(obj_list)<=0:
            obj_list={{"name": "port", "value": 0}}
            return JSONResponse(content=obj_list, status_code=200)

        #print("result..................",obj_list,file=sys.stderr)
        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)

