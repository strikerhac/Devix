from app.api.v1.uam.utils.uam_utils import *
from sqlalchemy.exc import SQLAlchemyError
na = "N/A"
tbf = "TBF"


def insert_uam_device_data(data, atom, ip_addr):
    try:
        # result = (
        #         db.session.query(UAM_Device_Table, Atom_Table)
        #         .join(Atom_Table, Atom_Table.atom_id == UAM_Device_Table.atom_id)
        #         .filter(Atom_Table.ip_address == ip_addr)
        #         .first()
        #     )

        device_obj = configs.db.query(UamDeviceTable).filter(UamDeviceTable.atom_id == atom.atom_id).first()
        print("device obj is:::::::::::::::;",device_obj,file=sys.stderr)
        update = False
        if device_obj is not None:
            update = True

        else:
            device_obj = UamDeviceTable()
            device_obj.atom_id = atom.atom_id

        if "device" in data:
            print("device in data is:::::::::::::::::",data,file=sys.stderr)
            if data["device"]["software_version"] is not None:
                device_obj.software_version = data["device"]["software_version"]
                print("device obj is not none")
            else:
                device_obj.software_version = na
            if "patch_version" in data and data["device"]["patch_version"] is not None:
                device_obj.patch_version = data["device"]["patch_version"]
            else:
                device_obj.patch_version = na
            if data["device"]["status"] is not None:
                device_obj.status = data["device"]["status"]
            else:
                device_obj.status = na

            if data["device"]["manufecturer"] is not None:
                device_obj.manufacturer = data["device"]["manufecturer"]
            else:
                device_obj.manufacturer = na

            if data["device"]["authentication"] is not None:
                device_obj.authentication = data["device"]["authentication"]
            else:
                device_obj.authentication = na
            if data["device"]["serial_number"] is not None:
                device_obj.serial_number = data["device"]["serial_number"]
            else:
                device_obj.serial_number = na
            if data["device"]["pn_code"] is not None:
                device_obj.pn_code = data["device"]["pn_code"]
            else:
                device_obj.pn_code = na
            if data["device"]["hw_version"] is not None:
                device_obj.hardware_version = data["device"]["hw_version"]
            else:
                device_obj.hardware_version = na
            if data["device"]["max_power"] is not None:
                device_obj.max_power = data["device"]["max_power"]
            else:
                device_obj.max_power = na
            if "stack" in data["device"]:
                device_obj.stack = data["device"]["stack"]
            else:
                device_obj.stack = 1
            device_obj.source = "Dynamic"

            if device_obj.pn_code is not None:
                sntcDevice = configs.db.query(SntcTable).filter(
                    SntcTable.pn_code == device_obj.pn_code
                ).first()
                if sntcDevice:
                    if sntcDevice.hw_eos_date is not None:
                        device_obj.hw_eos_date = sntcDevice.hw_eos_date
                    if sntcDevice.hw_eol_date is not None:
                        device_obj.hw_eol_date = sntcDevice.hw_eol_date
                    if sntcDevice.sw_eos_date is not None:
                        device_obj.sw_eos_date = sntcDevice.sw_eos_date
                    if sntcDevice.sw_eol_date is not None:
                        device_obj.sw_eol_date = sntcDevice.sw_eol_date

            # deviceName = UAM_Device_Table.query.with_entities(UAM_Device_Table.device_name).filter_by(ip_address=deviceObj.ip_address).first()

            status_code = 500
            if update:
                print("Updated device " + ip_addr, file=sys.stderr)
                status_code = UpdateDBData(device_obj)
                print("statud code is::::::::::::::::::",status_code,file=sys.stderr)

            else:
                print("Inserted device " + ip_addr, file=sys.stderr)
                status_code = InsertDBData(device_obj)
                print("status code ofr isnertion is:::::::::",status_code,file=sys.stderr)

            uam_id = 0
            if status_code == 200:
                uam_id = device_obj.uam_id
                print("uam id is:::::::::::::::for 200",uam_id,file=sys.stderr)
            return status_code, uam_id
        else:
            print("Device Inventory Not Found", file=sys.stderr)
            return "Device Inventory Not Found", 500
    except Exception as e:
        traceback.print_exc()
        return 500, 0


def insert_uam_device_board_data(uam_id, data):
    try:
        print("Data in insert_uam_device_board_data is:", data, file=sys.stderr)

        # Extracting device data
        device_data = data.get('device', {})
        board_name = device_data.get('chasis_name', 'na')
        serial_number = device_data.get('serial_number', 'na')
        description = device_data.get('desc', 'na')
        pn_code = device_data.get('pn_code', 'na')
        slot_id = device_data.get('desc', 'na')
        print("slot id is::::::::::::::::::::::::::",slot_id,file=sys.stderr)
        print("description is::::::::::::::::::::::::",description,file=sys.stderr)
        device_slot_id = slot_id
        device_pn_code = pn_code
        print("pn code is::::::::::::::::::::::::",device_pn_code,file=sys.stderr)
        # Check and update or insert the main board information before handling individual boards
        main_board_obj = configs.db.query(BoardTable).filter(
            BoardTable.board_name == board_name, BoardTable.uam_id == uam_id
        ).first()

        if main_board_obj:
            # Update main board info
            main_board_obj.serial_number = serial_number
            # main_board_obj.device_slot_id = description
            main_board_obj.pn_code = device_pn_code
            main_board_obj.device_slot_id = device_slot_id
            print(f"{device_slot_id}updated the table for the main chasis board>>>>>>>>>>.",file=sys.stderr)
        else:
            # Insert new main board info
            main_board_obj = BoardTable(
                uam_id=uam_id,
                board_name=board_name,
                serial_number=serial_number,
                status=description,
                pn_code=device_pn_code,
                device_slot_id=device_slot_id
            )
            configs.db.add(main_board_obj)
            print(f"{device_slot_id}isnertion for the main chasis board >>>>>>>",file=sys.stderr)
        configs.db.commit()


        # Process each board in the provided data
        for board in data.get("board", []):
            # Skip entries without a board name
            if not board.get("board_name"):
                continue

            board_name = board["board_name"].strip()
            if board_name == "":
                continue

            board_obj = configs.db.query(BoardTable).filter(
                BoardTable.board_name == board_name, BoardTable.uam_id == uam_id
            ).first()

            update = False
            if board_obj:
                update = True
            else:
                board_obj = BoardTable(uam_id=uam_id, board_name=board_name)

            # Assigning values with fallback to 'na'
            board_obj.device_slot_id = board.get("slot_id", 'na')
            board_obj.hardware_version = board.get("hw_version", 'na')
            board_obj.software_version = board.get("software_version", 'na')
            board_obj.serial_number = board.get("serial_number",
                                                serial_number)  # Fallback to device's serial if not provided
            board_obj.status = board.get("status", 'na')
            board_obj.pn_code = board.get("pn_code", pn_code)  # Fallback to device's pn_code if not provided

            # Insert or update logic as before

            if update:
                print(f"Updated board {board_obj.board_name} with serial number {board_obj.serial_number}",
                      file=sys.stderr)
                UpdateDBData(board_obj)
            else:
                print(f"Inserted board {board_obj.board_name} with serial number {board_obj.serial_number}",
                      file=sys.stderr)
                InsertDBData(board_obj)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        traceback.print_exc()


def insert_uam_device_subboard_data(uam_id, data):
    # print("$$$$$$$$ INSERT UAM DEVICE SUBBOARD DATA ", file=sys.stderr)
    for subboard in data["sub_board"]:
        try:
            if "subboard_name" not in subboard.keys():
                continue

            if subboard["subboard_name"] is None:
                continue

            subboard["subboard_name"] = subboard["subboard_name"].strip()
            if subboard["subboard_name"] == "":
                continue

            subboard_obj = configs.db.query(SubboardTable).filter(
                SubboardTable.board_name == subboard["subboard_name"], uam_id == uam_id
            ).first()

            update = False
            if subboard_obj is not None:
                update = True
            else:
                subboard_obj = SubboardTable()
                subboard_obj.uam_id = uam_id
                subboard_obj.subboard_name = subboard["subboard_name"]

            if subboard["subboard_type"] is not None:
                subboard_obj.subboard_type = subboard["subboard_type"]
            else:
                subboard_obj.subboard_type = na

            if "subrack_id" in subboard and subboard["subrack_id"] is not None:
                subboard_obj.subrack_id = subboard["subrack_id"]
            else:
                subboard_obj.subrack_id = na

            if subboard["slot_number"] is not None:
                subboard_obj.slot_number = subboard["slot_number"]
            else:
                subboard_obj.slot_number = na

            if subboard["subslot_number"] is not None:
                subboard_obj.subslot_number = subboard["subslot_number"]
            else:
                subboard_obj.subslot_number = na

            if subboard["hw_version"] is not None:
                subboard_obj.hardware_version = subboard["hw_version"]
            else:
                subboard_obj.hardware_version = na

            if (
                    "software_version" in subboard
                    and subboard["software_version"] is not None
            ):
                subboard_obj.software_version = subboard["software_version"]
            else:
                subboard_obj.software_version = na

            if subboard["serial_number"] is not None:
                subboard_obj.serial_number = subboard["serial_number"]
            else:
                subboard_obj.serial_number = na

            if subboard["status"] is not None:
                subboard_obj.status = subboard["status"]
            else:
                subboard_obj.status = na

            if subboard["pn_code"] is not None:
                subboard_obj.pn_code = subboard["pn_code"]
            else:
                subboard_obj.pn_code = na

            if subboard_obj.pn_code is not None:
                sntc_device = configs.db.query(SntcTable).filter(
                    SntcTable.pn_code == subboard_obj.pn_code
                ).first()

                if sntc_device:
                    if sntc_device.hw_eos_date is not None:
                        subboard_obj.eos_date = sntc_device.hw_eos_date
                    if sntc_device.hw_eol_date is not None:
                        subboard_obj.eol_date = sntc_device.hw_eol_date

            # if subboardObj.serial_number:
            #     subboardName = (
            #         Subboard_Table.query.with_entities(Subboard_Table.subboard_name)
            #         .filter_by(serial_number=subboardObj.serial_number)
            #         .first()
            #     )
            # else:
            #     subboardName = (
            #         Subboard_Table.query.with_entities(Subboard_Table.subboard_name)
            #         .filter_by(subboard_name=subboardObj.subboard_name)
            #         .first()
            #     )

            if update:
                print(
                    "Updated subboard "
                    + str(subboard_obj.subboard_name)
                    + " with serial number "
                    + subboard_obj.serial_number,
                    file=sys.stderr,
                )
                UpdateDBData(subboard_obj)
            else:
                print(
                    "Inserted subboard "
                    + str(subboard_obj.subboard_name)
                    + " with serial number "
                    + subboard_obj.serial_number,
                    file=sys.stderr,
                )
                InsertDBData(subboard_obj)

        except Exception:
            traceback.print_exc()


def insert_uam_device_sfp_data(uam_id, data):
    for sfp in data["sfp"]:
        print("sfp in insert uam device data is::::::::::::::::::::::::::::",sfp,file=sys.stderr)
        try:
            if "serial_number" not in sfp:
                continue

            if sfp["serial_number"] is None:
                continue

            sfp["serial_number"] = sfp["serial_number"].strip()
            if sfp["serial_number"] == "":
                continue

            sfp_data = configs.db.query(SfpsTable).filter(
                SfpsTable.serial_number == sfp["serial_number"], uam_id == uam_id
            ).first()

            update = False
            if sfp_data is not None:
                update = True
            else:
                sfp_data = SfpsTable()
                sfp_data.uam_id = uam_id
                sfp_data.serial_number = sfp["serial_number"]

            if sfp["media_type"] is not None:
                sfp_data.media_type = sfp["media_type"]
            else:
                sfp_data.media_type = na

            if sfp["port_name"] is not None:
                sfp_data.port_name = sfp["port_name"].strip()
            else:
                sfp_data.port_name = na

            if sfp["port_type"] is not None:
                sfp_data.port_type = sfp["port_type"]
            else:
                sfp_data.port_type = na

            if sfp["connector"] is not None:
                sfp_data.connector = sfp["connector"]
            else:
                sfp_data.connector = na

            if sfp["mode"] is not None:
                sfp_data.mode = sfp["mode"]
            else:
                sfp_data.mode = na

            if sfp["speed"] is not None:
                sfp_data.speed = sfp["speed"]
            else:
                sfp_data.speed = na

            if sfp["wavelength"] is not None:
                sfp_data.wavelength = sfp["wavelength"]
            else:
                sfp_data.wavelength = na

            if sfp["manufacturer"] is not None:
                sfp_data.manufacturer = sfp["manufacturer"]
            else:
                sfp_data.manufacturer = na

            if sfp["optical_direction_type"] is not None:
                sfp_data.optical_direction_type = sfp["optical_direction_type"]
            else:
                sfp_data.optical_direction_type = na

            if sfp["pn_code"] is not None:
                sfp_data.pn_code = sfp["pn_code"]
            else:
                sfp_data.pn_code = na

            if sfp["status"] is not None:
                sfp_data.status = sfp["status"]
            else:
                sfp_data.status = na

            if sfp_data.pn_code is not None:
                sntcDevice = configs.db.query(SntcTable).filter(SntcTable.pn_code == sfp_data.pn_code).first()
                if sntcDevice:
                    if sntcDevice.hw_eos_date is not None:
                        sfp_data.eos_date = sntcDevice.hw_eos_date
                    if sntcDevice.hw_eol_date is not None:
                        sfp_data.eol_date = sntcDevice.hw_eol_date

            # if sfpObj:
            #     if sfpObj.serial_number=="NE":
            #         sfpObj = Sfps_Table.query.with_entities(Sfps_Table).filter_by(device_name=sfpData.device_name).filter_by(port_name=sfpData.port_name.strip()).first()

            if update:
                print(
                    "Updated sfp "
                    + str(sfp_data.port_name)
                    + " with serial number "
                    + sfp_data.serial_number,
                    file=sys.stderr,
                )
                UpdateDBData(sfp_data)
            else:
                print(
                    "Inserted sfp "
                    + str(sfp_data.port_name)
                    + " with serial number "
                    + sfp_data.serial_number,
                    file=sys.stderr,
                )
                InsertDBData(sfp_data)
        except Exception:
            traceback.print_exc()


def insert_uam_device_license_data(uam_id, data):
    # print("$$$$$$$$ INSERT UAM DEVICE LICENSE DATA ", file=sys.stderr)
    for license_obj in data["license"]:
        try:
            if "name" not in license_obj:
                continue

            if license_obj["name"] is None:
                continue

            license_obj["name"] = license_obj["name"].strip()
            if license_obj["name"] == "":
                continue

            license_data = configs.db.query(LicenseTable).filter(
                LicenseTable.license_name == license_obj["name"], uam_id == uam_id
            ).first()

            update = False
            if license_data is not None:
                update = True
            else:
                license_data = LicenseTable()
                license_data.uam_id = uam_id
                license_data.license_name = license_obj["name"]

            if license_obj["description"] is not None:
                license_data.license_description = license_obj["description"]
            else:
                license_data.license_description = na

            if "activation_date" in license_obj:
                license_data.activation_date = FormatStringDate(
                    license_obj["activation_date"]
                )

            if license_obj["grace_period"] is not None:
                license_data.grace_period = license_obj["grace_period"]
            else:
                license_data.grace_period = na

            if "expiry_date" in license_obj:
                license_data.expiry_date = FormatStringDate(license_obj["expiry_date"])

            if license_obj["serial_number"] is not None:
                license_data.serial_number = license_obj["serial_number"]
            else:
                license_data.serial_number = na

            if license_obj["status"] is not None:
                license_data.status = license_obj["status"]
            else:
                license_data.status = na

            if license_obj["capacity"] is not None:
                license_data.capacity = license_obj["capacity"]
            else:
                license_data.capacity = na

            if license_obj["usage"] is not None:
                license_data.usage = license_obj["usage"]
            else:
                license_data.usage = na

            if license_obj["pn_code"] is not None:
                license_data.pn_code = license_obj["pn_code"]
            else:
                license_data.pn_code = na

            if update:
                UpdateDBData(license_data)
            else:
                InsertDBData(license_data)
        except Exception:
            traceback.print_exc()


def insert_uam_device_aps_data(uam_id, data):
    for ap in data["aps"]:
        try:
            if "serial_number" not in ap:
                continue

            if ap["serial_number"] is None:
                continue

            ap["serial_number"] = ap["serial_number"].strip()
            if ap["serial_number"] == "":
                continue

            aps_data = configs.db.query(APS_TABLE).filter(
                APS_TABLE.serial_number == ap["serial_number"], uam_id == uam_id
            ).first()

            update = False
            if aps_data is not None:
                update = True
            else:
                aps_data = APS_TABLE()
                aps_data.uam_id = uam_id
                aps_data.serial_number = ap["serial_number"]

            if "name" in ap:
                aps_data.ap_name = ap["name"]

            if ap["description"] is not None:
                aps_data.description = ap["description"]
            else:
                aps_data.description = na

            if "ip_addr" in ap:
                aps_data.ap_ip = ap["ip_addr"]

            if ap["serial_number"] is not None:
                aps_data.serial_number = ap["serial_number"]
            else:
                aps_data.serial_number = na

            if ap["hw_version"] is not None:
                aps_data.hardware_version = ap["hw_version"]
            else:
                aps_data.hardware_version = na

            if ap["software_version"] is not None:
                aps_data.software_version = ap["software_version"]
            else:
                aps_data.software_version = na

            if update:
                UpdateDBData(aps_data)
            else:
                InsertDBData(aps_data)
        except Exception:
            traceback.print_exc()


def insert_uam_device_aps_data(uam_id, data):
    for ap in data["aps"]:
        try:
            if "serial_number" not in ap:
                continue

            if ap["serial_number"] is None:
                continue

            ap["serial_number"] = ap["serial_number"].strip()
            if ap["serial_number"] == "":
                continue

            aps_data = configs.db.query(APS_TABLE).filter(
                APS_TABLE.serial_number == ap["serial_number"], uam_id == uam_id
            ).first()

            update = False
            if aps_data is not None:
                update = True
            else:
                aps_data = APS_TABLE()
                aps_data.uam_id = uam_id
                aps_data.serial_number = ap["serial_number"]

            if "name" in ap:
                aps_data.ap_name = ap["name"]

            if ap["description"] is not None:
                aps_data.description = ap["description"]
            else:
                aps_data.description = na

            if "ip_addr" in ap:
                aps_data.ap_ip = ap["ip_addr"]

            if ap["serial_number"] is not None:
                aps_data.serial_number = ap["serial_number"]
            else:
                aps_data.serial_number = na

            if ap["hw_version"] is not None:
                aps_data.hardware_version = ap["hw_version"]
            else:
                aps_data.hardware_version = na

            if ap["software_version"] is not None:
                aps_data.software_version = ap["software_version"]
            else:
                aps_data.software_version = na

            if update:
                UpdateDBData(aps_data)
            else:
                InsertDBData(aps_data)
        except Exception:
            traceback.print_exc()


def uam_inventory_data(puller_data):
    failed = False
    try:
        print("puller data in uam inventory data is::::::::::::::",puller_data,file=sys.stderr)
        for ip_addr in puller_data.keys():
            print(f"\n\n{ip_addr} : Checking Device For Onboarding", file=sys.stderr)
            data = puller_data[ip_addr]
            print("data in uam inventory data is:::::::::::::::::::::",data,file=sys.stderr)
            if data["status"] == "error":
                print(f"\n\n{ip_addr} : Error - Login Failed Skipping", file=sys.stderr)
                failed = True
            elif data["status"] == "success":
                atom = configs.db.query(AtomTable).filter(AtomTable.ip_address == ip_addr).first()
                if atom is None:
                    print(f"\n\n{ip_addr} : Error - Not Found In Atom", file=sys.stderr)
                    # return "IP Address Not Found",500
                    failed = True
                    continue

                print(f"\n\n{ip_addr} : Device Found in Atom", file=sys.stderr)

                status_code, uam_id = insert_uam_device_data(data, atom, ip_addr)
                print("status code is :::::::::::::::::",status_code,file=sys.stderr)
                print("uam id is::::::::::::::::::::::::::::;",uam_id,file=sys.stderr)
                if status_code == 200 and uam_id != 0:

                    if data["device"]["manufecturer"] is not None:
                        atom.vendor = data["device"]["manufecturer"]

                    atom.onboard_status = True
                    UpdateDBData(atom)

                    try:
                        insert_uam_device_board_data(uam_id, data)
                        print(
                            f"\n{ip_addr} : Boards Added Successfully", file=sys.stderr
                        )
                    except Exception:
                        print(
                            f"\n{ip_addr} : Error In Board Insertion", file=sys.stderr
                        )
                        traceback.print_exc()

                    try:
                        insert_uam_device_subboard_data(uam_id, data)
                        print(
                            f"\n{ip_addr} : Sub-Boards Added Successfully",
                            file=sys.stderr,
                        )
                    except Exception:
                        print(
                            f"\n{ip_addr} : Error In Sub-Board Insertion",
                            file=sys.stderr,
                        )
                        traceback.print_exc()

                    try:
                        insert_uam_device_sfp_data(uam_id, data)
                        print(f"\n{ip_addr} : SFPs Added Successfully", file=sys.stderr)
                    except Exception:
                        print(
                            f"\n\n{ip_addr} : Error In Sfp Insertion", file=sys.stderr
                        )
                        traceback.print_exc()

                    try:
                        insert_uam_device_license_data(uam_id, data)
                        print(
                            f"\n{ip_addr} : Licenses Added Successfully",
                            file=sys.stderr,
                        )
                    except Exception:
                        print(
                            f"\n\n{ip_addr} : Error In License Insertion",
                            file=sys.stderr,
                        )
                        traceback.print_exc()

                else:
                    print("Device Not Found", file=sys.stderr)
                    failed = True
        return failed
    except Exception as e:
        traceback.print_exc()
        print(
            f"Error while getting data from device error {e}", file=sys.stderr
        )
        failed = True
    return failed