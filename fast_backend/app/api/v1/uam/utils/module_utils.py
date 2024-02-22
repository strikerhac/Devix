from app.models.atom_models import *
from app.models.uam_models import *

from app.utils.db_utils import *
from app.core.config import *


def add_board_util(board_obj):
    try:

        board_obj["device_name"] = str(board_obj["device_name"]).strip()
        if board_obj["device_name"] == "":
            return "Device Name Can Not Be Empty", 400

        results = (
            configs.db.query(UamDeviceTable, AtomTable)
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .filter(AtomTable.device_name == board_obj["device_name"])
            .first()
        )

        if results is None:
            return "No Device Found With Given Name", 400

        uam, atom = results

        board = BoardTable()
        board.board_name = board_obj["board_name"]
        board.uam_id = uam.uam_id
        board.device_slot_id = board_obj["device_slot_id"]
        board.software_version = board_obj["software_version"]
        board.hardware_version = board_obj['hardware_version']
        board.serial_number = board_obj["serial_number"]
        board.manufacturer_date = board_obj['manufacturer_date']
        board.status = board_obj["status"]
        board.eos_date = board_obj["eos_date"]
        board.eol_date = board_obj["eol_date"]
        board.rfs_date = board_obj['rfs_date']
        board.pn_code = board_obj["pn_code"]

        if InsertDBData(board) == 200:
            return "Board Added Successfully", 200
        else:
            return "Error While Adding Board Data", 500

    except Exception:
        traceback.print_exc()
        return "Error While Adding Board Data", 500
