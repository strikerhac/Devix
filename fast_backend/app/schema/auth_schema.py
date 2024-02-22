from datetime import datetime
from pydantic import BaseModel
from app.schema.users_schema import *


class SignInNew(BaseModel):
    user_name: str
    password: str


class SignIn(BaseModel):
    # email__eq: Optional[str]
    password: str


class SignUp(BaseModel):
    company:dict
    user:dict
    # email: str
    # password: str
    # name: str
    # role: str
    # status:str
    # team:str
    # account_type:str
    # company_name:str

class Payload(BaseModel):
    user_id: int
    email_address: Optional[str]
    name: str
    is_superuser: bool
    user_role_id :int
    end_user_id:int
    configuration:str
    role:str
    liscence_verification:str

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email_address": self.email_address,
            "name": self.name,
            "is_superuser": self.is_superuser,
            "user_role_id": self.user_role_id,
            "configuration": self.configuration,
            "role": self.role
            # Convert other complex types to basic types if necessary
        }


class SignInResponse(BaseModel):
    data:dict
    message:str


class VerifyAccessTokenResponseSchema(BaseModel):
    access_token:str



