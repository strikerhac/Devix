from app.utils.db_utils import *
from app.models.uam_models import *
from app.models.atom_models import *
from app.models.site_rack_models import *
from fastapi.responses import JSONResponse

def FormatDate(date):
    print(f"String Date : {date}", file=sys.stderr)

    result = None
    try:
        result = date.strftime("%d-%m-%Y")
    except Exception:
        traceback.print_exc()

    return result


def FormatStringDate(date):
    print(f"String Date : {date}", file=sys.stderr)

    try:
        if date is not None:
            if "-" in date:
                return datetime.strptime(date, "%d-%m-%Y")
            elif "/" in date:
                return datetime.strptime(date, "%d/%m/%Y")
            else:
                print("Incorrect date format", file=sys.stderr)
    except Exception as e:
        traceback.print_exc()
        print(f"Date format exception - {e}", file=sys.stderr)

    return None


def get_all_uam_devices_util():
    deviceList = []
    try:
        devices = (
            configs.db.query(UamDeviceTable, AtomTable, RackTable, SiteTable)
            .join(AtomTable, AtomTable.atom_id == UamDeviceTable.atom_id)
            .join(RackTable, RackTable.rack_id == AtomTable.rack_id)
            .join(SiteTable, SiteTable.site_id == RackTable.site_id)
            .all()
        )
        print("devices in get all uam devices util is:::::::::::::::::::::::::::::::::::::::::::",devices,file=sys.stderr)

        for uam, atom, rack, site in devices:
            try:
                deviceDataDict = {}
                deviceDataDict["atom_id"] = atom.atom_id
                deviceDataDict["uam_id"] = uam.uam_id
                deviceDataDict["device_name"] = atom.device_name
                deviceDataDict["site_name"] = site.site_name
                deviceDataDict["rack_name"] = rack.rack_name
                deviceDataDict["ip_address"] = atom.ip_address
                deviceDataDict["device_type"] = atom.device_type
                deviceDataDict["software_type"] = uam.software_type
                deviceDataDict["software_version"] = uam.software_version
                deviceDataDict["creation_date"] = str(uam.creation_date)
                deviceDataDict["modification_date"] = str(uam.modification_date)
                deviceDataDict["status"] = uam.status
                deviceDataDict["ru"] = atom.device_ru
                deviceDataDict["department"] = atom.department
                deviceDataDict["section"] = atom.section
                deviceDataDict["function"] = atom.function
                deviceDataDict["manufacturer"] = uam.manufacturer
                deviceDataDict["hw_eos_date"] = str(uam.hw_eos_date)
                deviceDataDict["hw_eol_date"] = str(uam.hw_eol_date)
                deviceDataDict["sw_eos_date"] = str(uam.sw_eos_date)
                deviceDataDict["sw_eol_date"] = str(uam.sw_eol_date)
                deviceDataDict["virtual"] = atom.virtual
                deviceDataDict["rfs_date"] = str(uam.rfs_date)
                deviceDataDict["authentication"] = uam.authentication
                deviceDataDict["serial_number"] = uam.serial_number
                deviceDataDict["pn_code"] = uam.pn_code
                deviceDataDict["manufacturer_date"] = str(uam.manufacture_date)

                deviceDataDict["source"] = uam.source
                deviceDataDict["stack"] = uam.stack
                deviceDataDict["contract_number"] = uam.contract_number
                deviceDataDict["hardware_version"] = uam.hardware_version
                deviceDataDict["contract_expiry"] = str(uam.contract_expiry)
                deviceDataDict["uptime"] = uam.uptime
                deviceDataDict['status'] = uam.status

                deviceList.append(deviceDataDict)
            except Exception:
                traceback.print_exc()

    except Exception:
        traceback.print_exc()

    return deviceList


def delete_uam_device_util(ip_address):
    try:
        device = (
            configs.db.query(UamDeviceTable, AtomTable)
            .join(AtomTable, AtomTable.atom_id == UamDeviceTable.atom_id)
            .filter(AtomTable.ip_address == ip_address)
            .first()
        )

        if device is None:
            return (f"{ip_address} : Device Not Found"),200

        uam, atom = device

        if uam.status is not None:
            if uam.status == "Production":
                return (
                    f"{ip_address} : Device Is In Production Therefore Can Not Be Deleted"

                ),400
        devices_id = uam.uam_id
        if DeleteDBData(uam) == 200:
            data = {
                "data":devices_id,
                "message":f"{ip_address} : Device Deleted Successfully"
            }
            return data,200
        else:
            return f"{ip_address} : Error While Deleting Device", 500

    except Exception:
        traceback.print_exc()
        return f"{ip_address} : Exceprtion Occured", 500


def edit_uam_device_util(device_obj, uam_id):
    try:
        print("uam is is:::::::::::::::::::::::::::::::",uam_id,file=sys.stderr)
        # Check if Atom ID is provided
        if device_obj["atom_id"] is None:
            return "Atom ID Can Not Be Null", 500

        # Fetch the Atom based on provided Atom ID
        atom_id = device_obj["atom_id"]
        atom = configs.db.query(AtomTable).filter(AtomTable.atom_id == atom_id).first()

        # Return error if the Atom doesn't exist
        if atom is None:
            return "Device Not Found In Atom", 500

        # Check if the device already exists in UAM
        atom_id_uam = configs.db.query(UamDeviceTable).filter_by(atom_id = atom_id).first()
        uam_id = atom_id_uam.uam_id
        print("uam id based on the atom id is::::::::::::::::::::::::::",uam_id,file=sys.stderr)
        exits = False
        if uam_id is not None:
            device = configs.db.query(UamDeviceTable).filter(
                UamDeviceTable.uam_id == uam_id
            ).first()
            print("if uam is not none device id found is::::::::::::::::::::::::::::::",device,file=sys.stderr)
            if device is None:
                return "Device Not Found In UAM", 500

            exits = True
            print("after edvice id is not none exist value so:::::::::::::::::::::::::",exits,file=sys.stderr)
        else:
            # Create a new UamDeviceTable object if it doesn't exist
            device = configs.db.query(UamDeviceTable).filter(
                UamDeviceTable.atom_id == atom_id
            ).first()

        if device is None:
            device = UamDeviceTable()
            device.atom_id = atom_id

        # If Rack Name is not provided, assign default rack ID 1
        if device_obj["rack_name"] is None:
            atom.rack_id = 1
        else:
            rack = configs.db.query(RackTable).filter(
                RackTable.rack_name == device_obj["rack_name"]
            ).first()
            if rack is None:
                return "Invalid Rack Name", 500
            else:
                atom.rack_id = rack.rack_id

        # Strip and assign function to Atom
        device_obj["function"] = str(device_obj["function"]).strip()
        if device_obj["function"] == "":
            return "Function Can Not Be Empty", 500
        atom.function = device_obj["function"]

        # Update other Atom attributes based on device_obj
        if device_obj["ru"] is not None:
            atom.ru = device_obj["ru"]
        # ... (Continue updating other Atom attributes)

        UpdateDBData(atom)  # Update Atom in the database

        # Update device attributes
        if device_obj["software_version"] is not None:
            device.software_version = device_obj["software_version"]
        # ... (Continue updating other device attributes)

        # Determine if status is valid and update the device status
        if device_obj["status"] == "Production":
            pass
        elif device_obj["status"] == "Dismantled":
            pass
        elif device_obj["status"] == "Maintenance":
            pass
        elif device_obj["status"] == "Undefined":
            pass
        else:
            return "Status Is Invalid", 500

        # Perform Insert or Update based on exits variable
        if not exits:
            device.status = device_obj["status"]
            InsertDBData(device)
            # Generate attributes dictionary for the data response
            columns = [column.name for column in device.__table__.columns]
            values = [getattr(device, column) for column in columns]
            attributes_dict = dict(zip(columns, values))
            for key, value in attributes_dict.items():
                if isinstance(value, datetime):
                    attributes_dict[key] = value.isoformat()  # Convert datetime to string format

            update_uam_status_utils(atom.ip_address, device_obj["status"])

            # Generate data response for insertion
            data = {
                "attributes_dict": attributes_dict,
                "message": "Device Inserted Successfully"
            }
            print("data if not exists is:::::::::::::::::::::::::::::::", data, file=sys.stderr)
        else:
            # Update existing device data
            UpdateDBData(device)
            # Generate attributes dictionary for the data response
            columns = [column.name for column in device.__table__.columns]
            values = [getattr(device, column) for column in columns]
            attributes_dict = dict(zip(columns, values))
            for key, value in attributes_dict.items():
                if isinstance(value, datetime):
                    attributes_dict[key] = value.isoformat()  # Convert datetime to string format

            update_uam_status_utils(atom.ip_address, device_obj["status"])

            # Generate data response for update
            data = {
                "attributes_dict": attributes_dict,
                "message": "Device Updated Successfully"
            }
            print("data if exists is:::::::::::::::::::::::::::::::::::::::::::", data, file=sys.stderr)

        return data, 200  # Return the data response and success code (200)
    except Exception:
        traceback.print_exc()  # Print traceback in case of an exception
        return "Exception Occurred", 500  # Return error message and error code (500)



def update_uam_status_utils(ip, status):
    try:
        print("ip is::::::::::::::::::::",ip,file=sys.stderr)
        result = (
            configs.db.query(UamDeviceTable, AtomTable)
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .filter(AtomTable.ip_address == ip)
            .first()
        )
        print("result is::::::::::::::::::::::",result,file=sys.stderr)


        if result is None:
            return (f"{ip} : No Device Found"), 400

        uam, atom = result

        if status != "Production":
            atom.onboard_status = False

        if UpdateDBData(atom) == 200:
            columns_atom = [column.name for column in atom.__table__.columns]
            values_atom = [getattr(atom, column) for column in columns_atom]
            attributes_dict_atom = dict(zip(columns_atom, values_atom))
            for key, value in attributes_dict_atom.items():
                    if isinstance(value, datetime):
                        attributes_dict_atom[key] = value.isoformat()  # Convert datetime to string format

            # change status to dismantle in device table
            uam.status = status
            if UpdateDBData(uam) == 200:
                columns_uam = [column.name for column in uam.__table__.columns]
                values_uam = [getattr(uam, column) for column in columns_uam]
                attributes_dict_uam = dict(zip(columns_uam, values_uam))
                for key, value in attributes_dict_atom.items():
                    if isinstance(value, datetime):
                        attributes_dict_uam[key] = value.isoformat()  # Convert datetime to string format

                # Update status for related objects
                board_objs = (
                    configs.db.query(BoardTable)
                    .filter(BoardTable.uam_id == uam.uam_id)
                    .all()
                )

                for boardObj in board_objs:
                    boardObj.status = status
                    UpdateDBData(boardObj)

                subboard_objs = (
                    configs.db.query(SubboardTable)
                    .filter(SubboardTable.uam_id == uam.uam_id)
                    .all()
                )

                for subboardObj in subboard_objs:
                    subboardObj.status = status
                    UpdateDBData(subboardObj)

                sfp_objs = (
                    configs.db.query(SfpsTable)
                    .filter(SfpsTable.uam_id == uam.uam_id)
                    .all()
                )

                for sfpObj in sfp_objs:
                    sfpObj.status = status
                    UpdateDBData(sfpObj)

                combined_data = {**attributes_dict_atom, **attributes_dict_uam}
                for key, value in combined_data.items():
                    if isinstance(value, datetime):
                         combined_data[key] = value.isoformat()  # Or use str(value) for a different format

                device_data = {
                    "data": combined_data,
                    "message": f"{ip} : Device Status Updated Successfully To {status}"
                }
                print("device data is::::::::::::::::::::::::::::::::::::::::::::::::::",device_data,file=sys.stderr)

                return device_data, 200

            else:
                return  (f"{ip} : Error While Updating Device Status In UAM"), 400

        else:
            return (f"{ip} : Error While Updating Device Status In Atom"), 400
    except Exception:
        traceback.print_exc()
        return {"message": f"{ip} : Error Occurred While Status Update"}, 500
# def update_uam_status_utils(ip, status):
#     try:
#         result = (
#             configs.db.query(UamDeviceTable, AtomTable)
#             .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
#             .filter(AtomTable.ip_address == ip)
#             .first()
#         )

#         if result is None:
#             return f"{ip} : No Device Found", 500

#         uam, atom = result
#         print("atom is::::::::::::::::::::::;",atom,file=sys.stderr)
#         print("uam is::::::::::::::::::::::::::::::",uam,file=sys.stderr)

#         if status != "Production":
#             atom.onboard_status = False

#         if UpdateDBData(atom) == 200:
#             columns = [column.name for column in atom.__table__.columns]  # Get column names
#             values = [getattr(atom, column) for column in columns]  # Get corresponding values
#             attributes_dict = dict(zip(columns, values))  # Combine columns and values into a dictionary
#             print("Columns:", columns, file=sys.stderr)
#             print("Values:", values, file=sys.stderr)
#             print("Attributes dictionary:", attributes_dict, file=sys.stderr)
#             print(f"\n{ip} : Device ONBOARDED STATUS UPDATED IN ATOM", file=sys.stderr)

#             # change status to dismantle in device table
#             uam.status = status
#             if UpdateDBData(uam) == 200:
#                 columns = [column.name for column in uam.__table__.columns]  # Get column names
#                 print("Columns: for uam is::::::::::::::::::::::::::::::::::", columns, file=sys.stderr)
#                 values = [getattr(uam, column) for column in columns]  # Get corresponding values
#                 print("Values: is:::::::::::::::::::::::::::::::::::::::", values, file=sys.stderr)
#                 attributes_dict = dict(zip(columns, values))  # Combine columns and values into a dictionary


#                 print("Attributes dictionary:", attributes_dict, file=sys.stderr)
#                 print(
#                     f"{ip} : {atom.device_name} : Device Status Updated Successfully",
#                     file=sys.stderr,
#                 )
#                 # change all board status
#                 board_objs = (
#                     configs.db.query(BoardTable)
#                     .filter(BoardTable.uam_id == uam.uam_id)
#                     .all()
#                 )

#                 for boardObj in board_objs:
#                     boardObj.status = status
#                     UpdateDBData(boardObj)
#                     print(
#                         f"{ip} : {boardObj.board_name} : Module Status Updated Succedssfully",
#                         file=sys.stderr,
#                     )

#                 # change all sub-board status
#                 subboard_objs = (
#                     configs.db.query(SubboardTable)
#                     .filter(SubboardTable.uam_id == uam.uam_id)
#                     .all()
#                 )

#                 for subboardObj in subboard_objs:
#                     subboardObj.status = status
#                     UpdateDBData(subboardObj)
#                     print(
#                         f"{ip} : {subboardObj.subboard_name} : Stack Switche Updated Successfully",
#                         file=sys.stderr,
#                     )

#                 # change all SFP status
#                 sfp_objs = (
#                     configs.db.query(SfpsTable)
#                     .filter(SfpsTable.uam_id == uam.uam_id)
#                     .all()
#                 )

#                 for sfpObj in sfp_objs:
#                     sfpObj.status = status
#                     UpdateDBData(sfpObj)
#                     print(
#                         f"{ip} : {sfpObj.sfp_id} : SFP Status Updated Successfully",
#                         file=sys.stderr,
#                     )

#                 columns = result._asdict().keys()  # Get column names
#                 # print("column name is::::::::::::::::::::::::::::::::::::::::::::::::::::",columns,file=sys.stderr)
#                 values = result._asdict().values()  # Get corresponding values
#                 # print("values in update uam values utils is::::::::::::::::::::::::::::::::::::",values,file=sys.stderr)
#                 attributes_dict = dict(zip(columns, values))  # Combine columns and values into a dictionary
#                 # print("attribute dict containing the columns and values are:::::::::::::::::::::::::::",attributes_dict,file=sys.stderr)
#                 data = {
#                     "data":attributes_dict,
#                     "message":f"{ip} : Device Status Updated Successfully To {status}"
#                         }
#                 # print("data is:::::::::::::::::::::::::::::::::::::::",data,file=sys.stderr)
#                 return data,200

#             else:
#                 return f"{ip} : Error While Updating Device Status In UAM", 500

#         else:
#             return f"{ip} : Error While Updating Device Status In Atom", 500
#     except Exception:
#         traceback.print_exc()
#         return f"{ip} : Error Occurred While Status Update", 500




# def edit_uam_device_util(device_obj, uam_id):
#     try:

#         if device_obj["atom_id"] is None:
#             return "Atom ID Can Not Be Null", 500

#         atom_id = device_obj["atom_id"]

#         atom = configs.db.query(AtomTable).filter(AtomTable.atom_id == atom_id).first()
#         if atom is None:
#             return "Device Not Found In Atom", 500

#         exits = False
#         if uam_id is not None:
#             device = configs.db.query(UamDeviceTable).filter(
#                 UamDeviceTable.uam_id == uam_id
#             ).first()
#             if device is None:
#                 return "Device Not Found In UAM", 500

#             exits = True
#         else:
#             device = UamDeviceTable()
#             device.atom_id = atom_id

#         if device_obj["rack_name"] is None:
#             atom.rack_id = 1
#         else:
#             rack = configs.db.query(RackTable).filter(
#                 RackTable.rack_name == device_obj["rack_name"]
#             ).first()
#             if rack is None:
#                 return "Invalid Rack Name", 500
#             else:
#                 atom.rack_id = rack.rack_id

#         device_obj["function"] = str(device_obj["function"]).strip()
#         if device_obj["function"] == "":
#             return "Function Can Not Be Empty", 500

#         atom.function = device_obj["function"]

#         if device_obj["ru"] is not None:
#             atom.ru = device_obj["ru"]

#         if device_obj["department"] is not None:
#             atom.department = device_obj["department"]

#         if device_obj["section"] is not None:
#             atom.section = device_obj["section"]

#         if device_obj["criticality"] is not None:
#             atom.criticality = device_obj["criticality"]

#         if device_obj["virtual"] is not None:
#             atom.virtual = device_obj["virtual"]

#         UpdateDBData(atom)

#         if device_obj["software_version"] is not None:
#             device.software_version = device_obj["software_version"]

#         if device_obj["manufacturer"] is not None:
#             device.manufacturer = device_obj["manufacturer"]

#         if device_obj["authentication"] is not None:
#             device.authentication = device_obj["authentication"]

#         if device_obj["serial_number"] is not None:
#             device.serial_number = device_obj["serial_number"]

#         if device_obj["pn_code"] is not None:
#             device.pn_code = device_obj["pn_code"]

#         if device_obj["subrack_id_number"] is not None:
#             device.subrack_id_number = device_obj["subrack_id_number"]

#         if device_obj["source"] is not None:
#             device.source = device_obj["source"]

#         if device_obj["stack"] is not None:
#             device.stack = device_obj["stack"]

#         if device_obj["contract_number"] is not None:
#             device.contract_number = device_obj["contract_number"]

#         device_obj["status"] = str(device_obj["status"]).strip()

#         if device_obj["status"] == "Production":
#             pass
#         elif device_obj["status"] == "Dismantled":
#             pass
#         elif device_obj["status"] == "Maintenance":
#             pass
#         elif device_obj["status"] == "Undefined":
#             pass
#         else:
#             return "Status Is Invalid", 500

#         if not exits:
#             device.status = device_obj["status"]
#             InsertDBData(device)
#         else:
#             UpdateDBData(device)
#             columns = device._asdict().keys()  # Get column names
#             print("column name is::::::::::::::::::::::::::::::::::::::::::::::::::::",columns,file=sys.stderr)
#             values = device._asdict().values()  # Get corresponding values
#             print("values in update uam values utils is::::::::::::::::::::::::::::::::::::",values,file=sys.stderr)
#             attributes_dict = dict(zip(columns, values))  # Combine columns and values into a dictionary
#             print("attribute dict containing the columns and values are:::::::::::::::::::::::::::",attributes_dict,file=sys.stderr)

#         update_uam_status_utils(atom.ip_address, device_obj["status"])

#         return "Device Updated Successfully", 200
#     except Exception:
#         traceback.print_exc()
#         return "Exception Occurred", 500


def onboard_devices_data_fetch(ip):
    try:
        data = {}
        atom_exsist = configs.db.query(AtomTable).filter_by(ip_address = ip).first()
        configs.db.refresh(atom_exsist)
        if atom_exsist:
            password_group_exsist = configs.db.query(PasswordGroupTable).filter_by(password_group_id = atom_exsist.password_group_id).first()
            if password_group_exsist:
                data['password_group'] = password_group_exsist.password_group
            else:
                print("Password Group Not Found",file=sys.stderr)
            rack_exsist = configs.db.query(RackTable).filter_by(rack_id=atom_exsist.rack_id).first()
            if rack_exsist:
                    data['rack_name'] = rack_exsist.rack_name
                    site_exsist = configs.db.query(SiteTable).filter_by(site_id = rack_exsist.site_id).first()
                    if site_exsist:
                        data['site_name'] = site_exsist.site_name

            else:
                print("rack name not found")
            print("atom_exsists onboard status is:::::::::::::::",atom_exsist.onboard_status,file=sys.stderr)
            data['ip_address'] = atom_exsist.ip_address
            data['device_type'] = atom_exsist.device_type
            data['vendor'] = atom_exsist.vendor
            data['device_ru'] = atom_exsist.device_ru
            data['department'] = atom_exsist.department
            data['section'] = atom_exsist.section
            data['criticality'] = atom_exsist.criticality
            data['domain'] = atom_exsist.domain
            data['virtual'] = atom_exsist.virtual
            data['onboard_status'] = atom_exsist.onboard_status
            data['scop'] = atom_exsist.scop
            data['atom_id'] = atom_exsist.atom_id
        configs.db.close()
        return data
    except Exception as e:
        traceback.print_exc()
        return "Error while fetching the devices data fetch",500