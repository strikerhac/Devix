import traceback

from app.api.v1.ipam.routes.device_routes import *
from app.models.ipam_models import *
from app.models.atom_models import *
from app.models.uam_models import *
from app.models.site_rack_models import *
from sqlalchemy import and_, inspect
from app.utils.static_list import *
from app.schema.atom_schema import PasswordGroupTypeEnum


def validate_site(device):
    # Site Check
    default_site = configs.db.query(SiteTable).filter(SiteTable.site_name == "default_site").first()

    if device["site_name"] is None:
        pass
    else:
        device["site_name"] = device["site_name"].strip()

        if device["site_name"] == "":
            pass
        else:
            site_exist = configs.db.query(SiteTable).filter(
                SiteTable.site_name == device["site_name"]
            ).first()
            if site_exist is None:
                return f"{device['ip_address']} : Site Does Not Exists", 400
            else:
                return site_exist, 200

    return default_site, 200


def validate_rack(device, site):
    # Rack Check
    default_rack = configs.db.query(RackTable).filter(RackTable.rack_name == "default_rack").first()

    if device["rack_name"] is None:
        pass
    else:
        device["rack_name"] = device["rack_name"].strip()

        if device["rack_name"] == "":
            pass
        else:
            rack = configs.db.query(RackTable).filter(
                RackTable.rack_name == device["rack_name"]).first()
            if rack is None:
                return f"{device['ip_address']} : Rack Does Not Exists", 400

            elif rack.site_id != site.site_id:
                return f"{device['ip_address']} : Rack And Site Does Not Match", 400

            else:
                return rack, 200

    return default_rack, 200


def validate_password_group(device):
    if device["password_group"] is None:
        pass
    else:
        device["password_group"] = device["password_group"].strip()

        if device["password_group"] == "":
            pass
        else:
            password = configs.db.query(PasswordGroupTable).filter(
                PasswordGroupTable.password_group == device["password_group"]
            ).first()
            if password is None:
                return f"{device['ip_address']} : Password Group Does Not Exist", 400
            else:
                return password, 200

    password = configs.db.query(PasswordGroupTable).filter(
        PasswordGroupTable.password_group == "default_password"
    ).first()

    return password, 200
def check_device_name_uniqueness(device_ip, device_name):
    existing_device = (
        configs.db.query(AtomTable)
        .filter(and_(AtomTable.ip_address != device_ip, AtomTable.device_name == device_name))
        .first()
    )
    return existing_device is None

def validate_atom(device, update):
    try:
        if device["ip_address"].strip() == "" or device['ip_address'] == 'string':
            return f"Ip Address Can Not be Empty", 400
        if device['ip_address'] !="" or device['ip_address']!='string':
            try:
                validate_ip_address = ipaddress.ip_address(device['ip_address'])
            except ValueError:
                print("IP address is not a valid IP address")
                return f"{device['ip_address']} : IP Address is not valid", 400

        if not update:
            if (
                    configs.db.query(AtomTable).filter(
                        AtomTable.ip_address == device["ip_address"]).first()
                    is not None
            ):
                return f"{device['ip_address']} : IP Address Is Already Assigned", 400

            if (
                    configs.db.query(AtomTransitionTable).filter(
                        AtomTransitionTable.ip_address == device["ip_address"]
                    ).first()
                    is not None
            ):
                return f"{device['ip_address']} : IP Address Is Already Assigned", 400

        if device["device_name"] is None or device['device_name'] == 'string':
            return f"{device['ip_address']} : Device Name Can Not be Empty", 400

        device["device_name"] = device["device_name"].strip()
        if device["device_name"] == "":
            return f"{device['ip_address']} : Device Name Can Not be Empty", 400

        atom = configs.db.query(AtomTable).filter_by(ip_address = device["ip_address"]).first()
        if atom is not None:
            atom_device_name = atom.device_name
            if atom_device_name:
                if atom_device_name != device['device_name']:
                    print(f"{device['ip_address']}: already assigned with the {device['device_name']}", file=sys.stderr)
                    return f"{device['ip_address']} : Device Name Already Assigned To Another Device", 400
                else:
                    # For update, check if the device name is unique among other devices
                    is_unique_name = check_device_name_uniqueness(device["ip_address"], device["device_name"])
                    if not is_unique_name:
                        return f"{device['ip_address']} : Device Name Already Assigned To Another Device", 400
        else:
            # For new device addition, check if the device name is unique among other devices
            is_unique_name = check_device_name_uniqueness(device["ip_address"], device["device_name"])
            if not is_unique_name:
                return f"{device['ip_address']} : Device Name Already Assigned To Another Device", 400

        if device["function"] is None or device['function'] == 'string':
            return f"Function Can Not be Empty", 400 #{device['ip_address']} : 

        elif device["function"].strip() == "":
            return f"Function Can Not be Empty", 400 #{device['ip_address']} : 

        if device["device_type"] is None or device['device_type'] == 'string':
            return f"Device Type Can Not be Empty", 400 #{device['ip_address']} : 

        device["device_type"] = device["device_type"].strip()
        device["device_type"] = device["device_type"].lower()

        if device["device_type"] == "":
            return f"Device Type Can Not be Empty", 400 #{device['ip_address']} :

        if device["device_type"] not in device_type_list:
            return f"Device Type Is Not Supported - {device['device_type']}", 400#{device['ip_address']} :

        if device["vendor"] is None:
            return f"Vendor Can Not be Empty", 400 #{device['ip_address']} :
        if device['vendor'] not in vendor_list:
            return f"{device['ip_address']} : Device Vendor Is Unknown",400

        device["vendor"] = str(device["vendor"]).strip().capitalize()
        if device["vendor"] not in vendor_list:
            return f"{device['ip_address']} : Unknown Vendor - {device['vendor']}", 400

        site_exist, site_status = validate_site(device)
        if site_status != 200:
            return site_exist, site_status

        rack_exist, rack_status = validate_rack(device, site_exist)
        if rack_status != 200:
            return rack_exist, rack_status

        password_exist, password_status = validate_password_group(device)
        if password_status != 200:
            return password_exist, password_status

        return {"rack": rack_exist, "password_group": password_exist}, 200

    except Exception:
        error = f"Error : Exception Occurred"
        print(error, file=sys.stderr)
        traceback.print_exc()
        return error, 500


def add_complete_atom(device, update):
    try:
        attributes_dict = {}
        response, status = validate_atom(device, update)
        response_message = response
        response_status = status
        if status != 200:
            return response,400

        rack = response["rack"]
        password = response["password_group"]

        atom = configs.db.query(AtomTable).filter(
            AtomTable.ip_address == device["ip_address"].strip()).first()

        exist = False
        if atom is not None:
            exist = True
            # uam_exist = Device_Table.query.filter_by(ip_address=atom.ip_address, status='Production').first()
            # if uam_exist is not None:
            #     return f"{device['ip_address']} : Device is already in production", 500
        else:
            atom = AtomTable()
            atom.ip_address = device["ip_address"].strip()
            atom.onboard_status = False

        atom.rack_id = rack.rack_id
        atom.device_name = device["device_name"].strip()
        atom.device_type = device["device_type"].strip()
        if password is not None:
            atom.password_group_id = password.password_group_id

        atom.function = device["function"].strip()
        atom.vendor = str(device["vendor"]).capitalize()
        atom.device_ru = device["device_ru"]

        if device["department"] is None:
            atom.department = ""
        elif device["department"].strip() != "":
            atom.department = device["department"].strip()
        else:
            atom.department = ""

        if device["section"] is None:
            atom.section = ""
        elif device["section"].strip() != "":
            atom.section = device["section"].strip()
        else:
            atom.section = ""

        if device["criticality"] is None:
            atom.criticality = ""
        elif device["criticality"].strip() != "":
            atom.criticality = device["criticality"].strip()
        else:
            atom.criticality = ""

        if device["domain"] is None:
            atom.domain = ""
        elif device["domain"].strip() != "":
            atom.domain = device["domain"].strip()
        else:
            atom.domain = ""

        if device["virtual"] is None:
            atom.virtual = ""
        elif device["virtual"].strip() != "":
            atom.virtual = device["virtual"].strip()
        else:
            atom.virtual = ""
        atom_data = {}
        msg = ""
        status = 500
        if exist:
            status = UpdateDBData(atom)
            if status == 200:
                msg = f"{device['ip_address']} : Atom Updated Successfully"
                inspector = inspect(atom.__class__)
                columns = inspector.columns

                # Iterate through columns and fetch values
                for column in columns:
                    column_name = column.key
                    print("column name is::::::::::", column_name, file=sys.stderr)
                    # Exclude 'creation_date' and 'modification_date'
                    if column_name not in ['creation_date', 'modification_date']:
                        value = getattr(atom, column_name, None)
                        attributes_dict[column_name] = value
                        if column_name == 'rack_id':
                            rack = configs.db.query(RackTable).filter_by(rack_id=value).first()
                            if rack:
                                attributes_dict['rack_name'] = rack.rack_name
                                if rack.site_id:
                                    site = configs.db.query(SiteTable).filter_by(site_id=rack.site_id).first()
                                    attributes_dict['site_name'] = site.site_name

                            # Special handling for password_group_id
                        elif column_name == 'password_group_id':
                            password_group = configs.db.query(PasswordGroupTable).filter_by(
                                password_group_id=value).first()
                            if password_group:
                                attributes_dict['password_group'] = password_group.password_group
                        elif column_name == 'onboard_status' or column_name == "":
                            if value:
                                attributes_dict['onboard_status'] = True
                            elif value is None:
                                attributes_dict['onboard_status'] = False
                            else:
                                attributes_dict['onboard_status'] = False
                        else:
                            attributes_dict[column_name] = value
                devices_data = dict(device)
                devices_data['atom_id'] = atom.atom_id
                atom_data = {
                    "data":attributes_dict,
                    "message":msg
                }
                # print(msg, file=sys.stderr)
            else:
                msg = f"{device['ip_address']} : Error While Updating Atom"
        else:
            status = InsertDBData(atom)
            if status == 200:
                msg = f"{device['ip_address']} : Atom Inserted Successfully"
                inspector = inspect(atom.__class__)
                columns = inspector.columns

                # Iterate through columns and fetch values
                for column in columns:
                    column_name = column.key
                    # Exclude 'creation_date' and 'modification_date'
                    if column_name not in ['creation_date', 'modification_date']:
                        value = getattr(atom, column_name, None)
                        attributes_dict[column_name] = value
                        if column_name == 'rack_id':
                            rack = configs.db.query(RackTable).filter_by(rack_id=value).first()
                            if rack:
                                attributes_dict['rack_name'] = rack.rack_name
                                if rack.site_id:
                                    site = configs.db.query(SiteTable).filter_by(site_id=rack.site_id).first()
                                    attributes_dict['site_name'] = site.site_name

                            # Special handling for password_group_id
                        elif column_name == 'password_group_id':
                            password_group = configs.db.query(PasswordGroupTable).filter_by(
                                password_group_id=value).first()
                            if password_group:
                                attributes_dict['password_group'] = password_group.password_group
                        elif column_name == 'onboard_status' or column_name == "":
                            if value:
                                attributes_dict['onboard_status'] = True
                            elif value is None:
                                attributes_dict['onboard_status'] = False
                            else:
                                attributes_dict['onboard_status'] = False
                        else:
                            attributes_dict[column_name] = value
                devices_data = dict(device)
                devices_data['atom_id'] = atom.atom_id
                atom_data = {
                    "data":attributes_dict,
                    "message":msg
                }
            else:
                msg = f"{device['ip_address']} : Error While Inserting Atom"
                # print(msg, file=sys.stderr)

        if status == 200:
            try:
                transit_obj = configs.db.query(AtomTransitionTable).filter(
                    AtomTransitionTable.ip_address == atom.ip_address
                ).first()

                if transit_obj is not None:
                    DeleteDBData(transit_obj)

            except Exception:
                traceback.print_exc()

        return (atom_data),status

    except Exception:
        error = f"Error : Exception Occurred"
        print(error, file=sys.stderr)
        traceback.print_exc()
        return error, 500


def add_transition_atom(device, update):
    try:
        device["ip_address"] = device["ip_address"].strip()

        if device["ip_address"] == "" or device['ip_address'] == 'string':
            print("ip address is empty or a string::::::::::::::::::::::::",file=sys.stderr)
            return f"IP Address Can Not Be Empty", 400
        
        if device['ip_address'] !="" or device['ip_address']!='string':
            try:
                validate_ip_address = ipaddress.ip_address(device['ip_address'])
            except ValueError:
                print("IP address is not a valid IP address")
                return f"{device['ip_address']} : IP Address is not valid", 400

        if not update:
            if (
                    configs.db.query(AtomTable).filter(
                        AtomTable.ip_address == device["ip_address"]).first()
                    is not None
            ):
                return f"{device['ip_address']} : IP Address Is Already Assigned", 400

            if (
                    configs.db.query(AtomTransitionTable).filter(
                        AtomTransitionTable.ip_address == device["ip_address"]
                    ).first()
                    is not None
            ):
                return f"{device['ip_address']} : IP Address Is Already Assigned", 400

        # msg, status = ValidateAtom(device, row, update)

        trans_obj = configs.db.query(AtomTransitionTable).filter(
            AtomTransitionTable.ip_address == device["ip_address"]
        ).first()
        attributes_dict = {}
        processed_ips = {}
        exist = True
        if trans_obj is None:
            exist = False
            trans_obj = AtomTransitionTable()

            trans_obj.ip_address = device["ip_address"]

        trans_obj = fill_transition_data(device, trans_obj)

        if exist:
            status = UpdateDBData(trans_obj)
            if status == 200:
                msg = f"{device['ip_address']} : Atom Updated Successfully"

                # Check if trans_obj exists
                if trans_obj:
                    
                    inspector = inspect(trans_obj.__class__)
                    columns = inspector.columns
                    
                    # Iterate through columns and fetch values
                    for column in columns:
                        column_name = column.key
                        # Exclude 'creation_date' and 'modification_date'
                        if column_name not in ['creation_date', 'modification_date']:
                            value = getattr(trans_obj, column_name, None)
                            attributes_dict[column_name] = value
                            if column_name == 'rack_id':
                                rack = configs.db.query(RackTable).filter_by(rack_id=value).first()
                                if rack:
                                    attributes_dict['rack_name'] = rack.rack_name
                                    if rack.site_id:
                                        site = configs.db.query(SiteTable).filter_by(site_id=rack.site_id).first()
                                        attributes_dict['site_name'] = site.site_name

                                # Special handling for password_group_id
                            elif column_name == 'password_group_id':
                                password_group = configs.db.query(PasswordGroupTable).filter_by(
                                    password_group_id=value).first()
                                if password_group:
                                    attributes_dict['password_group'] = password_group.password_group
                            elif column_name == 'onboard_status' or column_name=="":
                                if value:
                                    attributes_dict['onboard_status'] = True
                                elif value is None:
                                    attributes_dict['onboard_status'] = False
                                else:
                                    attributes_dict['onboard_status'] = False
                            else:
                                attributes_dict[column_name] = value
                            
                transition_data = {
                        "data":attributes_dict,
                        "message":str(msg)
                }
                return (transition_data), 200
            else:
                msg = f"{device['ip_address']} : Error While Updating Atom"
                print(msg, file=sys.stderr)
                return msg, 500
        else:
            status = InsertDBData(trans_obj)
            
            if status == 200:
                msg = f"{device['ip_address']} :Transition Atom Inserted Successfully"

                devices = device
                onboard_status = None
                if trans_obj.onboard_status is None:
                    onboard_status = False
                devices_data ={
                    "atom_transition_id":trans_obj.atom_transition_id,
                    "ip_address":trans_obj.ip_address,
                    "rack_name":trans_obj.rack_name,
                    "device_name":trans_obj.device_name,
                    "vendor":trans_obj.vendor,
                    "device_ru":trans_obj.device_ru,
                    "department":trans_obj.department,
                    "section":trans_obj.section,
                    "criticality":trans_obj.criticality,
                    "function":trans_obj.function,
                    "domain":trans_obj.domain,
                    "virtual":trans_obj.virtual,
                    "device_type":trans_obj.device_type,
                    "password_group":trans_obj.password_group,
                    "onboard_status":onboard_status
                }
                data = {"transition id":trans_obj.atom_transition_id}
                transition_data = {
                    "data":devices_data,
                    "message":msg
                }
                # print(msg, file=sys.stderr)
                return (transition_data), 200
            else:
                msg = f"{device['ip_address']} : Error While Inserting Atom"
                # print(msg, file=sys.stderr)
                return msg, 500

    except Exception:
        error = f"Error : Exception Occurred"
        traceback.print_exc()
        return error, 500


def fill_transition_data(device, trans_obj):
    try:
        if device["device_name"] is not None:
            if device["device_name"].strip() != "":
                trans_obj.device_name = device["device_name"].strip()

        if device["vendor"] is not None:
            if device["vendor"].strip() != "":
                trans_obj.vendor = device["vendor"].strip()

        if device["function"] is not None and device["function"].strip() != "":
            trans_obj.function = device["function"].strip()

        if device["device_type"] is not None:
            if device["device_type"].strip() != "":
                trans_obj.device_type = device["device_type"].strip()

        if device["site_name"] is not None:
            if device["site_name"].strip() != "":
                trans_obj.site_name = device["site_name"].strip()

        if device["rack_name"] is not None:
            if device["rack_name"].strip() != "":
                trans_obj.rack_name = device["rack_name"].strip()

        if device["password_group"] is not None:
            if device["password_group"].strip() != "":
                trans_obj.password_group = device["password_group"].strip()

        trans_obj.device_ru = device["device_ru"]

        if device["department"] is not None:
            if device["department"].strip() != "":
                trans_obj.department = device["department"].strip()

        if device["section"] is not None:
            if device["section"].strip() != "":
                trans_obj.section = device["section"].strip()

        if device["criticality"] is not None:
            if device["criticality"].strip() != "":
                trans_obj.criticality = device["criticality"].strip()

        if device["domain"] is not None:
            if device["domain"].strip() != "":
                trans_obj.domain = device["domain"].strip()

        if device["virtual"] is not None:
            if device["virtual"].strip() != "":
                trans_obj.virtual = device["virtual"].strip()

        if device['device_ru'] is None:
            trans_obj.device_ru =0
        else:
            trans_obj.device_ru = device['device_ru']

        return trans_obj
    except Exception as e:
        traceback.print_exc()


def edit_atom_util(device):
    try:
        print("Received device data:", device, file=sys.stderr)
        atom = None
        trans_atom = None
        data = {}
        attributes_dict = {}

        if "atom_id" not in device and "atom_transition_id" not in device:
            return "Atom ID Or Atom Transition ID is Missing", 400

        # Retrieve atom or trans_atom from the database
        if "atom_id" in device and device["atom_id"] is not None:
            atom = configs.db.query(AtomTable).filter(
                AtomTable.atom_id == device["atom_id"]).first()

        if "atom_transition_id" in device and device["atom_transition_id"] is not None:
            trans_atom = configs.db.query(AtomTransitionTable).filter(
                AtomTransitionTable.atom_transition_id == device["atom_transition_id"]).first()

        if device["ip_address"].strip() == "":
            return "IP Address Cannot be Empty", 400

        # Process the atom or trans_atom
        if atom:
            atom, status = edit_complete_atom(device, atom)
            if status != 200:
                return atom, status
            status = UpdateDBData(atom)
            object_to_inspect = atom

        elif trans_atom:
            # Check for IP address conflicts
            if configs.db.query(AtomTransitionTable).filter(
                    AtomTransitionTable.ip_address == device["ip_address"],
                    AtomTransitionTable.atom_transition_id != device["atom_transition_id"]).first() or \
               configs.db.query(AtomTable).filter(
                    AtomTable.ip_address == device["ip_address"]).first():
                return f"{device['ip_address']} : IP Address Is Already Assigned To Another Device", 400

            trans_atom.ip_address = device['ip_address']
            trans_atom = fill_transition_data(device, trans_atom)
            print("trans atom is:::::::::::::::::::::::::tranistion atom",trans_atom,file=sys.stderr)
            msg, status = add_complete_atom(device, True)
            if status==200:
                return msg,status
            print("message for the add compelte atom is in tranistions",msg,file=sys.stderr)
            print("status for the add compelte atom is:::::::::::::::",status,file=sys.stderr)
            status = UpdateDBData(trans_atom)

            object_to_inspect = trans_atom
        else:
            return "Device Not Found", 400

        # Populate attributes_dict from the object
        if object_to_inspect:
            inspector = inspect(object_to_inspect.__class__)
            columns = inspector.columns
            for column in columns:
                column_name = column.key
                if column_name not in ['creation_date', 'modification_date']:
                    value = getattr(object_to_inspect, column_name, None)
                    attributes_dict[column_name] = value
                    if column_name == 'rack_id':
                        rack = configs.db.query(RackTable).filter_by(rack_id=value).first()
                        if rack:
                            attributes_dict['rack_name'] = rack.rack_name
                            if rack.site_id:
                                site = configs.db.query(SiteTable).filter_by(site_id=rack.site_id).first()
                                attributes_dict['site_name'] = site.site_name

                        # Special handling for password_group_id
                    elif column_name == 'password_group_id':
                        password_group = configs.db.query(PasswordGroupTable).filter_by(password_group_id=value).first()
                        if password_group:
                            attributes_dict['password_group'] = password_group.password_group
                    elif column_name == 'onboard_status':
                        if value:
                            attributes_dict['onboard_status'] = True
                        else:
                            attributes_dict['onboard_status'] = False
                    else:
                        attributes_dict[column_name] = value

        print("Attributes dict:", attributes_dict, file=sys.stderr)

        if status == 200:
            if object_to_inspect is atom:
                msg = f"{device['ip_address']} : Atom Updated Successfully"
            else:
                msg = f"{device['ip_address']} : Transition Atom Updated Successfully"

            data = {
                "data": attributes_dict,
                "message": msg
            }
        else:
            msg = f"{device['ip_address']} : Error While Updating Atom"

        return data, status

    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        traceback.print_exc()
        return "Error: Exception Occurred", 500


def edit_complete_atom(device, atom):
    if configs.db.query(AtomTable).filter(
            AtomTable.ip_address == device["ip_address"], AtomTable.atom_id != device[
                "atom_id"]).first() is not None:
        return f"{device['ip_address']} : IP Address Is Already Assigned To An Other Device", 400

    if configs.db.query(AtomTransitionTable).filter(
            AtomTransitionTable.ip_address == device["ip_address"]).first() is not None:
        return f"{device['ip_address']} : IP Address Is Already Assigned To An Other Device", 400

    # Device Name Check
    if device["device_name"] is None:
        return f"{device['ip_address']} : Device Name Can Not be Empty", 400

    device["device_name"] = device["device_name"].strip()
    if device["device_name"] == "":
        return f"{device['ip_address']} : Device Name Can Not be Empty", 400

    if configs.db.query(AtomTable).filter(
            AtomTable.device_name == device["device_name"], AtomTable.atom_id != device[
                "atom_id"]).first() is not None:
        return f"{device['ip_address']} : Device Name Already Assigned To An Other Device", 400

    if device["function"] is None:
        return f"{device['ip_address']} : Function Can Not be Empty", 400

    elif device["function"].strip() == "":
        return f"{device['ip_address']} : Function Can Not be Empty", 400

    if device["device_type"] is None:
        return f"{device['ip_address']} : Device Type Can Not be Empty", 400

    device["device_type"] = device["device_type"].strip()
    device["device_type"] = device["device_type"].lower()

    if device["device_type"] == "":
        return f"{device['ip_address']} : Device Type Can Not be Empty", 400

    if device["device_type"] not in device_type_list:
        return f"{device['ip_address']} : Device Type Is Not Supported - {device['device_type']}", 400

    site_exist, site_status = validate_site(device)
    if site_status != 200:
        return site_exist, site_status

    rack_exist, rack_status = validate_rack(device, site_exist)
    if rack_status != 200:
        return rack_exist, rack_status

    password_exist, password_status = validate_password_group(device)
    if password_status != 200:
        return password_exist, password_status

    atom.rack_id = rack_exist.rack_id
    atom.ip_address = device["ip_address"]
    atom.device_name = device["device_name"].strip()
    atom.device_type = device["device_type"].strip()
    atom.password_group_id = password_exist.password_group_id
    atom.function = device["function"].strip()
    atom.device_ru = device["device_ru"]

    if device["department"] is None:
        atom.department = ""
    elif device["department"].strip() != "":
        atom.department = device["department"].strip()
    else:
        atom.department = ""

    if device["section"] is None:
        atom.section = ""
    elif device["section"].strip() != "":
        atom.section = device["section"].strip()
    else:
        atom.section = ""

    if device["criticality"] is None:
        atom.criticality = ""
    elif device["criticality"].strip() != "":
        atom.criticality = device["criticality"].strip()
    else:
        atom.criticality = ""

    if device["domain"] is None:
        atom.domain = ""
    elif device["domain"].strip() != "":
        atom.domain = device["domain"].strip()
    else:
        atom.domain = ""

    if device["virtual"] is None:
        atom.virtual = ""
    elif device["virtual"].strip() != "":
        atom.virtual = device["virtual"].strip()
    else:
        atom.virtual = ""

    if "vendor" in device.keys():
        if device["vendor"] is not None:
            device["vendor"] = str(device["vendor"]).strip()
            if device["vendor"] != "" and device["vendor"] != "Unknown":
                atom.vendor = device["vendor"]

    return atom, 200


def get_transition_atoms():
    obj_list = []
    count = 0
    try:
        results = configs.db.query(AtomTransitionTable).all()

        for result in results:
            obj_dict = result.as_dict()

            msg, status = add_complete_atom(obj_dict, True)
            print("msg for get tranistion atom is ::::::::::::::",msg,file=sys.stderr)
            print("status for tranistion atom is ss::::",status,file=sys.stderr)

            if status != 200:
                obj_dict["creation_date"] = str(obj_dict["creation_date"])
                obj_dict["modification_date"] = str(obj_dict["modification_date"])
                obj_dict["message"] = msg
                obj_dict["status"] = status
                obj_dict['atom_table_id'] = count
                obj_list.append(obj_dict)
            
            count +=1
        configs.db.close()
    except Exception:
        configs.db.rollback()
        traceback.print_exc()

    return obj_list


def validate_password_group_name(pass_obj):
    pass_obj["password_group"] = pass_obj["password_group"].strip()

    if pass_obj["password_group"] == "" or pass_obj["password_group"] =='string':
        return f"Password Group Can Not be Empty", 400

    if pass_obj["password_group"] == "default_password":
        return f"{pass_obj['password_group']} : Password Group Name (default_password) Is Not Allowed", 400

    return pass_obj["password_group"], 200


def validate_password_group_credentials(pass_obj, password_exist):
    try:
        print("pass obj is::::::::::::::::::::::::::::::::::;", pass_obj, file=sys.stderr)
        print("password exist is::::::::::::::::::::::::::::::::::::", password_exist, file=sys.stderr)
        pass_obj["username"] = pass_obj["username"].strip()

        if pass_obj["username"] == "":
            return f"{pass_obj['password_group']} : Username Field Can Not Be Empty", 400

        password_exist.username = pass_obj["username"]

        if pass_obj['password_group_type'] is None or pass_obj['password_group_type'] == '':
            return f"Password Group Type cannot be empty", 400

        pass_obj["password"] = pass_obj["password"].strip()

        if pass_obj["password"] == "":
            return f"{pass_obj['password_group']} : Password Field Can Not be Empty", 400

        password_exist.password = pass_obj["password"]

        if pass_obj["password_group_type"] == 'TELNET':
                password_exist.password_group_type = "TELNET"

        if pass_obj["password_group_type"]=="SSH":
                password_exist.password_group_type = "SSH"

        if pass_obj["password_group_type"] not in ['SSH', 'TELNET']:
            error_message = f"Invalid password group type for '{pass_obj['password_group']}'. Please select either 'SSH' or 'TELNET'."
            return error_message, 400
        if "secret_password" in pass_obj and pass_obj["secret_password"]:
                pass_obj["secret_password"] = pass_obj["secret_password"].strip()

        # if pass_obj["secret_password"].strip() == "":
        #             return f"{pass_obj['password_group']} : Secret Password Field Can Not Be Empty For SSH", 400

        password_exist.secret_password = pass_obj["secret_password"]
        print("password exist for the secret password is:::", password_exist.secret_password, file=sys.stderr)

        # else:
        #     return f"{pass_obj['password_group']} : Invalid Password Group Type", 400

        return password_exist, 200
    except Exception as e:
        traceback.print_exc()
        print("Error occurred while validating the password group", str(e))


def add_password_group_util(pass_obj, update):
    try:
        name_response, status = validate_password_group_name(pass_obj)

        if status != 200:
            return name_response, status

        password_group = configs.db.query(PasswordGroupTable).filter(
            PasswordGroupTable.password_group == name_response
        ).first()
        
        # print("password group is::::::::::::::::::::::::::::::",password_group,file=sys.stderr)
        exist = False
        if password_group is not None:
            if not update:
                return f"{pass_obj['password_group']} : Password Group Already Exists",400
            else:
                exist = True

        if not exist:
            password_group = PasswordGroupTable()
            password_group.password_group = name_response
            pass_id = password_group.password_group_id
            # print("pass id issssssssssssssssss:::::::::::::::::::::::::::",pass_id,file=sys.stderr)

        password_group, status = validate_password_group_credentials(
            pass_obj, password_group
        )
        print("password group for validate passowrd group credential is::",password_group)
        if status != 200:
            return password_group, status

        if update:
            
            status = UpdateDBData(password_group)
            if status == 200:
                
                pass_data = dict(pass_obj)
                passworg_group_update = configs.db.query(PasswordGroupTable).filter_by(password_group = pass_data['password_group']).first()
                if passworg_group_update:
                    password_group_id = passworg_group_update.password_group_id
                    pass_data['password_group_id'] = password_group_id
                    msg=   f"{pass_obj['password_group']} : Password Group Updated Successfully"
                    password_group_data = {
                        "data":pass_data,
                        "message":msg
                    }
                    return (
                        password_group_data
                    ),200
                else:
                    print("error in password group updates")
        else:
            
            status = InsertDBData(password_group)
            if status == 200:
                pass_data = dict(pass_obj)
                password_group_id = password_group.password_group_id
                pass_data['password_group_id'] = password_group_id
                msg=   f"{pass_obj['password_group']} : Password Group Inserted Successfully"
                password_group_data = {
                    "data":pass_data,
                    "message":msg
                }
                return (
                    password_group_data
                ),200

        return f"{pass_obj['password_group']} : Server Error", 500

    except Exception:
        traceback.print_exc()
        return f"Server Error", 500


def edit_password_group_util(pass_obj):
    try:

        password_exist = configs.db.query(PasswordGroupTable).filter(
            PasswordGroupTable.password_group_id == pass_obj["password_group_id"]).first()

        if password_exist is None:
            return f"Password Group Does Not Found", 400

        if password_exist.password_group == "default_password":
            return f"Password Group (default_password) Is Not Editable", 400

        name_response, status = validate_password_group_name(pass_obj)
        print("validate passsword group staus is::::::::::",status,file=sys.stderr)

        if status != 200:
            return name_response, status

        password_group = configs.db.query(PasswordGroupTable).filter(
            PasswordGroupTable.password_group == name_response).first()
        
        if password_group is not None:
            if password_exist.password_group_id != password_group.password_group_id:
                return f"{pass_obj['password_group']} : Password Group Name Is Already Assigned",400
                

        password_exist.password_group = name_response

        password_exist, status = validate_password_group_credentials(
            pass_obj, password_exist
        )
        if status != 200:
            return password_exist, status

        status = UpdateDBData(password_exist)
        if status == 200:
            configs.db.merge(password_exist)
            configs.db.commit()
            pass_data = dict(pass_obj)
            password_group_id = password_group.password_group_id
            pass_data['password_group_id'] = password_group_id
            msg=f"{pass_obj['password_group']} : Password Group Updated Successfully"
            password_group_data = {
                    "data":pass_data,
                    "message":msg
            }
            return (
                    password_group_data
                ),200
            # return (
            #     f"{pass_obj['password_group']} : Password Group Updated Successfully",
            #     200,
            # )

        return f"{pass_obj['password_group']} : Server Error", 500

    except Exception:
        traceback.print_exc()
        return f"Server Error", 500
