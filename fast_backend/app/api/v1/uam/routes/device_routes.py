from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schema.uam_device_schema import *
from fastapi import FastAPI, Query

from app.api.v1.uam.utils.uam_utils import *
from app.utils.static_list import *
from app.core.config import *

router = APIRouter(
    prefix="/uam_device",
    tags=["uam_device"],
)


@router.post("/on_board_device", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
})
async def onboard_devices(ip_list: list[str]):
    try:
        success_list = []
        error_list = []
        data = []
        print("ip list is ::::::::::::::::::::::::::::::::::",ip_list,file=sys.stderr)
        for ip in ip_list:

            result = (configs.db.query(AtomTable, PasswordGroupTable).
                      join(PasswordGroupTable, PasswordGroupTable.password_group_id == AtomTable.password_group_id).
                      filter(AtomTable.ip_address == ip).first())

            print("result is:::::::::::::::::::::::::::::::::::::::::::fro onboard devices is",result,file=sys.stderr)
            if result is None:
                error_list.append(f"{ip} : Device or Password Group Not Found")
                continue

            else:
                atom, password_group = result

                atom = atom.as_dict()
                print("atom as dict is:::::::::::::::::::::::::::::::::::::::::::",atom,file=sys.stderr)
                password_group = password_group.as_dict()
                print("password is::::::::::::::::::::::::::::::::::::::::::::::::::::::",password_group,file=sys.stderr)
                atom_password_dict = {**atom, **password_group}
                print("atom password dict is::::::::::::::::::::::::::::::::::::::::",atom_password_dict,file=sys.stderr)
                # data.append(atom_password_dict)
                atom.update(password_group)

                if atom["device_type"] in onboard_dict:
                    try:

                        puller = onboard_dict[atom['device_type']]
                        hosts = [atom]
                        response = puller.get_inventory_data(hosts)
                        print("repsones of the puller is:::::::::::::::::::::::",response,file=sys.stderr)
                        for response in response:
                            ip_address = response.get('ip_address')
                            if response.get('status') == 'error':
                                error_message = response.get('message', 'Login or inventory retrieval failed.')
                                error_list.append(error_message)
                            else:
                                response = onboard_devices_data_fetch(ip)
                                print("resposne of the atom fetch utils function is:::",response,file=sys.stderr)
                                data.append(response)
                                success_list.append(f"{ip_address} : Device Onboarded Successfully")


                    except Exception:
                        traceback.print_exc()
                        error_list.append(f"{ip} : Error While Onboarding")
                else:
                    error_list.append(f"{ip} : Support Not Available For Device Type - {atom['device_type']}")

        response_dict = {
            "data": data,
            'success': len(success_list),
            'error': len(error_list),
            'success_list': success_list,
            'error_list': error_list
        }
        configs.db.close()
        return JSONResponse(content=response_dict, status_code=200)

    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Onboarding", status_code=500)


@router.get("/total_devices_in_device_dashboard", responses={
    200: {"model": TotalDeviceDashboardResponseSchema},
    500: {"model": str}
},
summary = "Use this API in UAM Device page to display the count of devices in Device Status Overview",
description = "Use this API in UAM Device page to display the count of devices in Device Status Overview")
async def total_devices_in_device_dashboard():
    try:
        query_string = f"select count(*) from uam_device_table"
        result = configs.db.execute(query_string).scalar()

        response = {"name": "Total Device Count", "value": result}

        return JSONResponse(content=response, status_code=200)

    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Data", status_code=500)


@router.get("/get_all_devices", responses={
    200: {"model": GetAllUAMDeviceResponseSchema},
    500: {"model": str}
},
summary = "Use this API tin UAM Device table to list down al the devices",
description = "Use this API tin UAM Device table to list down al the devices")
async def get_all_devices():
    try:
        response = get_all_uam_devices_util()
        print("reaponae in get all devices are:::::::::::::::::::::::::::::::::::::::",response,file = sys.stderr)
        return JSONResponse(content=response, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Uam Devices Data", status_code=500)


@router.post("/delete_devices", responses={
    200: {"model": DeleteResponseSchema},
    400: {"model": str},
    500: {"model": str}
})
async def delete_uam_device(ip_list: list[str]):
    try:

        success_list = []
        error_list = []
        data = []
        check = False
        for ip_address in ip_list:
            msg, status = delete_uam_device_util(ip_address)
            print("status is::::::::::::::::::::::::::::::",status,file=sys.stderr)
            print("message in delte uam is:::::::::::::::::::::::",msg,file=sys.stderr)
            if status == 400 or status == 500:
                check = False
                error_list.append(msg)
            elif status == 200:
                if isinstance(msg, dict):
                    for key,value in msg.items():
                        if key == "data":
                            data.append(value)
                        if key == "message":
                            success_list.append(value)
                    check =True
                else:
                    error_list.append(msg)

        
        
        response = {
            "data":data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }
        return JSONResponse(content=response, status_code=status)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Deleting Uam Devices", status_code=500)


@router.post("/edit_device", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
})
async def edit_uam_device(device_obj: EditUamDeviceRequestSchema):
    try:
        data = []
        success_list = []
        error_list = []

        # Getting the response from the edit_uam_device_util function
        response, status_code = edit_uam_device_util(device_obj, device_obj['uam_id'])
        print("response is::::::::::::::::::::::::::::::::::::::::", response, file=sys.stderr)
        print("status_code is::::::::::::::::::::::::::::::::::::::::", status_code, file=sys.stderr)

        # Checking the status code to determine success or error
        if status_code == 200:
            # If status code is 200, the operation was successful
            for key, value in response.items():
                if key == "attributes_dict":  # Assuming this is where your data is stored
                    data.append(value)
                if key == "message":
                    success_list.append(value)
        else:
            # If status code is different than 200, it indicates an error
            error_list.append(response)

        # Creating the response to be sent back
        respons = {
            "data": data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        # Returning the response as a JSONResponse
        return JSONResponse(content=respons)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Updating Uam Device", status_code=500)


@router.post("/device_status", responses={
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


@router.post("/top_functions", responses={
    200: {"model": dict},
    500: {"model": str}
},
summary = "use this api in the UAM Devices page to diaplay the  devices function count bar chart ",
description = "use this api in the UAM Devices page to diaplay the  devices function count bar chart "

)

async def top_functions():
    try:
        obj_list = []
        query_string = "select `FUNCTION`,count(`FUNCTION`) from uam_device_table\
         join atom_table on uam_device_table.atom_id = atom_table.atom_id \
         where `FUNCTION`!='' group by `FUNCTION`;"

        result = configs.db.execute(query_string)

        for row in result:
            obj_dict = {}
            function = row[0]
            count = row[1]
            obj_dict[function] = count
            obj_list.append(obj_dict)

        response = {}
        for i in obj_list:
            for j in i:
                response[j] = i[j]

        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Uam Data", status_code=500)


@router.get("/get_site_detail_by_ip_address", responses={
    200: {"model": GetSiteByIpResponseSchema},
    500: {"model": str}
},
summary = "Use this API in UAM device page when click on ip to ge the  site information of that IP address",
description = "Use this API in UAM device page when click on ip to ge the  site information of that IP address"
)
async def get_site_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:
        site_list = []
        result = (
            configs.db.query(AtomTable, RackTable, SiteTable)
            .join(RackTable, AtomTable.rack_id == RackTable.rack_id)
            .join(SiteTable, RackTable.site_id == SiteTable.site_id)
            .filter(AtomTable.ip_address == ip_address)
            .first()
        )

        if result is None:
            return "No Site Found", 500

        atom, rack, site = result
        site_data_dict = {"site_name": site.site_name, "region": site.region_name, "latitude": site.latitude,
                          "longitude": site.longitude, "city": site.city, "creation_date": str(site.creation_date),
                          "modification_date": str(site.modification_date), "status": site.status}
        site_list.append(site_data_dict)
        return JSONResponse(content=site_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Site Data", status_code=500)


@router.get("/get_rack_detail_by_ip_address", responses={
    200: {"model": GetRackByIpResponseSchema},
    500: {"model": str}
},
summary = "use this API In UAM device page to get the detail of the Rack based on Ip click",
description = "use this API In UAM device page to get the detail of the Rack based on Ip click"
)

async def get_rack_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:
        obj_list = []
        rack_list =[]
        result = (
            configs.db.query(AtomTable, RackTable, SiteTable)
            .join(RackTable, AtomTable.rack_id == RackTable.rack_id)
            .join(SiteTable, RackTable.site_id == SiteTable.site_id)
            .filter(AtomTable.ip_address == ip_address)
            .first()
        )

        if result is None:
            return "No Rack Found", 500

        atom, rack, site = result
        rack_data_dict = {"rack_name": rack.rack_name, "site_name": site.site_name,
                          "serial_number": rack.serial_number,
                          "manufacturer_date": str(rack.manufacture_date),
                          "unit_position": rack.unit_position, "creation_date": str(rack.creation_date),
                          "modification_date": str(rack.modification_date), "status": rack.status,
                          "rfs_date": str(rack.rfs_date), "height": rack.height, "width": rack.width,
                          "depth": rack.depth, "ru": rack.ru, "pn_code": rack.pn_code,
                          "rack_model": rack.rack_model, "floor": rack.floor}
        rack_list.append(rack_data_dict)
        return JSONResponse(content=rack_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Rack Data", status_code=500)


@router.get("/get_device_details_by_ip_address", responses={
    200: {"model": GetAllUAMDeviceResponseSchema},
    500: {"model": str}
},
summary = "USe this API in UAM device page to get the detail of device based on the click of ip address",
description ="USe this API in UAM device page to get the detail of device based on the click of ip address" )
async def get_device_details_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:
        result = (
            configs.db.query(UamDeviceTable, AtomTable, RackTable, SiteTable)
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .join(RackTable, AtomTable.rack_id == RackTable.rack_id)
            .join(SiteTable, RackTable.site_id == SiteTable.site_id)
            .filter(AtomTable.ip_address == ip_address)
            .first()
        )

        if result is None:
            return "No Rack Found", 500

        uam, atom, rack, site = result

        obj_dict = {"device_name": atom.device_name, "site_name": site.site_name, "rack_name": rack.rack_name,
                    "ip_address": atom.ip_address, "software_type": uam.software_type,
                    "software_version": uam.software_version, "patch_version": uam.patch_version,
                    "creation_date": str(uam.creation_date), "modification_date": str(uam.modification_date),
                    "status": uam.status, "ru": atom.device_ru, "department": atom.department, "section": atom.section,
                    "function": atom.function, "manufacturer": uam.manufacturer,
                    "hw_eos_date": str(uam.hw_eos_date), "hw_eol_date": str(uam.hw_eol_date),
                    "sw_eos_date": str(uam.sw_eos_date), "sw_eol_date": str(uam.sw_eol_date),
                    "virtual": atom.virtual, "authentication": uam.authentication, "serial_number": uam.serial_number,
                    "pn_code": uam.pn_code, "manufacturer_date": str(uam.manufacture_date),
                    "hardware_version": uam.hardware_version, "source": uam.source, "stack": uam.stack,
                    "contract_number": uam.contract_number, "contract_expiry": str(uam.contract_expiry)}

        return JSONResponse(content=obj_dict, status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred Fetching Device Data", status_code=500)


@router.post("/dismantle_onboard_device", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
},
summary = "Use this API on the UAM device page to dismantel the Device bansed on list of ip address"
)
async def dismantle_onboard_device(device_ips: list[str]):
    try:
        data = []
        error_list = []
        success_list = []

        for ip in device_ips:
            print("ip in desvice type is:::::::::::::::::::::::",ip,file=sys.stderr)
            try:
                ip_address = None
                uam_exsits = configs.db.query(UamDeviceTable).filter_by(uam_id = ip).first()
                if uam_exsits:
                    atom_exsist = configs.db.query(AtomTable).filter_by(atom_id = uam_exsits.atom_id).first()
                    if atom_exsist:
                        ip_address = atom_exsist.ip_address
                response, status = update_uam_status_utils(ip_address, "Dismantled")
                print("repsonse for the dismanteled onboard device is :::::::::::::::::::::::::::::::::::::::::",response,file=sys.stderr)
                print(response, status, file=sys.stderr)

                if status == 400:
                    error_list.append(response)
                else:
                    for key,value in response.items():
                        print("key in dismantel onboard devices is::::::::::::::::::::::::::",key,file=sys.stderr)
                        print("value is::::::::::::::::::::::::::::::::::",value,file=sys.stderr)
                        if key == "data":
                            data.append(value)
                        elif key == "message":
                            success_list.append(value)

            except Exception:
                traceback.print_exc()
                error_list.append(f"{ip} : Error Occurred While Dismantling")

        response_dict = {
            "data":data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        return JSONResponse(content=response_dict, status_code=200)
    except Exception as e:
        traceback.print_exc()
        return "Error While Updating Status", 500


@router.post("/add_device_statically", responses={
    200: {"model": str},
    500: {"model": str}
})
async def add_device_statically(device_obj: EditUamDeviceRequestSchema):
    try:

        device_obj['status'] = "Dismantled"
        response, status = edit_uam_device_util(device_obj, None)

        if status == 200:
            return "Device Onboarded Statically", 200

        return response, status
    except Exception as e:
        traceback.print_exc()
        return "Error While Adding Device Statically", 500
