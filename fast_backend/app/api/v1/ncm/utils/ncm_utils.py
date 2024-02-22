from app.models.ncm_models import *
from app.api.v1.atom.utils.atom_utils import *
from app.core.config import *




def FormatDate(date):
    # print(date, addIosTrackerfile=sys.stderr)
    if date is not None:
        result = date.strftime('%d-%m-%Y')
    else:
        # result = datetime(2000, 1, 1)
        result = datetime(1, 1, 2000)

    return result


def add_ncm_device_util(ncm_obj, update):
    try:
        ncm_data_dict = {}
        print("ncm obj is::::::::::::::::::::::",ncm_obj,file=sys.stderr)
        response, status = add_complete_atom(ncm_obj, update)
        print("repsonse in ncm is:::::::::::::::::",response,file=sys.stderr)
        print("status is::::::::::::::::",status,file=sys.stderr)
        if status != 200:
            return response, status

        atom = configs.db.query(AtomTable).filter(
            AtomTable.ip_address == ncm_obj["ip_address"]
        ).first()
        print("atom is:::::::::::",atom,file=sys.stderr)
        ncm = configs.db.query(NcmDeviceTable).filter(
            NcmDeviceTable.atom_id == atom.atom_id
        ).first()
        print("ncm is :::::::::::::",ncm,file=sys.stderr)
        exist = True
        if ncm is None:
            exist = False

        if not update:
            if exist:
                return f"{atom.ip_address} : Device Already Exists In NCM", 400
            else:
                ncm = NcmDeviceTable()
                ncm.atom_id = atom.atom_id

            ncm_obj["status"] = str(ncm_obj["status"]).strip()
            if ncm_obj["status"].lower() == "active":
                ncm.status = "Active"
            else:
                ncm.status = "InActive"


        if exist:
            status = UpdateDBData(ncm)
            if status == 200:
                data = {
                    "ncm_device_id": ncm.ncm_device_id,
                    "status": ncm.status,
                    "config_change_date": ncm.config_change_date,
                    "backup_status": ncm.backup_status
                }
                msg = f"{atom.ip_address} : NCM Device Updated Successfully"
                ncm_data_dict['data'] = data
                ncm_data_dict['message'] = msg
                print(msg, file=sys.stderr)
            else:
                msg = f"{atom.ip_address} : Error While Updating NCM Device"
        else:
            status = InsertDBData(ncm)
            if status == 200:
                # ncm_device_id = ncm.ncm_device_id
                data = {
                    "ncm_device_id":ncm.ncm_device_id,
                    "status":ncm.status,
                    "config_change_date":ncm.config_change_date,
                    "backup_status":ncm.backup_status
                }
                msg = f"{atom.ip_address} : NCM Device Inserted Successfully"
                ncm_data_dict['data'] = data
                ncm_data_dict['message'] = msg
                print(msg, file=sys.stderr)
            else:
                msg = f"{atom.ip_address} : Error While Inserting NCM Device"
                print(msg, file=sys.stderr)

        return ncm_data_dict, status

    except Exception:
        traceback.print_exc()
        return f"Error : Exception", 500


def edit_ncm_device_util(ncm_obj):
    try:
        ncm_obj = dict(ncm_obj)
        print("ncm obj is:::::::",ncm_obj,file=sys.stderr)
        ncm_data_dict = {}
        atom = configs.db.query(AtomTable).filter_by(ip_address = ncm_obj['ip_address']).first()
        print("atom is::::::::::::::::::::::",atom,file=sys.stderr)
        atom_id = atom.atom_id
        ncm_obj['atom_id'] = atom_id
        print("ncm obj is::::::::::::::::::::::",ncm_obj,file=sys.stderr)
        response, status = edit_atom_util(ncm_obj)
        print("repsosne is::::::;;;;;;;;;;;;;;;;;;;;",response,file=sys.stderr)
        print("status is:::::::::::::::::::::::::::::::",status,file=sys.stderr)
        if status != 200:
            return response, status

        ncm = configs.db.query(NcmDeviceTable).filter(
            NcmDeviceTable.atom_id == atom_id
        ).first()

        if ncm is None:
            return "Device Not Found In NCM", 400

        ncm_obj["status"] = str(ncm_obj["status"]).strip()
        if ncm_obj["status"].lower() == "active":
            ncm.status = "Active"
        else:
            ncm.status = "InActive"

        status = UpdateDBData(ncm)
        if status == 200:
            data = {
                "ncm_device_id": ncm.ncm_device_id,
                "status": ncm.status,
                "config_change_date": ncm.config_change_date,
                "backup_status": ncm.backup_status
            }
            msg = f"{ncm_obj['ip_address']} : NCM Device Updated Successfully"
            ncm_data_dict['data'] = data
            ncm_data_dict['message'] = msg
            print(msg, file=sys.stderr)
        else:
            msg = f"{ncm_obj['ip_address']} : Error While Updating NCM Device"

        return ncm_data_dict, status

    except Exception:
        traceback.print_exc()
        return f"Error : Exception Occurred", 500
