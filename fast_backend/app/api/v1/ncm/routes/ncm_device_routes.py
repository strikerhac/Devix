import os
import threading
import traceback
from pathlib import Path
from sqlalchemy import func

from fastapi import Request
from fastapi.responses import HTMLResponse
# from app.core.config import configs
from starlette.templating import Jinja2Templates
from app.api.v1.ncm.conf_diff_main.conf_diff import ConfDiff
from app.api.v1.ncm.ncm_pullers.ncm_puller import NCMPuller
from app.api.v1.ncm.ncm_pullers.ncm_restore import RestorePuller
from app.api.v1.ncm.utils.ncm_utils import *
from app.schema.ncm_schema import *
# from app.core.config import *
router = APIRouter(
    prefix="/ncm_device",
    tags=["ncm_device"],
)






@router.post("/add_ncm_device", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def add_ncm_device(ncm_obj: AddNcmRequestSchema):
    try:
        msg, status = add_ncm_device_util(ncm_obj, False)
        return JSONResponse(content=msg, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Adding NCM Device", status_code=500)


@router.post("/add_ncm_devices", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
},
summary="Use this API to add multiple devices",
description="Use this API to add multiple devices"
)
async def add_ncm_devices(ncm_objs: list[AddNcmRequestSchema]):
    try:
        data = []
        success_list = []
        error_list = []

        row = 0
        for ncm_obj in ncm_objs:
            try:
                row += 1

                ncm_obj["ip_address"] = ncm_obj["ip_address"].strip()
                if ncm_obj["ip_address"] == "":
                    error_list.append(f"Row {row} : IP Address Can Not Be Empty")
                    continue

                atom = configs.db.query(AtomTable).filter(
                    AtomTable.ip_address == ncm_obj["ip_address"]).first()

                if atom is not None:
                    msg, status = add_complete_atom(ncm_obj, True)
                    print("msg is:::::::::::::::::::::::",msg,file=sys.stderr)
                    print("if atom is not none::::",status,file=sys.stderr)
                    if isinstance(msg,dict):
                        for key,value in msg.items():
                            print("key is::::::::::::::::::::::",key,file=sys.stderr)
                            print("msg is::::::::::::::::::::::",msg,file=sys.stderr)
                            if key == 'data':
                                data.append(value)
                            elif key == 'message':
                                success_list.append(value)
                else:
                    msg, status = add_ncm_device_util(ncm_obj, False)
                    print("ncm is:::::::::",msg,file=sys.stderr)
                    print("ncm status is:::::::::::::::::",status,file=sys.stderr)
                    if isinstance(msg,dict):
                        for key,value in msg.items():
                            print("key is::::::::::::::::::::::",key,file=sys.stderr)
                            print("msg is::::::::::::::::::::::",msg,file=sys.stderr)
                            if key == 'data':
                                data.append(value)
                            elif key == 'message':
                                success_list.append(value)
            except Exception:
                traceback.print_exc()
                status = 500
                msg = f"{ncm_obj['ip_address']} : Exception Occurred"

            if status == 500 or status ==400:
                error_list.append(msg)
            else:
                success_list.append(msg)

        response_dict = {
            "data":data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        return JSONResponse(content=response_dict, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Adding/Updating NCM Devices",
                            status_code=500)


@router.post("/edit_ncm_device", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
},
summary="Use this API to edit the NCM device",
description="Use this API to edit the NCM devic"
)
async def edit_ncm_device(ncm_obj: AddNcmRequestSchema):
    try:
        msg, status = edit_ncm_device_util(ncm_obj)
        return JSONResponse(content=msg, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Adding NCM Device", status_code=500)


@router.get("/get_all_ncm_devices", responses={
    200: {"model": list[GetAllNcmResponseSchema]},
    500: {"model": str}

},
summary="Use this API to list down all the ncm devices",
description="Use this API to list down all the ncm devices"
)
async def get_all_ncm_devices():
    try:
        ncm_list = []
        results = (
            configs.db.query(NcmDeviceTable, AtomTable)
            .join(AtomTable, AtomTable.atom_id == NcmDeviceTable.atom_id)
            .all()
        )

        for ncm, atom in results:
            password = configs.db.query(PasswordGroupTable).filter(
                PasswordGroupTable.password_group_id == atom.password_group_id
            ).first()

            ncm_dict = {"ncm_device_id": ncm.ncm_device_id, "atom_id": ncm.atom_id,
                        "ip_address": atom.ip_address, "device_name": atom.device_name,
                        "device_type": atom.device_type, "function": atom.function,
                        "vendor": atom.vendor, "status": ncm.status,
                        "backup_status": ncm.backup_status,
                        "password_group": password.password_group,
                        "modification_date": ncm.modification_date,
                        "creation_date": ncm.creation_date}

            ncm_list.append(ncm_dict)
        return ncm_list

    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching NCM Devices", status_code=500)


@router.get("/get_atom_in_ncm", responses={
    200: {"model": list[GetAtomInNcmResponseSchema]},
    500: {"model": str}

},
summary="Use this API to list down the ATOM in NCM",
description="Use this API to list down the Atom in NCM"
)
async def get_atom_in_ncm():
    try:
        atom_ids = []
        ncm_devices = configs.db.query(NcmDeviceTable).all()
        for ncm in ncm_devices:
            atom_ids.append(ncm.atom_id)

        results = configs.db.query(AtomTable).all()

        atom_list = []
        for atom in results:
            if atom.atom_id in atom_ids:
                continue

            password_group = None
            if atom.password_group_id is not None:
                password = configs.db.query(PasswordGroupTable).filter(
                    PasswordGroupTable.password_group_id == atom.password_group_id
                ).first()

                if password is not None:
                    password_group = password.password_group

            obj_dict = {"atom_id": atom.atom_id, "ip_address": atom.ip_address,
                        "device_name": atom.device_name, "device_type": atom.device_type,
                        "password_group": password_group, "vendor": atom.vendor,
                        "function": atom.function}
            atom_list.append(obj_dict)

        return JSONResponse(content=atom_list, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Atom In NCM", status_code=500)


@router.post("/add_ncm_from_atom", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
},
summary="use this API to add the NCM from the atom",
description="Use this API to add the NCM from the atom"
)
async def add_ncm_from_atom(atom_ids: list[int]):
    try:
        data =[]
        success_list = []
        error_list = []
        password_group_attribute = ""
        for atom_id in atom_ids:
            print("atom id is:::::::::::::::::",atom_id,file=sys.stderr)
            atom = configs.db.query(AtomTable).filter(AtomTable.atom_id == atom_id).first()
            if atom is not None:
                print("atom is not none::::::::::::",atom,file=sys.stderr)
                queried_password_group = configs.db.query(PasswordGroupTable).filter(
                    PasswordGroupTable.password_group_id == atom.password_group_id).first()
                if queried_password_group is not None:
                    password_group_attribute = queried_password_group.password_group
                ncm = NcmDeviceTable()
                ncm.atom_id = atom.atom_id
                ncm.status = "Active"

                if InsertDBData(ncm) == 200:
                    data_dict = {
                        # "atom_id":atom.atom_id,
                        "ip_address":atom.ip_address,
                        "device_name":atom.device_name,
                        "vendor":atom.vendor,
                        "device_type":atom.device_type,
                        "function":atom.function,
                        "ncm_device_id":ncm.ncm_device_id,
                        "status":ncm.status,
                        "config_change_date":ncm.config_change_date,
                        "backup_status":ncm.backup_status,
                        "password_group":password_group_attribute
                    }
                    print("data dict is::::::::::::::",data_dict,file=sys.stderr)
                    data.append(data_dict)
                    success_list.append(f"{atom.ip_address} : Device Added Successfully")
                else:
                    error_list.append(
                        f"{atom.ip_address} : Exception Occurred While Insertion"
                    )

            else:
                error_list.append(f"{atom_id} : Atom Not Found")

        response_dict = {
            "data":data,
            "success": len(success_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": success_list,
        }

        return JSONResponse(content=response_dict, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Importing Atom In NCM", status_code=500)


@router.post("/delete_ncm_devices", responses={
            200:{"model":DeleteResponseSchema},
            400:{"model":str},
            500:{"model":str}
},
summary="Use this API to delete the ncm devices by ncm-device_id",
             description="Use this API to delete the ncm devices by ncm-device_id"
)
async def delete_ncm_device(ncm_ids: list[int]):
    try:
        data = []
        error_list = []
        response_list = []
        for ncm_id in ncm_ids:
            ncm = configs.db.query(NcmDeviceTable).filter(
                NcmDeviceTable.ncm_device_id == ncm_id).first()
            data.append(ncm_id)
            print("ncm is:::::::::::::::::::",ncm,file=sys.stderr)
            if ncm is None:
                error_list.append(f"{ncm_id} : No NCM Device Found")
            elif DeleteDBData(ncm):
                response_list.append(f"{ncm_id} : Device Deleted Successfully")
            else:
                error_list.append(f"{ncm_id} : Error While Deleting Device")

        response_dict = {
            "data":data,
            "success": len(response_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": response_list,
        }

        return JSONResponse(content=response_dict, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Deleting NCM Devices", status_code=500)


@router.post("/get_all_device_configurations_by_id", responses={
    200: {"model": list[NcmConfigHistorySchema]},
    500: {"model": str}
},
summary = "Use this API in the NCM modeule to list down all the configurations based on ip_address click by sending ncm_device_id in a payload",
description="Use this API in the NCM modeule to list down all the configurations based on ip_address click by sending ncm_device_id in a payload"
)
async def get_all_configuration(ncm_device_id: GetDeviceConfigurationById):
    try:

        results = configs.db.query(NCM_History_Table).filter(
            NCM_History_Table.ncm_device_id == ncm_device_id['ncm_device_id']
        ).all()

        obj_list = []
        for history in results:
            if history.deleted_state !=True:
                obj_dict = {"ncm_history_id": history.ncm_history_id,
                            "date": history.configuration_date,
                            "file_name": history.file_name}

                obj_list.append(obj_dict)

        return obj_list
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Backup History", status_code=500)


def check_path(file_path):
    from pathlib import Path

    # create a Path object with the path to the file
    path = Path(file_path)

    return path.is_file()



@router.post("/get_device_configuration", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
},
summary="Use this API to get the display the output of configuration based on ncm_history_id",
description="Use this API to get the display the output of configuration based on ncm_history_id"
)
async def get_device_configuration(ncm_history_id:GetDeviceConfigurationByHistory):
    try:
        data = {}
        history = configs.db.query(NCM_History_Table).filter(
            NCM_History_Table.ncm_history_id == ncm_history_id['ncm_history_id']
        ).first()
        print("history is::::::::::::::",history,file=sys.stderr)
        if history is None:
            return JSONResponse(content="Backup Not Found", status_code=400)

        cwd = os.getcwd()
        file_path = cwd + "/app/configuration_backups/" + history.file_name
        print("file path is::::::::::::::",file_path,file=sys.stderr)
        pathFlag = check_path(file_path)
        print("Path flag is:::::::::::::",pathFlag,file=sys.stderr)

        if pathFlag:
            f = open(file_path, "r")
            print("f file is:::::::::",file=sys.stderr)
            configuration = f.read()
            print("configuration is:::::::::::",configuration,file=sys.stderr)
            data['data'] = configuration
            data['message'] = f"{history.file_name} : Retrieved Successfully"
            return JSONResponse(content=data, status_code=200)
        else:
            DeleteDBData(history)
            return JSONResponse(content="Configuration File Does Not Exist", status_code=400)

    except Exception:
        traceback.print_exc()
        return "Server Error While Fetching Backup", 500


@router.post("/send_command", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
},
summary="Use this API in the NCM moodeul table to send the command and to display its output",
description="Use this API in the NCM moodeul table to send the command and to display its output"
)
async def send_command(ncm_obj: SendCommandRequestSchema):
    try:
        data = {}
        ncmPuller = NCMPuller()
        print("ncm puller is::::::::::::::::::",ncmPuller,file=sys.stderr)
        ncmPuller.setup_puller(ncm_obj)

        if ncmPuller.status != 200:
            return JSONResponse(content=ncmPuller.response, status_code=ncmPuller.status)

        ncm_obj["cmd"] = str(ncm_obj["cmd"]).strip()
        if ncm_obj["cmd"] == "":
            return JSONResponse(content="Command Is Empty", status_code=400)

        ncmPuller.send_remote_command(ncm_obj["cmd"])
        data['data'] = ncmPuller.response
        data['message'] = f"{ncm_obj['cmd']} : Executed Successfully"
        return JSONResponse(content=data, status_code=ncmPuller.status)

    except Exception as e:
        print(str(e), file=sys.stderr)
        traceback.print_exc()
        return JSONResponse(content="Server Error While Sending Remote Command", status_code=500)


@router.post("/get_configuration_backup", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
},
summary="Use this API to get the configuration based on the ncm_device_id",
description="Use this API to get the configuration based on the ncm_device_id"
)
async def get_configuration_backup(ncm_obj: NcmDeviceId):
    try:

        ncmPuller = NCMPuller()
        ncm_device = configs.db.query(NcmDeviceTable).filter_by()
        print("ncm puller is::::::::::::::",ncmPuller,file=sys.stderr)
        print("ncm obj is:::",ncm_obj,file=sys.stderr)
        ncmPuller.setup_puller(ncm_obj)
        print("ncm pulerr obj is::::::::::::::::",ncmPuller.setup_puller(ncm_obj),file=sys.stderr)

        if ncmPuller.status != 200:
            return JSONResponse(content=ncmPuller.response, status_code=ncmPuller.status)

        ncmPuller.backup_config()
        data = {
            'data':ncmPuller.response,
            'message':f"Configuration Backup Is Successfull"
        }
        print("NCM puller resposne is::::::::::",ncmPuller.response)
        # data['data'] = ncmPuller.response

        # data['message'] = f"Configuration Backup Is Successfull"
        return data

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error In Configuration Backup", status_code=500)



@router.post("/configuration_comparison", response_class=HTMLResponse, responses={
    400: {"model": str},
    500: {"model": str}
},
summary="use this API to compare the configuration based on ncm_history_ids",
description="use this API to compare the configuration based on ncm_history_ids"
)
async def configuration_comparison(ncm_obj: CompareBackupSchema, request: Request):
    try:
        print("reqeust in coonfiguration compariosn is:::::",request,file=sys.stderr)
        history1 = configs.db.query(NCM_History_Table).filter(
            NCM_History_Table.ncm_history_id == ncm_obj["ncm_history_id_1"],
        ).first()
        print("history 1 is:::::::::::::::::::::::::",history1,file=sys.stderr)
        history2 = configs.db.query(NCM_History_Table).filter(
            NCM_History_Table.ncm_history_id == ncm_obj["ncm_history_id_2"],
        ).first()
        print("history2 is::::::::::::::::::",history2,file=sys.stderr)
        if history1 is None or history2 is None:
            return JSONResponse(content="One of the Configurations Not Found",status_code=400)

        if history1.ncm_history_id == history2.ncm_history_id:
            return JSONResponse(content = "Can not compare same configurations",status_code= 400)

        cwd = os.getcwd()
        existingPath = f"{cwd}/app/templates/html_diff_output.html"
        print("exsisting path is::::::::::::",existingPath,file=sys.stderr)
        existingPath1 = os.path.exists(existingPath)
        print("exisisting path1 is::::::::::",existingPath1,file=sys.stderr)
        if existingPath1:
            print("Existing File Removed", file=sys.stderr)
            os.remove(existingPath)
        else:
            pass

        cwd = os.getcwd()

        path = f"{cwd}/app/configuration_backups/"
        file_1 = Path(f"{path}{history1.file_name}")
        print("file_1 is:::::::::",file_1,file=sys.stderr)
        file_2 = Path(f"{path}{history2.file_name}")
        print("file2 is:::::::::::::::",file_2,file=sys.stderr)
        html_file = Path(f"{cwd}/app/templates/html_diff_output.html")
        print("html file is::::::::::::",html_file,file=sys.stderr)
        html_diff = ConfDiff(file_1, file_2, html_file)
        print("html diff is:::::::::::",html_diff,file=sys.stderr)
        difference = html_diff.diff()
        print("html differnece iss:::",difference,file=sys.stderr)
        template = Jinja2Templates(directory=f"{cwd}/app/templates")
        print("templates in config file is:", template, file=sys.stderr)
        if difference is None:
            return JSONResponse(content="No Difference Found In Configurations", status_code=500)
        context = {
            "request":request
        }

        return template.TemplateResponse("html_diff_output.html", context, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Config Comparison", status_code=500)


@router.post('/bulk_backup_configuration',
             responses={
                 200: {"model": SummeryResponseSchema},
                 400: {"model": str},
                 500: {"model": str}
             },
             summary="API to get bulk backup by list of ncm_device_id",
             description='API to get bulk backup list of ncm_device_id'
             )
def get_bulk_backup_configurration(ncm_device_id: list[int]):
    try:
        configuration_status = {
            1:"Completed",
            0:"Failed",
            3:"In Progress",
            4:"Pending"
        }
        data = []
        errorList = []
        successList = []
        configuration = NcmDeviceTable()
        for id in ncm_device_id:
            device = configs.db.query(NcmDeviceTable).filter_by(ncm_device_id = id).first()
            device.configuration_status = configuration_status[3]
            device.backup_state = 'True'
            print("id in ncm devices is::::::::::::",id,file=sys.stderr)
            ncm = {"ncm_device_id": id}
            print("ncm is ::::::::::::::::::;",ncm,file=sys.stderr)
            ncm_puller = NCMPuller()  # Assuming NCMPuller is properly defined
            print("ncm puller is::::::::::::::::",ncm_puller,file=sys.stderr)
            ncm_puller.setup_puller(ncm)


            if ncm_puller.status == 500 or ncm_puller.status == 400:
                errorList.append(ncm_puller.response)
                device.configuration_status = configuration_status[0]
                device.backup_state = 'True'
                UpdateDBData(device)
                continue

            ncm_puller.backup_config()
            print("ncm puller is:::::::::::::",ncm_puller.backup_config(),file=sys.stderr)
            if ncm_puller.status == 200:
                print("ncm puller response is 200:::::",ncm_puller.response,file=sys.stderr)
                data.append(id)
                message = f"{id} :"+f"{ncm_puller.response}"
                successList.append(message)
                device.configuration_status =configuration_status[1]
                device.backup_state = 'True'
            else:
                device.backup_state = 'True'
                device.configuration_status = configuration_status[0]
                print("ncm puller response is::::::::::::",ncm_puller.response,file=sys.stderr)
                errorList.append(f"{id} : Backup Not Successful due to {ncm_puller.response}")
            UpdateDBData(device)
        responses = {
            "data": data,
            "success": len(successList),
            "error": len(errorList),
            "success_list": successList,
            "error_list": errorList
        }
        return responses  # No need for JSONResponse, FastAPI handles JSON serialization

    except Exception as e:
        # Handle exceptions appropriately, maybe log the error for debugging
        raise JSONResponse(status_code=500, content="Error Occurred While Getting Bulk Backup")




@router.get('/get_all_true_backup',
            responses={
                200:{"model":list[GetTrueBackup]},
                500:{"model":str}
            },
summary="API to use in the manage configuration to get the backup on the bulk bulk backup button",
description="API to use in the manage configuration to get the backup on the bulk bulk backup button"
)
def get_true_backup():
    try:
        backups_list = []
        backups = configs.db.query(NcmDeviceTable).filter_by(backup_state='True').all()
        print("backups are :::::::::::::::::::::::::", backups, file=sys.stderr)

        for backup in backups:
            if backup:
                atom_exist = configs.db.query(AtomTable).filter_by(atom_id=backup.atom_id).first()
                backup_dict = {
                    "ncm_device_id": backup.ncm_device_id,
                    "status": backup.status,
                    "config_change_date": backup.config_change_date,
                    "ip_address": atom_exist.ip_address
                }
                backups_list.append(backup_dict)
                backup.backup_state = 'False'
                configs.db.merge(backup)
                configs.db.commit()
                print("backup state set to false ::::::::::::::", file=sys.stderr)

        # Move the return statement outside the loop
        return backups_list

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Getting the true backup", status_code=500)

@router.post('/delete_configuration',
             responses={
                 200:{"model":DeleteResponseSchema},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="API to delete configuration",
            description="API to delete configuration"

             )
def delete_configuration(ncm_history_id:list[int]):
    try:
        deleted_ids = []
        success_list = []
        error_list = []
        for id in ncm_history_id:
            ncm_history = configs.db.query(NCM_History_Table).filter_by(ncm_history_id = id).first()
            if ncm_history:
                ncm_history.deleted_state = True
                configs.db.merge(ncm_history)
                configs.db.commit()
                deleted_ids.append(id)
                success_list.append(f"{ncm_history_id} has been deleted")
            else:
                error_list.append(f"{ncm_history_id} : Not Found")
        responses = {
            "data":deleted_ids,
            "success_list":success_list,
            "error_list":error_list,
            "success":len(success_list),
            "error":len(error_list)
        }
        return responses
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Deleting the configuration",status_code=500)


@router.post('/get_configuration_to_restore',
            responses={
                200: {"model": list[NcmConfigHistorySchema]},
                500: {"model": str}
            },
            summary="API to Get the deleted configurations",
            description="API to get the deleted configurations"
            )
def get_deleted_configuration(ncm_device_id: NcmDeletedConfigurationSchema):
    try:
        ncm_dev = ncm_device_id.ncm_device_id
        print("ncm dev is::::::", ncm_dev, file=sys.stderr)

        # Only fetch necessary fields
        configurations = configs.db.query(
            NCM_History_Table.ncm_history_id,
            NCM_History_Table.configuration_date,
            NCM_History_Table.file_name)\
            .filter_by(ncm_device_id=ncm_dev, deleted_state=True)\
            .all()

        config_list = [
            {"ncm_history_id": cfg.ncm_history_id, "date": cfg.configuration_date, "file_name": cfg.file_name}
            for cfg in configurations
        ]

        return config_list
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occurred while Getting the configuration")
@router.post('/restore_configuration',
             responses={
                 200:{"model":SummeryResponseSchema},
                 400:{"model":str},
                 500:{"model":str}
             })
def restore_configuration(ncm_history_id:list[int]):
    try:
        config_list =[]
        success_list = []
        error_list = []
        for id in ncm_history_id:
            ncm_history =configs.db.query(NCM_History_Table).filter_by(ncm_history_id = id).first()
            if ncm_history.deleted_state == True:
                connfig_data = {}
                ncm_history.deleted_state = False
                configs.db.merge(ncm_history)
                configs.db.commit()
                connfig_data['ncm_history_id'] =ncm_history.ncm_history_id
                connfig_data['date'] = ncm_history.configuration_date
                connfig_data['file_name'] = ncm_history.file_name
                config_list.append(connfig_data)
                success_list.append(f"{ncm_history.configuration_date} : has been restored")
            else:
                error_list.append(f"{id} : Not Found ")
        response = {
                    "data":config_list,
                    "success_list": success_list,
                    "error_list":error_list,
                    "success": len(success_list),
                    "error": len(error_list)
                    }
        return  response
    except Exception as e:
        traceback.print_exc()






@router.get('/sort_by_severity',
             responses={
                 200:{"model":list[SortSeverity]},
                 500:{"model":str}
             },summary= "Api to get completd and failed devices counting",
             description ="Api to  get completd and failed devices counting"
             )
def sort_severity():
    try:
        obj_list =[]
        total_count = (
                        configs.db.query(func.count())
                        .filter(NcmDeviceTable.configuration_status.isnot(None))
                        .scalar()
                        )
        if not total_count:
            total_count=0
        
        completed_count = (
                        configs.db.query(func.count())
                        .filter(NcmDeviceTable.configuration_status=='completed')
                        .scalar()
                        )
        if not completed_count:
            completed_count=0


        failed_count = (
                        configs.db.query(func.count())
                        .filter(NcmDeviceTable.configuration_status=='failed')
                        .scalar()
                        )
        if not failed_count:
            failed_count=0

        obj_list = [{
                    "name":"total",
                     "value":total_count},
                     {
                      "name":"completed",
                      "value":completed_count
                      },
                        {
                            "name":"failed",
                            "value":failed_count
                        }

                    ]

        return  JSONResponse(content=obj_list , status_code=200)
    except Exception as e:
        traceback.print_exc()

@router.get('/device_type_counting',
             responses={
                 200: {"model": list[DeviceType]},
                 500: {"model": str}
             },
             summary="Api to get device_type counting from AtomTable",
             description="Api to get device_type counting from AtomTable"
             )
def device_counting():
    try:
        obj_list = []
        obj_dict = {}
        device_values = (
            configs.db.query(AtomTable.device_type, func.count().label("device_type_count"))
            .filter(AtomTable.device_type.isnot(None))
            .join(NcmDeviceTable, NcmDeviceTable.atom_id == AtomTable.atom_id)
            .group_by(AtomTable.device_type)
            .all()
        )

        for device_type, device_type_count in device_values:
            print(f"Device Type: {device_type}, Count: {device_type_count}")
            obj_dict = {"name": device_type, "value": device_type_count}
            obj_list.append(obj_dict)

        if not obj_list:
            obj_list = [{"name": "No Device Type", "value": 0}]

        return JSONResponse(content=obj_list, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Device Type Counts", status_code=500)





# @router.post('/restore_configuration',
#              responses = {
#                  200:{"model":Response200},
#                  400:{"model":str},
#                  500:{"model":str}
#              },
#              summary="Use This API to restore configuration",
#              description="Use This API to restore configuration"
#              )
# def restore_configuration(data:RestoreConfigurationSchema):
#     try:
#         objDict = {}
#         ncm_data = dict(data)
#         device_type =""
#         print("NCM data is::::::::::::::",ncm_data,file=sys.stderr)
#         atom_exsist = configs.db.query(AtomTable).filter_by(ip_address = ncm_data['ip_address']).first()
#         ncm_device = configs.db.query(NcmDeviceTable).filter_by(atom_id = atom_exsist.atom_id).first()
#         if atom_exsist:
#             device_type = atom_exsist.device_type
#             objDict['ip_address'] = atom_exsist.ip_address
#             objDict['device_type'] = atom_exsist.device_type
#             objDict['device_name'] = atom_exsist.device_name
#             password_exsist = configs.db.query(PasswordGroupTable).filter_by(password_group_id = atom_exsist.password_group_id).first()
#             print("passowrd exsist is::::::",password_exsist,file=sys.stderr)
#             objDict['password'] = password_exsist.password.strip()
#             objDict['username'] = password_exsist.username.strip()
#         restore_configuration_puller = RestorePuller()
#         if device_type == "cisco_ios_xe":
#             device_type = "cisco_xe"
#
#         elif device_type == "cisco_ios_xr":
#             device_type = "cisco_xr"
#
#         elif device_type == "paloalto":
#             device_type = "paloalto_panaos"
#
#         elif device_type == 'h3c':
#             device_type = 'hp_comware'
#
#         end_result = restore_configuration_puller.poll(
#             objDict,device_type,ncm_data['date']
#         )
#         print("rnd resuotl for the restoration is the",end_result,file=sys.stderr)
#         if restore_configuration_puller.Success() == True:
#                 data = {
#                     "configuration":{
#                         "ncm_device_id":ncm_device.ncm_device_id,
#                         "status":ncm_device.status,
#                         "ip_address":atom_exsist.ip_address,
#                         "date":ncm_device.config_change_date
#                     },
#                 "message":f"{atom_exsist.ip_address} Is Restored"
#                 }
#                 return data
#         elif restore_configuration_puller.FileDoesNotExist():
#             return JSONResponse(content="File Does Not Exsist",status_code=500)
#         elif restore_configuration_puller.FailedLogin():
#             return JSONResponse(content="Failed To Login",status_code=500)
#     except Exception as e:
#         traceback.print_exc()
#         return JSONResponse(content="Error Occured While Restoring Configuration",status_code=500)


# @router.get('/recent_configuration',
#             responses={
#                 400:{"model":str},
#                 500:{"model":str}
#             },
#             summary="Recent Configuration API",
#             description="Recent Configuration SPI"
#             )
# def get_recent_configuration(request: Request):
#     try:
#         data = {}
#         queryString = f"select distinct CONFIGURATION_DATE from ncm_history_table order by CONFIGURATION_DATE desc limit 2;"
#         result = configs.db.execute(queryString).fetchall()
#         for row in result:
#             dt1 = row[1]
#             queryString1 = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE={dt1};"
#         if queryString == "" or queryString1 =="":
#             return JSONResponse(content="One of the Configuration Not Found",status_code=500)
#         else:
#             html_diff = ConfDiff(f"{queryString}",f"{queryString1}")
#             # difference = html_diff.diff()
#             # if difference is None:
#             #     return JSONResponse(content="No Difference Found In Configurations", status_code=500)
#             return configs.templates.TemplateResponse("html_diff_output.html", context=request,
#                                                   status_code=200)
#     except Exception as e:
#         print("Error:",str(e))
#         traceback.print_exc()
#
#
#
#
#
#
#
# @router.post('/download_configuration',
#              responses={
#                  200: {"model": Response200},
#                  400: {"model": str},
#                  500: {"model": str}
#              },
#              summary="To download configuration",
#              description="to download configuration"
#              )
# def download_configuration(ncm_obj: str):
#     try:
#         ncm_obj = dict(ncm_obj)
#         if "ncm_history_id" not in ncm_obj or ncm_obj['ncm_history_id'] is None:
#             return "NCM History ID Is Missing OR Empty", 500
#
#         history = configs.db.query(NCM_History_Table).filter(
#             NCM_History_Table.ncm_history_id == ncm_obj["ncm_history_id"]
#         ).first()
#
#         if history is None:
#             return "Configuration Does Not Exist", 500
#
#         if history.file_name != "":
#             cwd = os.getcwd()
#             path = cwd + f"/app/configuration_backups/{history.file_name}"
#             path_exists = os.path.exists(path)
#
#             if path_exists:
#                 with open(path, "r") as f:
#                     output = f.read()
#                     if output == "":
#                         return "Configuration Does Not Exist", 500
#                     else:
#                         data = {
#                             output
#                         }
#                         data['message'] = f"{history.file_name} : Downloaded Successfully"
#                         return JSONResponse(content=data, status_code=200)
#             else:
#                 return JSONResponse(content="File Does Not Exist", status_code=500)
#         else:
#             return JSONResponse(content="File Does Not Exist", status_code=500)
#     except Exception as e:
#         traceback.print_exc()
#
#
#
# def checkFile(id):
#     queryString = f"select file_name from ncm_history_table h1 where h1.ncm_device_id= {id} and h1.configuration_date = (SELECT MAX(h2.configuration_date) FROM ncm_history_table h2 WHERE h2.ncm_device_id = h1.ncm_device_id);"
#     result = configs.db.execute(queryString)
#     file_name = ""
#
#     for row in result:
#         file_name += row[0]
#
#     if file_name != "":
#         cwd = os.getcwd()
#         path = cwd + f"/app/configuration_backups/{file_name}"
#         pathExists = os.path.exists(path)
#
#         output = ""
#         if pathExists:
#             f = open(path, "r")
#             output = f.read()
#             if output == "":
#                 return None
#
#             return file_name, output
#
#         else:
#             return None
#     else:
#         return None
#
#
# def bulkDownloadThread(ncmObj, responseList, errorList):
#     ncmPuller = NCMPuller()
#     ncmPuller.setup_puller(ncmObj)
#
#     if ncmPuller.status == 500:
#         errorList.append(ncmPuller.response)
#     else:
#         ncmPuller.backup_config()
#
#         if ncmPuller.status == 200:
#             responseList.append(ncmPuller.response)
#         else:
#             errorList.append(ncmPuller.response)
#
#
# @router.post('/download_bulk_configuration',
#              responses= {
#                  200:{"model":str},
#                  400:{"model":str},
#                  500:{"model":str}
#              },
#              summary="API to download bulk configuration",
#              description="API to download bulk configuration"
#              )
# def download_bulk_configuration(ips:list[str]):
#     try:
#         ips = dict(ips)
#         print("ips in download bulk configuration is:::",ips,file=sys.stderr)
#         final_result = []
#         pullet_lst = []
#         for ip in ips:
#             file_data = checkFile(ip)
#             if file_data is None:
#                 pullet_lst.append(ip)
#             else:
#                 file_name,output = file_data
#                 final_result.append({"name":file_name,"value":output})
#
#         threads = []
#         for ip in pullet_lst:
#             print("ip in puller list is::::::::::",ip,file=sys.stderr)
#             thread = threading.Thread(
#                 target=bulkDownloadThread,
#                 args=(
#                     ip,
#                     final_result
#                 ),
#             )
#             thread.start()
#             threads.append(thread)
#
#         for thread in threads:
#             thread.join()
#         return JSONResponse(content=final_result,status_code=200)
#
#     except Exception as e:
#         traceback.print_exc()
#         return  JSONResponse(content="Error Occured While Downloading Bulk Configuration",status_code=500)
#
#
# @router.post('/delete_configuration',
#              responses = {
#                  200:{"model":DeleteResponseSchema},
#                  400:{"model":str},
#                  500:{"model":str}
#              },
#              summary="API to delte configuration",
#              description="API to delete configuration"
#              )
# def delete_configuration(configurationObj:list['str']):
#     try:
#         configurationObj = dict(configurationObj)
#         print("configuration obj is :::::::::",configurationObj,file=sys.stderr)
#         for conf in configurationObj:
#             print("conf is::::::::::::",conf,file=sys.stderr)
#             config_exsist = configs.db.query(NCM_History_Table).filter(file_name = conf).first()
#             if config_exsist:
#
#                 DeleteDBData(config_exsist)
#                 if os.path.exists(f"{conf}.cfg"):
#                     os.remove(f"{conf}.cfg")
#             else:
#                 return JSONResponse(content=f"{conf} : Configuration Not Found",status_code=400)
#     except Exception as e:
#         traceback.print_exc()
#         return JSONResponse(content="Error Occurred While Deleting Configuration",status_code=500)
#
#
# @router.get('/most_recent_changes',
#             responses = {
#                 400:{"model":str},
#                 500:{"model":str}
#             },
#             description="API to get the most recent changes",
#             summary="API to get the most recent changes"
#             )
# def most_recent_changes(request: Request):
#     try:
#         cwd = os.getcwd()
#         existing_path = f"{cwd}/app/templates/html_diff_output_most_recent.html"
#         existing_path1 = os.path.exists(existing_path)
#         print("Existing path is:::::::::",existing_path,file=sys.stderr)
#         print("Existing path1 is:::::::::::;",existing_path1,file=sys.stderr)
#         if existing_path1:
#             print("Existing file removed:::::",file=sys.stderr)
#             os.remove(existing_path)
#         else:
#             pass
#         queryString = f"SELECT CONFIGURATION_DATE from ncm_history_table order by CONFIGURATION_DATE DESC LIMIT 2;"
#         result = configs.db.execute(queryString)
#         print("result is:::::::::::::",result,file=sys.stderr)
#         dateList = []
#         for row in result:
#             dateList.append(row[0])
#         if len(dateList) <=2:
#             return JSONResponse(content="There Should Be At-least Two Backup",status_code=400)
#         else:
#             fileList = []
#             queryString1 = f"SELECT FILE_NAME from ncm_history_table where CONFIGURATION_DATE='{dateList[1]}';"
#             result1 = configs.db.execute(queryString1)
#             for row in result1:
#                 fileList.append(row[0])
#             queryString2 = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE='{dateList[0]}';"
#             result2 = configs.db.execute(queryString2)
#             for row in result2:
#                 fileList.append(row[0])
#             if len(fileList) ==2:
#                 cwd = os.getcwd()
#                 path = f"{cwd}/app/configuration_backups"
#                 path1 = f"/app/app/templates/html_diff_output_most_recent.html"
#                 html_diff = ConfDiff(
#                     f"{path} {fileList[0]}.cfg",f"{path} {fileList[1]}.cfg",path1
#                 )
#                 html_diff.diff()
#                 return configs.templates.TemplateResponse("html_diff_output.html", context=request,
#                                                           status_code=200)
#
#             else:
#                 return "Something Went Wrong",500
#
#     except Exception as e:
#         traceback.print_exc()
#         return  JSONResponse(content="Error Ooccured While Getting Most Recent Changes",status_code=500)



#
#
#
#
#
#
#
#
#
#
















# # @app.route('/recentConfigrations',methods = ["GET"])
# # # @token_required
# # def recentConfigrations():
# #     if True:
# #         try:
# #             queryString = f"select distinct CONFIGURATION_DATE  from ncm_history_table  order by CONFIGURATION_DATE desc limit 2;"
# #             result = db.session.execute(queryString).fetchall()
# #             for row in result:
# #                 dt=row[0]
# #                 queryString = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE={dt};"
# #             for row in result:
# #                 dt1=row[1]
# #                 queryString1 = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE={dt1};"
# #             if queryString=="" or queryString1=="":
# #                 return "One of the Configurations Not Found",500
# #             else:
# #                 # cwd = os.getcwd()
# #                 # path = f"{cwd}/app/configuration_backups/"
# #                 # path1 = f"/app/app/templates/html_diff_output.html"
# #                 html_diff = ConfDiff(f"{queryString}, f"{queryString1}")
# #                 html_diff.diff()
#
# #                 return render_template('html_diff_output.html'),200
# #         except Exception as e:
# #             print(str(e),file=sys.stderr)
# #             traceback.print_exc()
# #             return str(e),500
# #     else:
# #         print("Authentication Failed", file=sys.stderr)
# #         return jsonify({'message': 'Authentication Failed'}), 401
#
#
# @app.route("/bulkBackupConfigurations", methods=["POST"])
# @token_required
# def BulkBackupConfigurations(user_data):
#     try:
#         ids = request.get_json()
#
#         errorList = []
#         responseList = []
#
#         for id in ids:
#             ncmObj = {"ncm_device_id": id}
#
#             ncmPuller = NCMPuller()
#             ncmPuller.setup_puller(ncmObj)
#
#             if ncmPuller.status == 500:
#                 errorList.append(ncmPuller.response)
#                 continue
#
#             ncmPuller.backup_config()
#
#             if ncmPuller.status == 200:
#                 responseList.append(ncmPuller.response)
#             else:
#                 errorList.append(ncmPuller.response)
#
#         responseDict = {
#             "success": len(responseList),
#             "error": len(errorList),
#             "error_list": errorList,
#             "success_list": responseList,
#         }
#
#         return jsonify(responseDict), 200
#
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return "Server Error In Bulk Configuration Backup", 500
#
#
# @app.route("/downloadConfiguration", methods=["POST"])
# @token_required
# def DownloadConfiguration(user_data):
#     try:
#         ncmObj = request.get_json()
#
#         if "ncm_history_id" not in ncmObj.keys():
#             return "NCM Device ID Is Missing", 500
#
#         if ncmObj["ncm_history_id"] is None:
#             return "NCM Device ID Is Empty", 500
#
#         history = NCM_History_Table.query.filter(
#             NCM_History_Table.ncm_history_id == ncmObj["ncm_history_id"]
#         ).first()
#
#         if history is None:
#             return "Configuration Does Not Exits", 500
#
#         if history.file_name != "":
#             cwd = os.getcwd()
#             path = cwd + f"/app/configuration_backups/{history.file_name}"
#             pathExists = os.path.exists(path)
#
#             if pathExists:
#                 f = open(path, "r")
#                 output = f.read()
#                 if output == "":
#                     return "Configuration Does Not Exist", 500
#                 else:
#                     return jsonify({"name": history.file_name, "value": output}), 200
#
#             else:
#                 return "File Does Not Exist", 500
#         else:
#             return "File Does Not Exist", 500
#
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return "Error While Downloading Backup File", 500
#
#
# def checkFile(id):
#     queryString = f"select file_name from ncm_history_table h1 where h1.ncm_device_id= {id} and h1.configuration_date = (SELECT MAX(h2.configuration_date) FROM ncm_history_table h2 WHERE h2.ncm_device_id = h1.ncm_device_id);"
#     result = db.session.execute(queryString)
#     file_name = ""
#
#     for row in result:
#         file_name += row[0]
#
#     if file_name != "":
#         cwd = os.getcwd()
#         path = cwd + f"/app/configuration_backups/{file_name}"
#         pathExists = os.path.exists(path)
#
#         output = ""
#         if pathExists:
#             f = open(path, "r")
#             output = f.read()
#             if output == "":
#                 return None
#
#             return file_name, output
#
#         else:
#             return None
#     else:
#         return None
#
#
# def bulkDownloadThread(ncmObj, responseList, errorList):
#     ncmPuller = NCMPuller()
#     ncmPuller.setup_puller(ncmObj)
#
#     if ncmPuller.status == 500:
#         errorList.append(ncmPuller.response)
#     else:
#         ncmPuller.backup_config()
#
#         if ncmPuller.status == 200:
#             responseList.append(ncmPuller.response)
#         else:
#             errorList.append(ncmPuller.response)
#
#
# @app.route("/downloadBulkConfiguration", methods=["POST"])
# @token_required
# def DownloadBulkConfiguration(user_data):
#     if True:
#         try:
#             ips = request.get_json()
#             print(ips, file=sys.stderr)
#             finalResult = []
#
#             pullerList = []
#             for ip in ips:
#                 file_data = checkFile(ip)
#
#                 if file_data is None:
#                     pullerList.append(ip)
#                 else:
#                     file_name, output = file_data
#                     finalResult.append({"name": file_name, "value": output})
#
#             threads = []
#             for ip in pullerList:
#                 thread = threading.Thread(
#                     target=bulkDownloadThread,
#                     args=(
#                         ip,
#                         finalResult,
#                     ),
#                 )
#                 thread.start()
#                 threads.append(thread)
#
#             for thread in threads:
#                 thread.join()
#
#             return jsonify(finalResult), 200
#
#         except Exception as e:
#             print(str(e), file=sys.stderr)
#             traceback.print_exc()
#             return str(e), 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#
# @app.route("/deleteConfigurations", methods=["POST"])
# @token_required
# def DeleteConfigurations(user_data):
#     try:
#         configurationObjs = request.get_json()
#         for configurationObj in configurationObjs:
#             queryString = (
#                 f"delete from ncm_history_table where FILE_NAME='{configurationObj}';"
#             )
#             db.session.execute(queryString)
#             db.session.commit()
#             if os.path.exists(f"{configurationObj}.cfg"):
#                 os.remove(f"{configurationObj}.cfg")
#             else:
#                 print("The file does not exist")
#         return "Configurations Deleted Successfully", 200
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return str(e), 500
#
#
# @app.route("/mostRecentChanges", methods=["GET"])
# @token_required
# def MostRecentChanges(user_data):
#     if True:
#         try:
#             cwd = os.getcwd()
#             existingPath = f"{cwd}/app/templates/html_diff_output_most_recent.html"
#             existingPath1 = os.path.exists(existingPath)
#             if existingPath1:
#                 print("Existing File Removed", file=sys.stderr)
#                 os.remove(existingPath)
#             else:
#                 pass
#             queryString = f"select CONFIGURATION_DATE from ncm_history_table order by CONFIGURATION_DATE DESC LIMIT 2;"
#             result = db.session.execute(queryString)
#             dateList = []
#             for row in result:
#                 dateList.append(row[0])
#             if len(dateList) <= 2:
#                 return "There Should be Atleast Two Backups", 500
#             else:
#                 fileList = []
#                 queryString1 = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE='{dateList[1]}';"
#                 result1 = db.session.execute(queryString1)
#                 for row in result1:
#                     fileList.append(row[0])
#                 queryString2 = f"select FILE_NAME from ncm_history_table where CONFIGURATION_DATE='{dateList[0]}';"
#                 result2 = db.session.execute(queryString2)
#                 for row in result2:
#                     fileList.append(row[0])
#                 if len(fileList) == 2:
#                     cwd = os.getcwd()
#                     path = f"{cwd}/app/configuration_backups/"
#                     path1 = f"/app/app/templates/html_diff_output_most_recent.html"
#                     html_diff = ConfDiff(
#                         f"{path}{fileList[0]}.cfg", f"{path}{fileList[1]}.cfg", path1
#                     )
#                     html_diff.diff()
#
#                     return render_template("html_diff_output.html"), 200
#                 else:
#                     return "Something Went Wrong", 500
#         except Exception as e:
#             print(str(e), file=sys.stderr)
#             traceback.print_exc()
#             return str(e), 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#
# @app.route("/restoreConfiguration", methods=["POST"])
# @token_required
# def RestoreConfiguration(user_data):
#     return "Service Not Available At This Time", 500
#     if True:
#         try:
#             ncmObj = request.get_json()
#             queryString = f"select IP_ADDRESS,DEVICE_TYPE,PASSWORD_GROUP,DEVICE_NAME from ncm_table where IP_ADDRESS='{ncmObj['ip_address']}';"
#             result = db.session.execute(queryString)
#
#             for row in result:
#                 objDict = {}
#                 ip_address = row[0]
#                 device_type = row[1]
#                 password_group = row[2]
#                 device_name = row[3]
#                 objDict["ip_address"] = ip_address
#                 objDict["device_type"] = device_type
#                 objDict["device_name"] = device_name
#                 queryString2 = f"select USERNAME,PASSWORD from password_group_table where password_group='{password_group}';"
#                 result2 = db.session.execute(queryString2)
#                 for row2 in result2:
#                     username = row2[0]
#                     password = row2[1]
#                     username = username.strip()
#                     password = password.strip()
#                     objDict["username"] = username
#                     objDict["password"] = password
#
#             restoreConfigurationPoller = RestorePuller()
#
#             if device_type == "cisco_ios_xe":
#                 device_type = "cisco_xe"
#             if device_type == "cisco_ios_xr":
#                 device_type = "cisco_xr"
#
#             endResult = restoreConfigurationPoller.poll(
#                 objDict, device_type, ncmObj["date"]
#             )
#             if restoreConfigurationPoller.success() == True:
#                 return "Configuration Restored Successfully", 200
#             elif restoreConfigurationPoller.FileDoesNotExist() == True:
#                 return "File Does Not Exist", 500
#             elif restoreConfigurationPoller.FailedLogin():
#                 return "Failed to Login into Device", 500
#
#         except Exception as e:
#             print(str(e), file=sys.stderr)
#             traceback.print_exc()
#             return str(e), 500
#     else:
#         print("Authentication Failed", file=sys.stderr)
#         return jsonify({"message": "Authentication Failed"}), 401
#
#

# @app.route("/getAllConfigurationDatesInString", methods=["POST"])
# @token_required
# def GetAllConfigurationDatesInString(user_data):
#     try:
#         ncmObj = request.get_json()
#
#         if "ncm_device_id" not in ncmObj.keys():
#             return "NCM Device ID Is Missing", 500
#
#         if ncmObj["ncm_device_id"] is None:
#             return "NCM Device ID Is Empty", 500
#
#         results = NCM_History_Table.query.filter(
#             NCM_History_Table.ncm_device_id == ncmObj["ncm_device_id"]
#         ).all()
#
#         objList = []
#         for history in results:
#             date = (history.configuration_date).strftime("%Y-%m-%d %H:%M:%S")
#             objList.append(date)
#
#         return jsonify(objList), 200
#     except Exception as e:
#         print(str(e), file=sys.stderr)
#         traceback.print_exc()
#         return "Server Error While Fetching Configuration Dates", 500
#
#








