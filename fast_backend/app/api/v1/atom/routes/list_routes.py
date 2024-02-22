import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.utils.static_list import *

router = APIRouter(
    prefix="/static_list",
    tags=["static_list"],
)


@router.get("/get_vendor_list", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_vendor_list():
    try:
        return JSONResponse(content=vendor_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Vendor List", status_code=500)


@router.get("/get_device_type_list", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_device_type_list():
    try:
        return JSONResponse(content=device_type_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Device Type List", status_code=500)



@router.get("/get_function_list", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_function_list():
    try:
        return JSONResponse(content=function_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Fucntion List", status_code=500)

@router.get("/get_password_group_type_dropdown",
            responses={
                    200: {"model": list[str]},
                    500: {"model": str}}
            )
def password_group_type():
    try:
        return JSONResponse(content = password_group_types_list,status_code = 200)
    except Exception as e:
        traceback.print_exc()

@router.get('/get_status_dropdown',responses={
                    200: {"model": list[str]},
                    500: {"model": str}})
def status_dropdown():
    try:
        return JSONResponse(content =status_list,status_code = 200 )
    except Exception as e:
        traceback.print_exc()




@router.get('/get_virutal_values_dropdown',responses={
                    200: {"model": list[str]},
                    500: {"model": str}})
def virtual_dropdown():
    try:
        return JSONResponse(content =virutal_list,status_code = 200 )
    except Exception as e:
        traceback.print_exc()




@router.get('/get_criticality_values_dropdown',responses={
                    200: {"model": list[str]},
                    500: {"model": str}})
def criticality_dropdown():
    try:
        return JSONResponse(content =criticality_list,status_code = 200 )
    except Exception as e:
        traceback.print_exc()