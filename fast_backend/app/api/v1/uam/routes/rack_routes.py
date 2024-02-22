from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query
from app.api.v1.uam.utils.rack_utils import *
from app.schema.site_rack_schema import *
from app.models.site_rack_models import *
from app.schema.validation_schema import Response200
from app.schema.base_schema import DeleteResponseSchema

router = APIRouter(
    prefix="/rack",
    tags=["rack"],
)


@router.post("/add_rack", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def add_rack(rack: AddRackRequestSchema):
    try:
        response, status = add_rack_util(rack)
        print("repsoones in add rack is:::::::::::::::::",rack,file=sys.stderr)
        if status == 200:
            return response
        elif status == 400:
            return JSONResponse(content=response, status_code=400)
        # response = json.dumps(response, default=str)
        # print("repsonse with the jsoon dumpt is:::::::::::::::::::::",response,file=sys.stderr)
        
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Rack", status_code=500)


@router.post("/edit_rack", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def edit_rack(rack: EditRackRequestSchema):
    try:
        response, status = edit_rack_util(rack)
        print("response is:::::::::::::::::::::::::::::::::::::::",response,file=sys.stderr)
        if status == 200:
            return response
        elif status == 400:
            return JSONResponse(content=response, status_code=400)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Updating Rack", status_code=500)


@router.post("/delete_rack", responses={
    200: {"model": DeleteResponseSchema},
    400: {"model": str},
    500: {"model": str}
})
async def delete_rack(rack_ids: list[int]):
    try:
        response, status = delete_rack_util(rack_ids)
        print("repsosne is:::::::::::::::::::::::::::::::::",response,file=sys.stderr)
        return JSONResponse(content=response, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Deleting Rack", status_code=500)


@router.get("/get_racks_by_site_dropdown", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_rack_by_site(site_name: str = Query(...,description="Name of the site")):
    try:
        obj_list = []
        site_obj = site_name
        print("site obj is::::::::::::::::",site_obj,file=sys.stderr)
        result = (
            configs.db.query(RackTable, SiteTable)
            .join(SiteTable, RackTable.site_id == SiteTable.site_id)
            .filter(SiteTable.site_name == site_name)
            .all()
        )
        print("result is:::::::::::::::::::::::::",result,file=sys.stderr)

        for rack, site in result:
            rack_name = rack.rack_name
            obj_list.append(rack_name)

        return JSONResponse(content=obj_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)


@router.get("/get_rack_by_rack_name", responses={
    200: {"model": list[GetRackResponseSchema]},
    500: {"model": str}
})
async def get_rack_by_rack_name(rack_name: str = Query(...,description="Name of the rack")):
    try:
        response, status = get_rack_details_by_rack_name(rack_name)
        return JSONResponse(content=response, status_code=status)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)


@router.get("/get_all_racks", responses={
    200: {"model": list[GetRackResponseSchema]},
    500: {"model": str}
})
async def get_all_racks():
    try:
        response = get_all_rack()
        # print("reposne in get all racks is::::::::::::::::::::::::::::::::::::::::",response,file=sys.stderr)
        non_default_sorted = sorted(
            (x for x in response if x['rack_name'] != 'default_rack'),
            key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%d %H:%M:%S') if isinstance(x['creation_date'],
                                                                                                   str) else x[
                'creation_date'],
            reverse=True
        )

        # Sort 'default_rack' and place it at the beginning
        default_rack = [x for x in response if x['rack_name'] == 'default_rack']
        sorted_list = default_rack + non_default_sorted

        return sorted_list


    except Exception:
            traceback.print_exc()
            return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)

# GetTotalRacksSchema
@router.get("/get_total_racks",responses={
    200: {"model": list[GetTotalRacksSchema]},
    500: {"model": str}
})
async def total_racks():
    try:
        query_string = f"select count(distinct RACK_NAME) from rack_table;"
        result = configs.db.execute(query_string).scalar()

        query_string1 = f"select count(*) from uam_device_table;"
        result1 = configs.db.execute(query_string1).scalar()

        query_string2 = f"select sum(RU) from rack_table;"
        result2 = configs.db.execute(query_string2).scalar()

        obj_list = [
            {"name": "Racks", "value": result if result is not None else 0},
            {"name": "Devices", "value": result1 if result1 is not None else 0},
            {"name": "Total RU", "value": result2 if result2 is not None else 0},
        ]

        return obj_list

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)

RackLeafLetSchema
@router.get("/get_rack_leaf_let",responses={
    200: {"model": list[RackLeafLetSchema]},
    500: {"model": str}
})
async def rack_leaflet():
    try:
        query_string = f"select LONGITUDE,LATITUDE from site_table where site_id in (select site_id from rack_table);"
        result = configs.db.execute(query_string)

        obj_list = []
        for row in result:
            longitude = row[0]
            latitude = row[1]
            obj_dict = {"longitude": longitude, "latitude": latitude}
            obj_list.append(obj_dict)

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)


@router.get("/get_all_floors",responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def all_floors():
    try:

        obj_list = []
        query_string = f"select FLOOR from rack_table;"
        result = configs.db.execute(query_string)

        for row in result:
            floor = row[0]
            obj_list.append(floor)
        print(obj_list, file=sys.stderr)

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)


# @router.get("/get_all_racks_dropdwon",responses={
#     200: {"model": list[GetRackResponseSchema]},
#     500: {"model": str}
# })
# async def all_racks():
#     try:
#         obj_list = []
#         racks = get_all_rack()
#         print("racks are::::::::::::::::::::::",racks,file=sys.stderr)

#         for rack in racks:
#             obj_list.append(rack["rack_name"])

#         print(obj_list, file=sys.stderr)

#         return obj_list

#     except Exception:
#         traceback.print_exc()
#         return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)

TopRacksSchema
@router.get("/get_top_racks",responses={
    200: {"model": list[TopRacksSchema]},
    500: {"model": str}
})
async def top_racks():
    try:
        query_string = f"select site_table.site_name,count(rack_name) from rack_table inner join site_table on rack_table.site_id = site_table.site_id group by site_name order by count(rack_name) DESC;"
        result = configs.db.execute(query_string)

        obj_list = []
        for row in result:
            sites = row[0]
            count = row[1]
            obj_dict = {"name": sites, "value": count}
            obj_list.append(obj_dict)

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Rack", status_code=500)



@router.get('/testingRoute')
def testing_route():
    try:
        return {"message":"testing route"}
    except Exception as e:
        traceback.print_exc()