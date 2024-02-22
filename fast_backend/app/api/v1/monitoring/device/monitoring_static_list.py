import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.utils.static_list import *

router = APIRouter(
    prefix="/monitoring_static_list",
    tags=["monitoring_static_list"],
)



@router.get('/get_authorization_protocol',responses={
    200:{"model":str},
    500:{"model":str}
},
summary="API to get the autorization protocol",
description="APi to get the autorization protocol"
)
async def get_authorization_protocol():
    try:
        authorization_protocol_list =[
            'MD5',
            'SHA',
            'SHA-256',
            'SHA-512'
        ]
        return JSONResponse(content=authorization_protocol_list,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting Authorization Protocol",status_code=500)



@router.get('/get_encryption_protocol',responses={
    200:{"model":str},
    500:{"model":str}
},
summary="API to ge the encryption protocol",
description="API to get the encryption protocol"
)
def get_encryption_protocol():
    try:
        encryption_protocol_list = [
            'DES',
            '3DES',
            'AES',
            'AES-256',
            'AES-192',
            'AES-128'
        ]
        return JSONResponse(content=encryption_protocol_list,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error OCcured While Getting Encryption Protocol",status_code=500)