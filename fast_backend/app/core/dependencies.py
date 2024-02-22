from dependency_injector.wiring import Provide, inject
# from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
import sys
from app.core.config import configs
from app.core.container import Container
from app.core.exceptions import AuthError
from app.core.security import ALGORITHM, JWTBearer
from app.models.users_models import UserTableModel as User
from app.schema.auth_schema import Payload
from app.services.user_service import UserService
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import Database
from fastapi.responses import JSONResponse

@inject
def get_current_user(
        token: str = Depends(JWTBearer()),
        service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
        print("token data for the payload is:::::::::::::::",token_data,file=sys.stderr)
    except (jwt.JWTError, ValidationError):
        return JSONResponse(status_code=403, content="Could not validate credentials")
    id = token_data.user_id
    current_user: User = service.get_by_id(id)
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
        token: str = Depends(JWTBearer()),
        service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user


def get_current_super_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role != 'super_admin':
        raise AuthError("Access denied")
    return current_user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role != 'Admin':
        raise AuthError("Access denied")
    return current_user


def get_current_regular_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role != 'user':
        raise AuthError("Access denied")
    return current_user


def get_current_admin_or_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role not in ['admin', 'user']:
        raise AuthError("Access denied")
    return current_user


def get_current_admin_or_super_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role not in ['admin', 'super_admin']:
        raise AuthError("Access denied")
    return current_user


def get_current_admin_or_super_admin_or_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active or current_user.role not in ['admin', 'super_admin', 'user']:
        raise AuthError("Access denied")
    return current_user

def get_db() -> Session:
    with Database(configs.DATABASE_URI).session() as db:
        yield db