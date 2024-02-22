import traceback
import sys
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.responses import JSONResponse
from app.core.container import Container
from app.core.dependencies import get_current_active_user
from app.models.users_models import UserTableModel as User
from app.schema.auth_schema import SignIn, SignUp, SignInResponse, SignInNew,VerifyAccessTokenResponseSchema
from app.schema.users_schema import User as UserSchema
from app.services.auth_service import AuthService
# from fastapi.status import HTTP_204_NO_CONTENT
from app.core.security import JWTBearer
from app.api.v1.users.utils.user_utils import add_end_user_registration



from app.core.security import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign_in", responses={
    200:{"model":SignInResponse},
    400:{"model":str},
    500:{"model":str}
})
@inject
async def sign_in(user_info: SignInNew, service: AuthService = Depends(Provide[Container.auth_service])):
    try:
        result =  service.sign_in(user_info)
        print("result in sign in for serivxw is:::",result,file=sys.stderr)
        return result
    except Exception as e:
        traceback  .print_exc()

@router.post("/sign_up",  responses = {
                    200:{"model":UserSchema},
                    400:{"model":str},
                    500:{"model":str}
                  },)
@inject
async def sign_up(user_info: SignUp
                  ,service: AuthService = Depends(Provide[Container.auth_service])):
    try:
        print("user infor for signup is::::::::::::",user_info,file=sys.stderr)
        #print("provider is::::",Provide,file=sys.stderr)
        return service.sign_up(user_info)
    except Exception as e :
        traceback.print_exc()
        return JSONResponse(content="Error Occured while Sign in ",status_code=500)

@router.get("/me", response_model=UserSchema)
@inject
async def get_me(current_user: User = Depends(get_current_active_user)):
    user = UserSchema()
    user.name = current_user.name
    user.email = current_user.email
    user.created_at = current_user.created_at
    user.updated_at = current_user.updated_at
    user.is_active = current_user.is_active
    user.is_superuser = current_user.is_superuser
    user.id = current_user.id
    return user


@router.post("/sign_out")
@inject
async def sign_out(
        current_user: User = Depends(get_current_active_user),
        service: AuthService = Depends(Provide[Container.auth_service]),
        token: str = Depends(JWTBearer())):
    try:
        service.blacklist_token(current_user.email, token)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logout successfully"})
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.post('/validate_sign_in_token',responses={
    200:{"model":SignInResponse},
    400:{"model":str},
    500:{"model":str}
},
summary="API to validate the sign in token",
description="API to validate the signin token"
)
def validate_sign_in_token(token:VerifyAccessTokenResponseSchema):
    try:
        print("token is:::::::::::::::::",token,file=sys.stderr)
        data = {}
        jwt_token = token.access_token
        print("jwt token is:::::::::::::::::::::::::::",jwt_token,file=sys.stderr)
        status = JWTBearer.verify_jwt(jwt_token)
        print("staus is:::::::::::::::::::::::::",status,file=sys.stderr)
        if status:
            data["data"] ={
                "access_token": status
            }
            data['message'] = f"Token validated"
        else:
            data["data"] = {
                "access_token": status
            }
            data['message'] = f"Token Not Invalidated"
        return JSONResponse(content=data,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured while validating the sign in token",status_code=500)