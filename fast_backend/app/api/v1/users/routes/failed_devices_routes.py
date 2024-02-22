from fastapi import FastAPI,APIRouter
from fastapi.responses import JSONResponse
from app.models.users_models import *
from app.schema.users_schema import *
from app.core.config import *
from app.utils.db_utils import *
from app.models.common_models import *
import sys
import traceback


router = APIRouter(
    prefix="/failed_devices",
    tags=['failed_devices']
)



@router.get("/get_ipam_failed_devices",
            responses={
                200:{"model":list[FailedDevicesResponseSchema]},
                500:{"model":str}
            },
summary="API to get all the IPAM failed device",
description="API to get all the IPAM failed devices"
)
def get_ipam_failed_devices():
    try:
        failed_list = []
        failed_devices = configs.db.query(FailedDevicesTable).filter_by(module="IPAM").all()
        for devices in failed_devices:
            failed_dict = {
                "failure_id":devices.failure_id,
                "ip_address":devices.ip_address,
                "device_type":devices.device_type,
                "date":devices.date,
                "failure_reason":devices.failure_reason,
                "module":devices.module
            }
            failed_list.append(failed_dict)
        return failed_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting IPAM failed Devices",status_code=500)



@router.get("/get_uam_failed_devices",
            responses={
                200:{"model":list[FailedDevicesResponseSchema]},
                500:{"model":str}
            },
summary="API to get all the UAM failed device",
description="API to get all the UAM failed devices"
)
def get_uam_failed_devices():
    try:
        failed_list = []
        failed_devices = configs.db.query(FailedDevicesTable).filter_by(module="UAM").all()
        for devices in failed_devices:
            failed_dict = {
                "failure_id":devices.failure_id,
                "ip_address":devices.ip_address,
                "device_type":devices.device_type,
                "date":devices.date,
                "failure_reason":devices.failure_reason,
                "module":devices.module
            }
            failed_list.append(failed_dict)
        return failed_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting UAM failed Devices",status_code=500)

@router.get("/get_auto_discovery_failed_devices",
            responses={
                200:{"model":list[FailedDevicesResponseSchema]},
                500:{"model":str}
            },
summary="API to get all the IPAM failed device",
description="API to get all the IPAM failed devices"
)
def get_auto_discovery_failed_devices():
    try:
        failed_list = []
        failed_devices = configs.db.query(FailedDevicesTable).filter_by(module="Discovery").all()
        for devices in failed_devices:
            failed_dict = {
                "failure_id":devices.failure_id,
                "ip_address":devices.ip_address,
                "device_type":devices.device_type,
                "date":devices.date,
                "failure_reason":devices.failure_reason,
                "module":devices.module
            }
            failed_list.append(failed_dict)
        return failed_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Auto Discovery failed Devices",status_code=500)


@router.get("/get_ncm_failed_devices",
            responses={
                200:{"model":list[FailedDevicesResponseSchema]},
                500:{"model":str}
            },
summary="API to get all the IPAM failed device",
description="API to get all the IPAM failed devices"
)
def get_ncm_failed_devices():
    try:
        failed_list = []
        failed_devices = configs.db.query(FailedDevicesTable).filter_by(module="NCM").all()
        for devices in failed_devices:
            failed_dict = {
                "failure_id":devices.failure_id,
                "ip_address":devices.ip_address,
                "device_type":devices.device_type,
                "date":devices.date,
                "failure_reason":devices.failure_reason,
                "module":devices.module
            }
            failed_list.append(failed_dict)
        return failed_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting NCM failed Devices",status_code=500)


@router.get("/get_monitoring_failed_devices",
            responses={
                200:{"model":list[FailedDevicesResponseSchema]},
                500:{"model":str}
            },
summary="API to get all the IPAM failed device",
description="API to get all the IPAM failed devices"
)
def get_monitoring_failed_devices():
    try:
        failed_list = []
        failed_devices = configs.db.query(FailedDevicesTable).filter_by(module="Monitoring").all()
        for devices in failed_devices:
            failed_dict = {
                "failure_id":devices.failure_id,
                "ip_address":devices.ip_address,
                "device_type":devices.device_type,
                "date":devices.date,
                "failure_reason":devices.failure_reason,
                "module":devices.module
            }
            failed_list.append(failed_dict)
        return failed_list
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting IPAM failed Devices",status_code=500)



@router.get('/get_failed_devices_count',responses={
    200:{"model":list[FailedDevicesCountResponseSchema]},
    400:{"model":str}
})
def get_failed_devices_count():
    try:
        failed_devices_list = []
        ipam_query = f"SELECT count(*) FROM failed_devices_table WHERE module='IPAM';"
        ipam_result = configs.db.execute(ipam_query).scalar()

        discovery_query = f"SELECT count(*) FROM failed_devices_table WHERE module='Discovery';"
        discovery_result = configs.db.execute(discovery_query).scalar()

        ncm_query = f"SELECT count(*) FROM failed_devices_table WHERE module='NCM';"
        ncm_result = configs.db.execute(ncm_query).scalar()

        monitoring_query = f"SELECT count(*) FROM failed_devices_table WHERE module='Monitoring';"
        monitoring_result = configs.db.execute(monitoring_query).scalar()

        uam_query = f"SELECT count(*) FROM failed_devices_table WHERE module='Monitoring';"
        uam_result = configs.db.execute(uam_query).scalar()

        failed_dict = {
            "auto_discovery_failed_devices":discovery_result,
            "ipam_failed_devices":ipam_result,
            "monitoring_failed_devices":monitoring_result,
            "ncm_failed_devices":ncm_result,
            "uam_failed_devices":uam_result
        }
        failed_devices_list.append(failed_dict)
        return failed_dict

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error while failed devices count",status_code=500)