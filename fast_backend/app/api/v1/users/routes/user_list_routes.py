import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.config import *
from app.utils.static_list import *

router = APIRouter(
    prefix="/user_static_list",
    tags=["user_static_list"],
)



@router.get('/get_user_status',responses={
    200:{"model":str},
    500:{"model":str}
},
description="API to list down the user status in the add user dropdown",
summary="API to list down the user status in the add user dropdown"
)
def get_user_status():
    try:
        return JSONResponse(content=user_status_list,status_code=200)
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting the User Status",status_code=500)


@router.get('/get_user_account_type',responses={
    200:{"model":str},
    500:{"model":str}
},
summary="API to get the user account type dropdown",
description="API to get the user account type dropdown"
)
def get_user_account_type():
    try:
        return JSONResponse(content=user_account_type_list,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting the user account type",status_code=500)