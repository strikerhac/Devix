from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.api.v1.uam.utils.sntc_utils import FormatDate,FormatStringDate
# from app.schema.uam_device_schema import *
from fastapi import FastAPI, Query
from app.models.uam_models import *
from app.api.v1.uam.utils.uam_utils import *
from app.utils.static_list import *
from app.core.config import *

from app.schema.uam_sntc_schema import *

router = APIRouter(
    prefix="/uam_sntc",
    tags=["uam_sntc"],
)


@router.get('/get_all_sntc',responses={
    200: {"model": list[GetSntcSchema]},
    500: {"model": str}
},
summary = "Use this api in HW Life cycle UAM module to list down all the sntc in the table",
description = "Use this api in HW Life cycle UAM module to list down all the sntc in the table"
)
async def get_all_sntcs():
    try:
        sntc_list = []
        sntc_results = configs.db.query(SntcTable).filter(SntcTable.pn_code !="" and SntcTable.pn_code != "N/A").all()
        print("sntc result is::::::::::::::::::::::::::::::",sntc_results,file=sys.stderr)
        for sntcs in sntc_results:
            print("sntc result is:::::::::::::::::::::::::",sntcs,file=sys.stderr)
            sntc_dict = {
                "sntc_id":sntcs.sntc_id,
                "pn_code":sntcs.pn_code,
                "hw_eos_date":FormatDate(sntcs.hw_eos_date),
                "hw_eol_date":FormatDate(sntcs.hw_eol_date),
                "sw_eos_date":FormatDate(sntcs.sw_eos_date),
                "sw_eol_date":FormatDate(sntcs.sw_eol_date),
                "manufacture_date":FormatDate(sntcs.manufacture_date),
                "creation_date":FormatDate(sntcs.creation_date),
                "modification_date":FormatDate(sntcs.modification_date)
            }
            sntc_list.append(sntc_dict)
        sorted_list = sorted(sntc_list, key=lambda x: x['creation_date'], reverse=True)
        return JSONResponse(content =sorted_list,status_code=200)
    except Exception as e:
        traceback.print_exc()
        configs.db.rollback()
        return JSONResponse(content = "Error Occured while fetching SNTC",status_code = 500)
        

@router.get('/sync_from_inventory',
            responses={
                200: {"model":list[SummeryResponseSchema]},
                400:{"model":str},
                500: {"model": str}
            },
            summary="Use this API in HW lifecycle to sync from inventory in UAM module Upon calling this API it will check for the pn_code in device,board,subboard and sfp if exsist in sntc it will update else insert in sntc table",
            description="Use this API in HW lifecycle to sync from inventory in UAM module Upon calling this API it will check for the pn_code in device,board,subboard and sfp if exsist in sntc it will update else insert in sntc table"
)
async def sync_from_inventorys():
    try:
        data_lst = []
        error_list = []
        success_list = []

        tables = ['uam_device_table', 'board_table', 'subboard_table', 'sfp_table']
        existing_pn_codes = set()

        # Fetching existing pn_code values in sntc_table for later update check
        existing_query = "SELECT pn_code FROM sntc_table;"
        existing_results = configs.db.execute(existing_query)
        for row in existing_results:
            existing_pn_code = row.pn_code
            existing_pn_codes.add(existing_pn_code)

        # Iterating through tables to fetch and process data
        for table in tables:
            query_string = f"""
                SELECT DISTINCT pn_code
                FROM {table};
            """
            result = configs.db.execute(query_string)

            for row in result:
                pn_code = row.pn_code

                # Check if pn_code exists in sntc_table for update or insert
                if pn_code not in existing_pn_codes:
                    # Insert new entry if pn_code doesn't exist in sntc_table
                    sntc = SntcTable(pn_code=pn_code, creation_date=datetime.now(), modification_date=datetime.now())
                    configs.db.add(sntc)
                    configs.db.commit()

                    data_lst.append({
                        "sntc_id":sntc.sntc_id,
                        "pn_code": sntc.pn_code,
                        "hw_eos_date": FormatDate(sntc.hw_eos_date),
                        "hw_eol_date": FormatDate(sntc.hw_eol_date),
                        "sw_eos_date": FormatDate(sntc.sw_eos_date),
                        "sw_eol_date": FormatDate(sntc.sw_eol_date),
                        "manufacture_date": FormatDate(sntc.manufacture_date),
                        "creation_date": FormatDate(sntc.creation_date),
                        "modification_date": FormatDate(sntc.modification_date)
                    })
                    success_list.append(f"{sntc.pn_code} : Inserted in SNTC Table")
                else:
                    # Update existing entry if pn_code exists in sntc_table
                    sntc = configs.db.query(SntcTable).filter_by(pn_code=pn_code).first()
                    if sntc:
                        sntc.modification_date = datetime.now()
                        configs.db.commit()

                        data_lst.append({
                            "sntc_id":sntc.sntc_id,
                            "pn_code": sntc.pn_code,
                            "hw_eos_date": FormatDate(sntc.hw_eos_date),
                            "hw_eol_date": FormatDate(sntc.hw_eol_date),
                            "sw_eos_date": FormatDate(sntc.sw_eos_date),
                            "sw_eol_date": FormatDate(sntc.sw_eol_date),
                            "manufacture_date": FormatDate(sntc.manufacture_date),
                            "creation_date": FormatDate(sntc.creation_date),
                            "modification_date": FormatDate(sntc.modification_date)
                        })
                        success_list.append(f"{sntc.pn_code} : Updated In SNTC Table")

        response = SummeryResponseSchema(
            data=data_lst,
            success=len(success_list),
            error=len(error_list),
            success_list=success_list,
            error_list=error_list
        )
        return response

    except Exception as e:
        configs.db.rollback()
        return f"Error: {str(e)}", 500
@router.get('/sync_to_inventory',
            responses={
                200: {"model": List[SummeryResponseSchema]},
                400:{"model":str},
                500: {"model": str}
            },
            summary="Use this API in HW lifecycle in sync to inventory UAM module Upon calling this API this will check for the pn code in the device,board,subboard and sfps table update them",
            description="Use this API in HW lifecycle in sync to inventory UAM module Upon calling this API this will check for the pn code in the device,board,subboard and sfps table update them"
)
async def sync_to_inventory():
    try:
        error_list = []
        success_list = []
        data_lst = []
        results = configs.db.query(SntcTable).all()
        print("results re::::::::::::::",results,file=sys.stderr)
        sync_results = []

        for sntc in results:
            try:
                print("sntc in result is:::::::::::",sntc,file=sys.stderr)
                # Create a new dictionary for each table update
                updated_fields = {}

                # UAM Devices Sync
                uam_rows = configs.db.query(UamDeviceTable).filter(
                    UamDeviceTable.pn_code == sntc.pn_code
                ).all()

                for uam in uam_rows:
                    if uam:
                        # Update UAM Device Table
                        # Update necessary fields
                        if sntc.hw_eos_date:
                            uam.hw_eos_date = sntc.hw_eos_date
                            updated_fields['hw_eos_date'] = sntc.hw_eos_date
                        if sntc.hw_eol_date:
                            uam.hw_eol_date = sntc.hw_eol_date
                            updated_fields['hw_eol_date'] = sntc.hw_eol_date
                        if sntc.sw_eos_date:
                            uam.sw_eos_date = sntc.sw_eos_date
                            updated_fields['sw_eos_date'] = sntc.sw_eos_date
                        if sntc.sw_eol_date:
                            uam.sw_eol_date = sntc.sw_eol_date
                            updated_fields['sw_eol_date'] = sntc.sw_eol_date
                        if sntc.manufacture_date:
                            uam.manufacture_date = sntc.manufacture_date
                            updated_fields['manufacture_date'] = sntc.manufacture_date

                        UpdateDBData(uam)
                        updated_fields['uam_id'] = uam.uam_id
                        uam_updated_object = {
                            "data": updated_fields.copy()  # Create a copy to append distinct dictionary objects
                        }
                        print("updates uam object is::",uam_updated_object,file=sys.stderr)
                        data_lst.append(updated_fields.copy())
                        success_list.append(f"{uam.uam_id} : UAM Updated Successfully")
                    else:
                        error_list.append("UAM Not updated")

                # Board Sync
                board_rows = configs.db.query(BoardTable).filter(
                    BoardTable.pn_code == sntc.pn_code
                ).all()

                for board in board_rows:
                    if board:
                        # Update Board Table
                        # Update necessary fields
                        if sntc.hw_eos_date:
                            board.eos_date = sntc.hw_eos_date
                            updated_fields['eos_date'] = sntc.hw_eos_date
                        if sntc.hw_eol_date:
                            board.eol_date = sntc.hw_eol_date
                            updated_fields['eol_date'] = sntc.hw_eol_date
                        if sntc.manufacture_date:
                            board.manufacture_date = sntc.manufacture_date
                            updated_fields['manufacture_date'] = sntc.manufacture_date

                        UpdateDBData(board)
                        updated_fields['board_id'] = board.board_id
                        board_updated_object = {"data": updated_fields.copy()}
                        data_lst.append(updated_fields.copy())
                        success_list.append(f"{board.board_id} : Board Updated Successfully")
                    else:
                        error_list.append("Board Not Updated")

                # Subboard Sync
                subboard_rows = configs.db.query(SubboardTable).filter(
                    SubboardTable.pn_code == sntc.pn_code
                ).all()

                for subboard in subboard_rows:
                    if subboard:
                        # Update Subboard Table
                        # Update necessary fields
                        if sntc.hw_eos_date:
                            subboard.eos_date = sntc.hw_eos_date
                            updated_fields['eos_date'] = sntc.hw_eos_date
                        if sntc.hw_eol_date:
                            subboard.eol_date = sntc.hw_eol_date
                            updated_fields['eol_date'] = sntc.hw_eol_date
                        if sntc.manufacture_date:
                            subboard.manufacture_date = sntc.manufacture_date
                            updated_fields['manufacture_date'] = sntc.manufacture_date

                        UpdateDBData(subboard)
                        updated_fields['subboard_id'] = subboard.subboard_id
                        subboard_updated_object = {"data": updated_fields.copy()}
                        data_lst.append(updated_fields.copy())
                        success_list.append(f"{subboard.subboard_id} : Subboard Updated Successfully")
                    else:
                        error_list.append("Subboard Not Updated")

                # SFPs Sync
                sfps_rows = configs.db.query(SfpsTable).filter(
                    SfpsTable.pn_code == sntc.pn_code
                ).all()

                for sfp in sfps_rows:
                    if sfp:
                        # Update SFPs Table
                        # Update necessary fields
                        if sntc.hw_eos_date:
                            sfp.eos_date = sntc.hw_eos_date
                            updated_fields['eos_date'] = sntc.hw_eos_date
                        if sntc.hw_eol_date:
                            sfp.eol_date = sntc.hw_eol_date
                            updated_fields['eol_date'] = sntc.hw_eol_date

                        UpdateDBData(sfp)
                        updated_fields['sfp_id'] = sfp.sfp_id
                        sfp_updated_object = {"data": updated_fields.copy()}
                        data_lst.append(updated_fields.copy())
                        success_list.append(f"{sfp.sfp_id} : SFP Updated Successfully")
                    else:
                        error_list.append("SFP Not Updated")

            except Exception as e:
                traceback.print_exc()
                error_list.append("Error Occurred While syncing to inventory")

        response = SummeryResponseSchema(
            data=data_lst,
            success=len(success_list),
            error=len(error_list),
            success_list=success_list,
            error_list=error_list
        )
        return response

    except Exception as e:
        configs.db.rollback()
        raise JSONResponse(status_code=500, content="Error Occurred while syncing to Inventory")
@router.post('/edit_sntc',
             responses={
                 200: {"model": Response200},
                 400: {"model": str},
                 500: {"model": str},
             },
summary="Use this in UAM Hw lifecycle page to edit the SNTC entry based on the sntc_id Pn_code is not editable",
description="Use this in UAM Hw lifecycle page to edit the SNTC entry based on the sntc_id Pn_code is not editable",
)
async def edit_sntc(sntcObj: SntcEditRequest):
    try:
        sntc = configs.db.query(SntcTable).filter_by(sntc_id=sntcObj.sntc_id).first()
        if sntc:
            sntc.pn_code = sntcObj.pn_code
            sntc.hw_eos_date = sntcObj.hw_eos_date
            sntc.hw_eol_date = sntcObj.hw_eol_date
            sntc.sw_eos_date = sntcObj.sw_eos_date
            sntc.sw_eol_date = sntcObj.sw_eol_date
            sntc.manufacture_date = sntcObj.manufacture_date
            configs.db.commit()

            sntc_data_dict = {
                "data": sntcObj.dict(),
                "message": f"{sntcObj.sntc_id} : Updated"
            }
            return sntc_data_dict
        else:
            return JSONResponse(status_code=400, content=f"{sntcObj.sntc_id} : Not Found")
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content="Internal Server Error")
    


@router.post('/delete_pn_code',
            responses={
    200: {"model": ListtDeleteResponseSchema},
    400: {"model": str},
    500: {"model": str}
},
summary = "Use this API in the HW Lifecycle to delete the SNTC based on the sntc_id it is accepting list of sntc_ids",
description = "Use this API in the HW Lifecycle to delete the SNTC based on the sntc_id it is accepting list of sntc_ids"
)
async def delete_pn_code(sntc_id: List[int]):
    success_list = []
    error_list = []
    deleted_ids = []
    
    for obj in sntc_id:
        posID = Configs.db.query(SntcTable).filter(SntcTable.sntc_id == obj).first()
        if posID:
            print("post id is:::::::::::::::::::::::::::::",posID,file=sys.stderr)
            configs.db.delete(posID)
            configs.db.commit()
            print("posrt sntc id is:::::::::::::::::",posID.sntc_id,file=sys.stderr)
            deleted_ids.append(posID.sntc_id)
            success_list.append(f"PnCode {obj} deleted successfully")
        else:
            error_list.append(f"No ID found for PnCode {obj}")

    return {
        "data": deleted_ids,
        "success": len(success_list),
        "error": len(error_list),
        "success_list": success_list,
        "error_list": error_list
    }


#sntc\




@router.post('/add_sntc',
             responses={
                 200: {"model": List[SummeryResponseSchema]},
                 400: {"model": str},
                 500: {"model": str}
             },
             summary="Use this API in HW lifecycle While Importing the SNTC",
             description="Use this API in HW lifecycle While Importing the SNTC"
             )
async def AddSntc(sntc_obj: list[AddSntcRequestSchema]):
    try:
        error_list = []
        success_list = []
        data_lst = []


        sntc_obj_list = sntc_obj if isinstance(sntc_obj, list) else [sntc_obj]
        print("sntc obj is:::::::::::::::::::::::::", sntc_obj_list, file=sys.stderr)
        if len(sntc_obj_list)==0:
            error_list.append(f"No matching data found.")
        for sntcObj in sntc_obj_list:
            if sntcObj is not None:
                sntc = SntcTable()

                print(sntcObj, file=sys.stderr)
                sntc.pn_code = sntcObj.pn_code

                if sntcObj.hw_eos_date is not None and sntcObj.hw_eos_date != "NA":
                    try:
                        sntc.hw_eos_date = sntcObj.hw_eos_date
                    except ValueError:
                        print("Incorrect formatting in hw_eos_date", file=sys.stderr)
                        error_list.append("Incorrect formatting in hw_eos_date")
                        traceback.print_exc()

                if sntcObj.hw_eol_date is not None and sntcObj.hw_eol_date != "NA":
                    try:
                        sntc.hw_eol_date = sntcObj.hw_eol_date
                    except ValueError:
                        print("Incorrect formatting in hw_eol_date", file=sys.stderr)
                        error_list.append("Incorrect formatting in hw_eol_date")
                        traceback.print_exc()

                if sntcObj.sw_eos_date is not None and sntcObj.sw_eos_date != "NA":
                    try:
                        sntc.sw_eos_date = sntcObj.sw_eos_date
                    except ValueError:
                        print("Incorrect formatting in sw_eos_date", file=sys.stderr)
                        traceback.print_exc()

                if sntcObj.sw_eol_date is not None and sntcObj.sw_eol_date != "NA":
                    try:
                        sntc.sw_eol_date = sntcObj.sw_eol_date
                    except ValueError:
                        print("Incorrect formatting in sw_eol_date", file=sys.stderr)
                        error_list.append("Incorrect formatting in sw_eol_date")
                        traceback.print_exc()

                if sntcObj.manufacture_date is not None and sntcObj.manufacture_date != "NA":
                    try:
                        sntc.manufacture_date = sntcObj.manufacture_date
                    except ValueError:
                        print("Incorrect formatting in manufacture_date", file=sys.stderr)
                        error_list.append("Incorrect formatting in manufacture_date")
                        traceback.print_exc()

                if (
                        configs.db.query(SntcTable)
                                .with_entities(SntcTable.sntc_id)
                                .filter_by(pn_code=sntcObj.pn_code)
                                .first() is not None
                ):
                    sntc.sntc_id = (
                        configs.db.query(SntcTable)
                        .with_entities(SntcTable.sntc_id)
                        .filter_by(pn_code=sntcObj.pn_code)
                        .first()[0]
                    )
                    print("Updated " + sntcObj.pn_code, file=sys.stderr)
                    sntc.modification_date = datetime.now()
                    UpdateDBData(sntc)
                    sntc_updated_object = {
                        "sntc_id":sntc.sntc_id,
                        "pn_code":sntc.pn_code,
                        "hw_eos_date":sntc.hw_eos_date,
                        "hw_eol_date":sntc.hw_eol_date,
                        "sw_eos_date":sntc.sw_eos_date,
                        "sw_eol_date":sntc.sw_eol_date,
                        "manufacture_date":sntc.manufacture_date
                    }
                    data_lst.append(sntc_updated_object)
                    success_list.append(f"{sntcObj.pn_code} : Updated Successfully")
                else:
                    print("Inserted " + sntcObj.pn_code, file=sys.stderr)
                    sntc.creation_date = datetime.now()
                    sntc.modification_date = datetime.now()
                    InsertDBData(sntc)
                    sntc_insted_object = {
                        "sntc_id": sntc.sntc_id,
                        "pn_code": sntc.pn_code,
                        "hw_eos_date": sntc.hw_eos_date,
                        "hw_eol_date": sntc.hw_eol_date,
                        "sw_eos_date": sntc.sw_eos_date,
                        "sw_eol_date": sntc.sw_eol_date,
                        "manufacture_date": sntc.manufacture_date
                    }
                    data_lst.append(sntc_insted_object)
                    success_list.append(f"{sntcObj.pn_code} : Inserted Successfully")
            else:
                error_list.append(f"No matching data found.")
        response_dict = {
            "data": data_lst,
            "success_list": success_list,
            "error": len(error_list),
            "error_list": error_list
        }
        return response_dict
    except Exception as e:
        traceback.print_exc()
        return "Failed To Update Data", 500


#updated file sntc_route