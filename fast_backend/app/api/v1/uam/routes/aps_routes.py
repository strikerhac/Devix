import traceback
from app.schema.uam_aps_schema import GetApsSchema
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import configs

from app.models.uam_models import *

router = APIRouter(
    prefix="/uam_aps",
    tags=["uam_aps"],
)


@router.get("/get_all_aps", responses={
    200: {"model": list[GetApsSchema]},
    500: {"model": str}
},
summary = "Use this API within UAM modeule in APS page to display all APS in Table",
description = "Use this API within UAM modeule in APS page to display all APS in Table"
)
async def get_all_aps():
    try:
        ap_objs = configs.db.query(ApsTable).all()

        obj_list = []
        for ap_obj in ap_objs:
            obj_dict = {"ap_id": ap_obj.ap_id, "uam_id": ap_obj.uam_id, "controller_name": ap_obj.controller_name,
                        "ap_ip": ap_obj.ap_ip, "ap_name": ap_obj.ap_name, "serial_number": ap_obj.serial_number,
                        "ap_model": ap_obj.ap_model, "hardware_version": ap_obj.hardware_version,
                        "software_version": ap_obj.software_version, "description": ap_obj.description,
                        "creation_date": ap_obj.creation_date, "modification_date": ap_obj.modification_date}
            obj_list.append(obj_dict)

        # print(obj_list, file=sys.stderr)
        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Access Point Data", status_code=500)
