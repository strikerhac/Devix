from app.schema.base_schema import *



class AwsCredentialScehma(BaseSchema):
    access_key: str
    secret_access_key : str
    account_label : str

class GetAwsSchema(BaseSchema):
    aws_access_key : str
    account_label :str
    access_type : str
    status : bool

class GetEC2Schema(BaseSchema):
    instance_id : int
    instance_name : str
    region_id : str
    access_key : str
    account_label : str
    monitoring_status : str

class AddEc2Schema(BaseSchema):
    access_key : str
    instance_id : int
    instance_name : str
    region_id : int
    access_key :str

class UpdateEc2Status(BaseSchema):
    instance_id : str

class AWSReloadScehma(BaseSchema):
    aws_access_key : str

class GetEc3Schema(BaseSchema):
    bucket_name : str
    region_id : int
    account_label : str
    monitoring_status : str

class Response200(BaseSchema):
    data: dict
    message: str

class DeleteResponseSchema(BaseSchema):
    data: dict
    success: int
    error: int
    success_list: list[str]
    error_list: list[str]

class GetAllELBSchema(BaseSchema):
    id:int
    load_balancer_name:str
    load_balancer_type:str
    load_balancer_scheme:str
    load_balancer_arn:str
    monitoring_status:str
    acccess_key :str |None = None


class ChangeS3StatusSchema(BaseSchema):
    monitoring_status:str
    bucket_name:str

class ChangeELBStatusSchema(BaseSchema):
    monitoring_status:str
    lb_arn:str

class ChangeEc2StatusSchema(BaseSchema):
    monitoring_status:str
    instanace_id:int