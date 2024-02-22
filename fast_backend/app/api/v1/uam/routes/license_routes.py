import traceback
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query
from app.core.config import configs

from app.models.atom_models import *
from app.models.uam_models import *
from app.schema.uam_license_schema import *

router = APIRouter(
    prefix="/uam_license",
    tags=["uam_license"],
)


#getLicenseDetailsByIpAddress
@router.get("/get_liscence_detail_by_ip_address", responses={
    200: {"model": list[GetLicenseResponseSchema]},
    400: {"model": str},
    500: {"model": str}
},
summary = "Use this API within the UAM Module on devices to retrieve detailed Liscence information upon clicking the IP address.",
description = "Use this API within the UAM Module on devices to retrieve detailed Liscence information upon clicking the IP address.")
async def get_license_details_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:

        atom = configs.db.query(AtomTable).filter(AtomTable.ip_address == ip_address).first()
        if atom is None:
            return JSONResponse(content="no device found in atom with the given ip address", status_code=400)

        uam = configs.db.query(UamDeviceTable).filter(UamDeviceTable.atom_id == atom.atom_id).first()
        if uam is None:
            return JSONResponse(content="no device found in uam with the given ip address", status_code=400)

        results = configs.db.query(LicenseTable).filter(LicenseTable.uam_id == uam.uam_id).all()

        obj_list = []
        for license_obj in results:
            license_data_dict = {'license_id': license_obj.license_id, 'uam_id': license_obj.uam_id,
                                 "device_name": atom.device_name, "license_name": license_obj.license_name,
                                 "status": license_obj.status, "license_description": license_obj.license_description,
                                 'rfs_date': str(license_obj.rfs_date),
                                 "activation_date": str(license_obj.activation_date),
                                 "expiry_date": str(license_obj.expiry_date), 'grace_period': license_obj.grace_period,
                                 'serial_number': license_obj.serial_number, 'capacity': license_obj.capacity,
                                 'usage': license_obj.usage, "pn_code": license_obj.pn_code,
                                 "creation_date": str(license_obj.creation_date),
                                 "modification_date": str(license_obj.modification_date)}

            obj_list.append(license_obj)

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error While Fetching License Data", status_code=500)


#
#getAllLicenses

@router.get("/get_all_licenses", responses={
    200: {"model": list[GetLicenseResponseSchema]},
    500: {"model": str}
},
summary = "Use this API in UAM Liscence modeult to list down all the liscence information in table",
description  = "Use this API in UAM Liscence modeult to list down all the liscence information in table"
)
async def get_all_licenses():
    try:
        license_list = []
        results = (
            configs.db.query(LicenseTable, UamDeviceTable, AtomTable)
            .join(UamDeviceTable, LicenseTable.uam_id == UamDeviceTable.uam_id)
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .all()
        )

        for license_obj, uam, atom in results:
            license_data_dict = {'license_id': license_obj.license_id, 'uam_id': license_obj.uam_id,
                                 "device_name": atom.device_name, "license_name": license_obj.license_name,
                                 "status": license_obj.status, "license_description": license_obj.license_description,
                                 'rfs_date': str(license_obj.rfs_date),
                                 "activation_date": str(license_obj.activation_date),
                                 "expiry_date": str(license_obj.expiry_date), 'grace_period': license_obj.grace_period,
                                 'serial_number': license_obj.serial_number, 'capacity': license_obj.capacity,
                                 'usage': license_obj.usage, "pn_code": license_obj.pn_code,
                                 "creation_date": str(license_obj.creation_date),
                                 "modification_date": str(license_obj.modification_date)}

            license_list.append(license_data_dict)

        return JSONResponse(content=license_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error While Fetching License Data", status_code=500)
#
#
# @app.route("/editLicenses", methods = ['POST'])
# def EditLicenses():
#     if True:
#         licensesObj = request.get_json()
#         print(licensesObj,file = sys.stderr)
#         licenses = LicenseTable.query.with_entities(LicenseTable).filter_by(license_name=licensesObj["license_name"]).first()

#         licenses.item_code = licensesObj['item_code']
#         licenses.item_desc = licensesObj['item_desc']
#         licenses.ciei = licensesObj['ciei']
#         licenses.modification_date= datetime.now()
#         UpdateData(licenses)

#         return jsonify({'response': "success","code":"200"})

#     else:
#         print("Service not Available",file=sys.stderr)
#         return jsonify({"Response":"Service not Available"}),503
#
