from datetime import datetime

from app.schema.atom_schema import AddAtomRequestSchema, GetAtomResponseSchema, BaseSchema


class NcmDeviceId(BaseSchema):
    ncm_device_id: int


class AddNcmRequestSchema(AddAtomRequestSchema):
    status: str


class EditNcmRequestSchema(AddNcmRequestSchema):
    ncm_device_id: int
    atom_id: int
    status: str


class GetAllNcmResponseSchema(GetAtomResponseSchema):
    ncm_device_id: int
    status: str
    backup_status: str | None = None
    password_group: str


class GetAtomInNcmResponseSchema(BaseSchema):
    atom_id: int
    ip_address: str
    device_name: str
    device_type: str
    password_group: str
    vendor: str | None = None
    function: str


class NcmAlarmSchema(BaseSchema):
    ip_address: str
    device_name: str
    alarm_category: str
    alarm_title: str
    alarm_description: str
    alarm_status: str
    creation_date: datetime
    modification_date: datetime
    resolve_remarks: str | None
    mail_status: str
    date : str
    time : str


class NcmConfigHistorySchema(BaseSchema):
    ncm_history_id: int
    date: datetime
    file_name: str


class SendCommandRequestSchema(NcmDeviceId):
    cmd: str



class Response200(BaseSchema):
    data: dict
    message: str

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class RestoreConfigurationSchema(BaseSchema):
    ip_address: str
    date:str

class GetTrueBackup(BaseSchema):
    ncm_device_id:int
    status:str | None = None
    confg_change_date:str | None = None
    ip_adderss:str |None = None

class CompareBackupSchema(BaseSchema):
    ncm_history_id_1:int
    ncm_history_id_2:int

class GetDeviceConfigurationById(BaseSchema):
    ncm_device_id:int

class GetDeviceConfigurationByHistory(BaseSchema):
    ncm_history_id:int

class NcmDeletedConfigurationSchema(BaseSchema):
    ncm_device_id:int


class NCMBackupSummaryConfiguration(BaseSchema):
    backup_successful:int
    backup_failure:int
    not_backup:int


class GetNcmDecivesCountByFucntionSchema(BaseSchema):
    device_type:str
    function:str
    vendor:str
    device_count:int

class GetNcmAlarmCategoryGraph(BaseSchema):
    name:str
    vlaue: int
    total_count:int | None = None

class GetNcmVendorSchema(BaseSchema):
    name: list[str]
    config_change_time : list[str] 
    config_date : list[str]
    value : list[int]

class DeviceType(BaseSchema):
    name : str
    value : int    