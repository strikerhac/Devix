from app.schema.base_schema import *


class AddAtomRequestSchema(BaseSchema):
    ip_address: str

    device_name: str | None = None
    device_type: str | None = None
    function: str | None = None
    site_name: str | None = None
    rack_name: str | None = None
    password_group: str | None = None

    vendor: str | None = None
    device_ru: int | None = None
    department: str | None = None
    section: str | None = None
    criticality: str | None = None
    domain: str | None = None
    virtual: str | None = None

    @validator('device_ru', pre=True, always=True)
    def validate_device_ru(cls, v):
        if v == "":
            return None
        return v

class EditAtomRequestSchema(AddAtomRequestSchema):
    atom_id: int | None = None
    atom_transition_id: int | None = None


class GetAtomResponseSchema(BaseSchema):
    atom_id: int = Field(None, title="Atom ID", description="ID for Atom Record")
    atom_transition_id: int = Field(None, title="Transition Atom ID", description="ID for "
                                                                                  "Transition "
                                                                                  "Atom Record")
    ip_address: str
    status: int
    message: str

    device_name: str | None = None
    device_type: str | None = None
    function: str | None = None
    site_name: str | None = None
    rack_name: str | None = None
    password_group: str | None = None

    vendor: str | None = None
    device_ru: int | None = None
    department: str | None = None
    section: str | None = None
    criticality: str | None = None
    domain: int | None = None
    virtual: str | None = None
    onboard_status: bool | None = None

    creation_date: str
    modification_date: str


class DeleteAtomRequestSchema(BaseSchema):
    atom_id: int | None = None
    atom_transition_id: int | None = None


class PasswordGroupTypeEnum(str):
    ssh = "SSH"
    telnet = "Telnet"


class AddPasswordGroupRequestSchema(BaseSchema):
    password_group: str
    username: str
    password: str
    secret_password: str | None = None
    password_group_type: PasswordGroupTypeEnum


class EditPasswordGroupRequestSchema(AddPasswordGroupRequestSchema):
    password_group_id: int


class GetPasswordGroupResponseSchema(BaseSchema):
    password_group_id: int
    password_group: str
    username: str
    password: str
    secret_password: str | None = None
    password_group_type: PasswordGroupTypeEnum

    creation_date: str
    modification_date: str


class DeletePasswordGroupRequestSchema(BaseSchema):
    password_group_id: int
