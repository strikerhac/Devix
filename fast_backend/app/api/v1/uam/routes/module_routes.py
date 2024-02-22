from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query
from app.api.v1.uam.utils.uam_utils import FormatDate
from app.api.v1.uam.utils.module_utils import *
from app.schema.uam_module_schema import *

router = APIRouter(
    prefix="/uam-module",
    tags=["uam-module"],
)

#getBoardDetailsByIpAddress
@router.get("/get_board_details_by_ip_address", responses={
    200: {"model": list[GetBoardResponseSchema]},
    400: {"model": str},
    500: {"model": str}
},
summary = "Use this API in UAM Devices Page to get the inforamtion of board based on the ip click",
description = "Use this API in UAM Devices Page to get the inforamtion of board based on the ip click"
)
async def get_board_details_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:
        atom = configs.db.query(AtomTable).filter(AtomTable.ip_address == ip_address).first()
        if atom is None:
            return JSONResponse(content="no device found in atom with the given ip address",
                                status_code=400)

        uam = configs.db.query(UamDeviceTable).filter(
            UamDeviceTable.atom_id == atom.atom_id).first()
        if uam is None:
            return JSONResponse(content="no device found in uam with the given ip address",
                                status_code=400)

        results = configs.db.query(BoardTable).filter(BoardTable.uam_id == uam.uam_id).all()

        obj_list = []
        for board in results:
            try:
                obj_dict = {
                    "board_id": board.board_id,
                    "board_name": board.board_name,
                    "device_name": atom.device_name,
                    "serial_number": board.serial_number,
                    "pn_code": board.pn_code,
                    "status": board.status,
                    "device_slot_id": board.device_slot_id,
                    "software_version": board.software_version,
                    "hardware_version": board.hardware_version,
                    "manufacture_date": FormatDate(board.manufacture_date),
                    "eos_date": FormatDate(board.eos_date),
                    "eol_date": FormatDate(board.eol_date),
                    "creation_date": FormatDate(board.creation_date),
                    "modification_date": board.modification_date
                }
                obj_list.append(obj_dict)

            except Exception:
                traceback.print_exc()
        return obj_list
        # return JSONResponse(content=obj_list, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error While Fetching Board Data", status_code=500)
# getSubBoardDetailsByIpAddress
@router.get("/get_subboard_details_by_ip_address", responses={
    200: {"model": list[GetSubboardResponseSchema]},
    400: {"model": str},
    500: {"model": str}
},
summary = "Use this APi in the UAM Device Page to get the information of subboard based on the ip click",
description = "Use this APi in the UAM Device Page to get the information of subboard based on the ip click"
)
async def get_subboard_details_by_ip_address(ip_address: str = Query(..., description="IP address of the device")):
    try:
        atom = configs.db.query(AtomTable).filter(AtomTable.ip_address == ip_address).first()
        if atom is None:
            return JSONResponse(content="no device found in atom with the given ip address",
                                status_code=400)

        uam = configs.db.query(UamDeviceTable).filter(
            UamDeviceTable.atom_id == atom.atom_id).first()
        if uam is None:
            return JSONResponse(content="no device found in uam with the given ip address",
                                status_code=400)

        results = configs.db.query(SubboardTable).filter(SubboardTable.uam_id == uam.uam_id).all()

        obj_list = []
        for subboard in results:
            try:
                objDict = {"subboard_name": subboard.subboard_name,
                           "device_name": atom.device_name,
                           "subboard_type": subboard.subboard_type,
                           "subrack_id": subboard.subrack_id,
                           "slot_number": subboard.slot_number,
                           "subslot_number": subboard.subslot_number,
                           "software_version": subboard.software_version,
                           "hardware_version": subboard.hardware_version,
                           "serial_number": subboard.serial_number,
                           "creation_date": str(subboard.creation_date),
                           "modification_date": str(subboard.modification_date),
                           "status": subboard.status,
                           "manufacturer_date": str(subboard.manufacture_date),
                           "eos_date": str(subboard.eos_date),
                           "eol_date": str(subboard.eol_date),
                           "rfs_date": str(subboard.rfs_date),
                           "pn_code": subboard.pn_code,
                           "subboard_id": subboard.subboard_id}
                obj_list.append(objDict)

            except Exception:
                traceback.print_exc()

        return JSONResponse(content=obj_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error While Fetching Sub-Board Data", status_code=500)


@router.get("/get_all_boards", responses={
    200: {"model": list[GetBoardResponseSchema]},
    500: {"model": str}
},
summary = "Use this API in the UAM Module Page to list down the information all boards in th table",
description = "Use this API in the UAM Module Page to list down the information all boards in th table"
)
async def get_all_boards():
    try:
        boardObjList = []

        results = (
            configs.db.query(BoardTable, UamDeviceTable, AtomTable)
            .join(UamDeviceTable, BoardTable.uam_id == UamDeviceTable.uam_id)
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .all()
        )

        for boardObj, uam, atom in results:
            try:
                boardDataDict = {
                                "board_id":boardObj.board_id,
                                "board_name": boardObj.board_name,
                                 "device_name": atom.device_name,
                                 "device_slot_id": boardObj.device_slot_id,
                                 "software_version": boardObj.software_version,
                                 "hardware_version": boardObj.hardware_version,
                                 "serial_number": boardObj.serial_number,
                                 "manufacturer_date": str(boardObj.manufacture_date),
                                 "creation_date": str(boardObj.creation_date),
                                 "modification_date": str(boardObj.modification_date),
                                 "status": boardObj.status,
                                 "eos_date": str(boardObj.eos_date),
                                 "eol_date": str(boardObj.eol_date),
                                 "rfs_date": str(boardObj.rfs_date),
                                 "pn_code": boardObj.pn_code}

                boardObjList.append(boardDataDict)
            except Exception:
                traceback.print_exc()

        return JSONResponse(content=boardObjList, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error While Getting Board Data", status_code=500)


@router.get("/get_all_sub_boards", responses={
    200: {"model": list[GetSubboardResponseSchema]},
    500: {"model": str}
})
def get_all_subboards():
    try:
        subboardObjList = []

        results = (
            configs.db.query(SubboardTable, UamDeviceTable, AtomTable)
            .join(
                UamDeviceTable,
                SubboardTable.uam_id == UamDeviceTable.uam_id,
            )
            .join(AtomTable, UamDeviceTable.atom_id == AtomTable.atom_id)
            .all()
        )

        for subboardObj, uam, atom in results:
            try:
                subboardDataDict = {"subboard_name": subboardObj.subboard_name,
                                    "device_name": atom.device_name,
                                    "subboard_type": subboardObj.subboard_type,
                                    "subrack_id": subboardObj.subrack_id,
                                    "slot_number": subboardObj.slot_number,
                                    "subslot_number": subboardObj.subslot_number,
                                    "software_version": subboardObj.software_version,
                                    "hardware_version": subboardObj.hardware_version,
                                    "serial_number": subboardObj.serial_number,
                                    "creation_date": str(subboardObj.creation_date),
                                    "modification_date": str(subboardObj.modification_date),
                                    "status": subboardObj.status,
                                    "eos_date": str(subboardObj.eos_date),
                                    "eol_date": str(subboardObj.eol_date),
                                    "rfs_date": str(subboardObj.rfs_date),
                                    "pn_code": subboardObj.pn_code,
                                    "subboard_id":subboardObj.subboard_id
                                    }

                subboardObjList.append(subboardDataDict)
            except Exception:
                traceback.print_exc()

        return JSONResponse(content=subboardObjList, status_code=200)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error While Getting Sub-Board Data", status_code=500)


@router.get("/add_board", responses={
    200: {"model": str},
    400: {"model": str},
    500: {"model": str}
})
def add_board(board_obj: AddBoardRequestSchema):
    try:
        msg, status = add_board_util(board_obj)
        print(msg, file=sys.stderr)
        return JSONResponse(content=msg, status_code=status)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)

# @app.route("/editBoard", methods=["POST"])
# @token_required
# def EditBoard(user_data):
#     try:
#         boardObj = request.get_json()
#         print(boardObj, file=sys.stderr)
#
#         board = (
#             Board_Table.query.with_entities(Board_Table)
#             .filter_by(board_name=boardObj["board_name"])
#             .first()
#         )
#
#         board.rfs_date = FormatStringDate(boardObj["rfs_date"])
#
#         if UpdateDBData(board) == 200:
#             return "Board Updated Successfully", 200
#         else:
#             return "Error While Updating Board", 500
#     except Exception as e:
#         traceback.print_exc()
#         return "Server Error", 500
#
#
# @app.route("/editSubBoard", methods=["POST"])
# @token_required
# def EditSubBoard(user_data):
#     try:
#         subBoardObj = request.get_json()
#         print(subBoardObj, file=sys.stderr)
#
#         subBoard = (
#             Subboard_Table.query.with_entities(Subboard_Table)
#             .filter_by(subboard_name=subBoardObj["subboard_name"])
#             .first()
#         )
#
#         subBoard.rfs_date = FormatStringDate(subBoardObj["rfs_date"])
#
#         if UpdateDBData(subBoard) == 200:
#             return "Sub-Board Updated Successfully", 200
#         else:
#             return "Error While Updating Sub-Board", 500
#
#     except Exception as e:
#         traceback.print_exc()
#         return "Server Error", 500
