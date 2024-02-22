from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.v1.uam.utils.site_utils import *
from app.schema.site_rack_schema import *
from app.models.site_rack_models import *
from app.schema.validation_schema import Response200
from app.schema.response_schema import DeleteResponseSchema


router = APIRouter(
    prefix="/site",
    tags=["site"],
)


@router.post("/add_site", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def add_site(site: AddSiteRequestSchema):
    try:
        response, status = add_site_util(site)
        print("reponse in add site is::::::::::::::::::::::::::::::::::::::::",add_site,file=sys.stderr)
        return JSONResponse(content=response, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Site", status_code=500)


@router.post("/edit_site", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def edit_site(site: EditSiteRequestSchema):
    try:
        response, status = edit_site_util(site)
        print("response is:::::::::::::::::::::::::::::::::",file=sys.stderr)
        return JSONResponse(content=response, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Site", status_code=500)


@router.post("/delete_sites", responses={
    200: {"model": ListtDeleteResponseSchema},
    400: {"model": str},
    500: {"model": str}
})
async def delete_site(site_ids: list[int]):
    try:
        error_list = []
        success_list = []
        deleted_sites = []
       
        for site_id in site_ids:
            print("site id is:::::::::::::::::::::::::::::::::::::::::::::::",site_id,file=sys.stderr)
            msg, status = delete_site_util(site_id)
            
            if status != 200:
                print("status nit 200:::::::::::::::::::::::::::::::::::::",file=sys.stderr)
                error_list.append(msg)
            else:
                for key,value in msg.items():
                    print("key in msg is:::::::::::::::::::::::::::::::::::",key,file=sys.stderr)
                    print("value in msg is ::::::::::::::::::::::::::::",value,file=sys.stderr)
                    if key == "data":
                        # deleted_site_dict = {
                        #     "site_id":value     
                        # }
                        deleted_sites.append(value)
                    elif key == "message":
                        success_list.append(value)
                    else:
                        error_list.append(value)

                # success_list.append(msg)
              
                # print("deleted site id issssssssssssssss::::::::::::::::::::::::::::::",file=sys.stderr)
                # deleted_sites.append(deleted_dict)
                

        response = {
            "data":deleted_sites,
            "error": len(error_list),
            "success": len(success_list),
            "error_list": error_list,
            "success_list": success_list
        }

        return response
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Site", status_code=500)


@router.get("/get_all_sites", responses={
    200: {"model": list[GetSiteResponseSchema]},
    500: {"model": str}
})
async def get_all_site():
    try:

        response = list()

        results = configs.db.query(SiteTable).all()
        for result in results:
            response.append(result.as_dict())

        print(response)
        non_default_sorted = sorted(
            (x for x in response if x['site_name'] != 'default_site'),
            key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )

        # Sort 'default_password' groups and place them at the beginning
        default_site = [x for x in response if x['site_name'] == 'default_site']
        sorted_list = default_site + non_default_sorted
        print("sorted list is::::::::::::::::::::::", sorted_list, file=sys.stderr)

        return JSONResponse(content=sorted_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)


@router.get("/get_sites_dropdown", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_site_dropdown():
    try:
        result = configs.db.query(SiteTable).all()
        response = list()

        for site in result:
            site_name = site.site_name
            response.append(site_name)

        return JSONResponse(content=response, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)


@router.get("/phy_leaf_let",response_model=list[location]
            ,summary="API to get phy_leaf_let",
            description="API to get phy_leaf_let")
async def phy_leaflet():
    try:
        result = configs.db.query(SiteTable).all()
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


@router.get("/top_sites")
async def top_sites():
    try:
        query_string = "SELECT s.SITE_NAME, COUNT(u.UAM_ID) AS DEVICE_COUNT FROM site_table s LEFT JOIN rack_table r ON s.SITE_ID = r.SITE_ID LEFT JOIN atom_table a ON r.RACK_ID = a.RACK_ID LEFT JOIN uam_device_table u ON a.ATOM_ID = u.ATOM_ID GROUP BY s.SITE_NAME;"
        result = configs.db.execute(query_string)

        obj_list = list()

        for row in result:
            site = row[0]
            count = row[1]
            obj_dict = {site: count}
            obj_list.append(obj_dict)

        response = dict()
        for i in obj_list:
            for j in i:
                response[j] = i[j]

        return JSONResponse(content=response, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)


@router.get("/data_centre_status")
async def data_center_status():
    try:
        query_string = (
            f"select distinct STATUS, count(STATUS) from site_table group by STATUS;"
        )
        result = configs.db.execute(query_string)
        obj_list = []

        for row in result:
            status = row[0]
            count = row[1]

            obj_list.append({
                status: count
            })

        response = dict()
        for i in obj_list:
            for j in i:
                print("i in obj list is:::::::::::::::::::::::::::::::",i,file=sys.stderr)
                print("j in i is:::::::::::::::::::::::::::::::::::::::::",j,file=sys.stderr)
                response[j] = i[j]

        return JSONResponse(content=response, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)


@router.get("/total_sites")
async def total_sites():
    try:
        query_string = f"select count(distinct SITE_NAME) from site_table;"
        result = configs.db.execute(query_string).scalar()

        query_string1 = f"select count(distinct DEVICE_NAME) from uam_device_table join atom_table on uam_device_table.atom_id = atom_table.atom_id;"
        result1 = configs.db.execute(query_string1).scalar()

        query_string2 = f"select count(distinct MANUFACTURER) from uam_device_table;"
        result2 = configs.db.execute(query_string2).scalar()

        response = [
            {"name": "Sites", "value": result},
            {"name": "Devices", "value": result1},
            {"name": "Vendors", "value": result2},
        ]

        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Sites", status_code=500)