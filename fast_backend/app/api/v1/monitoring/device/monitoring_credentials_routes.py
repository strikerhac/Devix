import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.auto_discovery_models import *
from app.api.v1.monitoring.device.utils.alerts_utils import *
from app.schema.monitoring_schema import *

router = APIRouter(
    prefix="/credentials",
    tags=["monitoring_credentials"]
)


@router.post("/add_snmp_v1_v2_credentials", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def add_snmp_v2_credentials(credential_obj: SnmpV2CredentialsRequestSchema):
    try:
        print("monitoring credentials obj is:::::::::",credential_obj,file=sys.stderr)
        data = {}
        if (configs.db.query(Monitoring_Credentails_Table).filter(
                Monitoring_Credentails_Table.profile_name == credential_obj["profile_name"])
                .first() is not None):
            return JSONResponse(content="Profile Name is Already Assigned",status_code=400)
        else:
            print("Insertion in progress::::::::",file=sys.stderr)
            credential = Monitoring_Credentails_Table()

            credential.category = "v1/v2"
            credential.profile_name = credential_obj["profile_name"]
            credential.snmp_port = credential_obj["port"]
            credential.snmp_read_community = credential_obj["community"]
            credential_obj.description = credential_obj["description"]
            print("Insertion is being executed:::::::",file=sys.stderr)
            InsertDBData(credential)
            print("Data inserted into the DB:::::::::::",file=sys.stderr)
            v1_2_dict = {
                    "monitoring_credentials_id": credential.monitoring_credentials_id,
                    "profile_name": credential.profile_name,
                    "port": credential.snmp_port,
                    "username": credential.username,
                    "password": credential.password,
                    "description":credential.description,
                    "community":credential.snmp_read_community,
                    "category":credential.category
            }
            data['data'] = v1_2_dict
            data['message'] =  f"Inserted {credential.monitoring_credentials_id} Credentials Successfully"
            print(
                    f"Inserted {credential.monitoring_credentials_id} Credentials Successfully",
                    file=sys.stderr,
            )
            print("v1_v2 credential data",v1_2_dict,file=sys.stderr)
            print("data is:::::::::::::::::::::::::::::",data,file=sys.stderr)
            return JSONResponse(content=data, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.post("/add_snmp_v3_credentials", responses={
    200: {"model": str},
    400: {"model": str},
    500: {"model": str}
})
async def add_snmp_v3_credentials(credential_obj: AddMonitoringSnmpV3CredentialsRequestSchema):
    try:
        data = {}
        if (configs.db.query(Monitoring_Credentails_Table).filter(
                Monitoring_Credentails_Table.profile_name == credential_obj["profile_name"])
                .first() is not None):
            return JSONResponse(content="Profile Name Is Already Assigned", status_code=400)
        else:
            credential = Monitoring_Credentails_Table()

            credential.category = "v3"
            credential.profile_name = credential_obj["profile_name"]
            credential.snmp_port = credential_obj["port"]

            if "description" in credential_obj:
                credential_obj.description = credential_obj["description"]

            credential.username = credential_obj["username"]
            credential.password = credential_obj["authorization_password"]
            credential.encryption_password = credential_obj["encryption_password"]
            credential.authentication_method = credential_obj["authorization_protocol"]
            credential.encryption_method = credential_obj["encryption_protocol"]


            if InsertDBData(credential) == 200:
                v3_dict = {
                    "monitoring_credentials_id": credential.monitoring_credentials_id,
                    "profile_name": credential.profile_name,
                    "port": credential.snmp_port,
                    "username": credential.username,
                    "password": credential.password,
                    "encryption_password": credential.encryption_password,
                    "authorization_protocol": credential.authentication_method,
                    "encryption_protocol": credential.encryption_method,
                    "authorization_password":credential.password,
                    "description":credential.description
                }
                data['data'] = v3_dict
                data['message'] =  f"Inserted {credential.monitoring_credentials_id} Credentials Successfully"
                print(
                    f"Inserted {credential.monitoring_credentials_id} Credentials Successfully",
                    file=sys.stderr,
                )
                return JSONResponse(content=data, status_code=200)
            else:
                return JSONResponse(content="Error While Adding Credentials", status_code=500)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get("/get_dev_credentials", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_dev_credentials():
    try:
        results = configs.db.query(Monitoring_Credentails_Table).all()

        response_list = []
        for result in results:
            response_list.append(result.profile_name)

        return JSONResponse(content=response_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error in getting credentials", status_code=500)


@router.get("/get_snmp_v1_v2_credentials", responses={
    200: {"model": list[SnmpV2CredentialsResponseSchema]},
    500: {"model": str}
})
def get_snmp_v2_credentials():
    try:
        credentials_list = []

        results = configs.db.query(Monitoring_Credentails_Table).filter(
            Monitoring_Credentails_Table.category == "v1/v2"
        ).all()

        for monitoring_obj in results:
            print("monitoring obj is::::::::::::::",monitoring_obj,file=sys.stderr)
            credential_obj = {"profile_name": monitoring_obj.profile_name,
                              "description": monitoring_obj.description,
                              "community": monitoring_obj.snmp_read_community,
                              "port": monitoring_obj.snmp_port,
                              "category":monitoring_obj.category,
                              "monitoring_credentials_id": monitoring_obj.monitoring_credentials_id}

            credentials_list.append(credential_obj)
        print("credential_list is:::::::::::",credentials_list,file=sys.stderr)

        return JSONResponse(credentials_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)

@router.post('/add_WMI_credentials',
             responses={
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="use this api to add the WMI credentials",
             description="Use this api to add the WMI credentials"
             )
def add_wmi_credentials(wmiObj:WMIMonitoringCredentialSchema):
    try:
        data_dict_wmi = {}
        wmiObj = dict(wmiObj)
        credentials = Monitoring_Credentails_Table()
        if configs.db.query(Monitoring_Credentails_Table).filter_by(profile_name=wmiObj['profile_name']).first():
            return JSONResponse(content={"message": "Duplicate Entry"}, status_code=400)
        credentials.username = wmiObj['user_name']
        credentials.profile_name = wmiObj['profile_name']
        credentials.password = wmiObj['password']
        credentials.category = "wmi"
        InsertDBData(credentials)
        data_dict = {
            "monitoring_credentials_id":credentials.monitoring_credentials_id,
            "user_name":credentials.username,
            "password":credentials.password,
            "profile_name":credentials.profile_name,
            "category":credentials.category
        }
        data_dict_wmi['data'] = data_dict
        data_dict_wmi['message'] = f"{credentials.profile_name} : Inserted Successfully"

        return JSONResponse(content=data_dict_wmi,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured while adding wmi credentials",status_code=500)



@router.get('/get_WMI_credentials',
            responses={
                200:{"model":list[GetWMIMonitoringCredentialSchema]},
                500:{"model":str}
            },
            summary="Use this API in monitoring credentials to list down WMI credentials",
            description="Use this API in monitoring credentials to list down WMI credentials"
            )
def get_wmi_credentials():
    try:
        wmi_lst = []
        wmiObj = configs.db.query(Monitoring_Credentails_Table).filter_by(category='wmi').all()
        for row in wmiObj:
            wmi_dict = {
            "monitoring_credentials_id":row.monitoring_credentials_id,
            "username":row.username,
            "password":row.password,
            "profile_name":row.profile_name,
            "category":row.category
            }
            wmi_lst.append(wmi_dict)
        return  JSONResponse(content=wmi_lst,status_code=200)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured while getting WMI credentials",status_code=500)



# @app.route("/getWMICredentials", methods=["GET"])
# def WMICredentials():
#     if True:
#         try:
#             MonitoringObjList = []
#
#             queryString = f"select profile_name,username,password,monitoring_credentials_id from monitoring_credentials_table where category='wmi'"
#             results = db.session.execute(queryString)
#
#             for MonitoringObj in results:
#                 MonitoringDataDict = {}
#                 MonitoringDataDict["profile_name"] = MonitoringObj[0]
#                 MonitoringDataDict["username"] = MonitoringObj[1]
#                 MonitoringDataDict["password"] = MonitoringObj[2]
#                 MonitoringDataDict["cred_id"] = MonitoringObj[3]
#
#                 MonitoringObjList.append(MonitoringDataDict)
#
#             return jsonify(MonitoringObjList), 200
#
#         except Exception as e:
#             traceback.print_exc()
#             return "Something Went Wrong!", 500
#     else:
#         print("Service not Available", file=sys.stderr)
#         return jsonify({"Response": "Service not Available"}), 503
#
#
@router.get("/get_snmp_v3_credentials", responses={
    200: {"model": list[SnmpV3CredentialsResponseSchema]},
    500: {"model": str}
})
def get_snmp_v3_credentials():
    try:
        credentials_list = []

        results = configs.db.query(Monitoring_Credentails_Table).filter(
            Monitoring_Credentails_Table.category == "v3"
        ).all()

        for credentials_obj in results:
            credentials_dict = {"profile_name": credentials_obj.profile_name,
                                "username": credentials_obj.username,
                                "description": credentials_obj.description,
                                "port": credentials_obj.snmp_port,
                                "authentication_protocol": credentials_obj.authentication_method,
                                "authentication_password": credentials_obj.password,
                                "encryption_protocol": credentials_obj.encryption_method,
                                "encryption_password": credentials_obj.encryption_password,
                                "credentials_id": credentials_obj.monitoring_credentials_id}
            credentials_list.append(credentials_dict)

        return JSONResponse(credentials_list, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.post("/delete_snmp_credentials", responses={
    200: {"model": DeleteResponseSchema},
    500: {"model": str}
})
async def delete_snmp_credentials(id_list: list[int]):
    try:

        response_list = []
        error_list = []
        data = []
        for id in id_list:
            cred = configs.db.query(Monitoring_Credentails_Table).filter(
                Monitoring_Credentails_Table.monitoring_credentials_id == id).first()
            monitoring_credential_id = cred.monitoring_credentials_id
            if cred is None:
                error_list.append(f"ID {id} : Credentials Not Found")
            else:
                profile = cred.profile_name

                if DeleteDBData(cred) == 200:
                    data.append(monitoring_credential_id)
                    response_list.append(f"{profile} : Deleted Successfully")
                else:
                    error_list.append(f"{profile} : Error While Deleting Credentials")

        response_dict = {
            "data":data,
            "success": len(response_list),
            "error": len(error_list),
            "error_list": error_list,
            "success_list": response_list,
        }

        return JSONResponse(content=response_dict, status_code=200)

    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Server Error", status_code=500)


@router.get('/get_all_monitoring_credentials',responses={
    200:{"model":list[MonitoringCredentialsResponseSchema]},
    500:{"model":str}
},
description="API to get all the SNMP credentials",
summary="API to get all the snmp cerdentials"
)
def get_all_snmp_credentials():
    try:
        credentials_list = []
        credentials = configs.db.query(Monitoring_Credentails_Table).all()
        for credential in credentials:
            print("credentials are:::::::::::::::",credential,file=sys.stderr)
            credentials_dict = {
                "monitoring_credentials_id":credential.monitoring_credentials_id,
                "category":credential.category,
                "profile_name":credential.profile_name,
                "credentials":credential.category+"-"+credential.profile_name
            }
            credentials_list.append(credentials_dict)
        return JSONResponse(content=credentials_list,status_code=200)
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Getting the Monitoring credentials",status_code=500)


@router.post('/edit_snmp_v1_v2_credentials',responses={
    200:{"model":str},
    400:{"model":str},
    500:{"model":str}
},
description="API to edit the  snmp v1_v2 credentials",
summary="API to edit the  snmp v1_v2 credentials"
)
def edit_snmp_v1_v2_credentials(v2_data:EditSnmpV2Credentials):
    try:
        data_dict = {}
        v2_data = dict(v2_data)
        print("v2 data is::::",v2_data,file=sys.stderr)
        v2_exsists = configs.db.query(Monitoring_Credentails_Table).filter_by(monitoring_credentials_id = v2_data['monitoring_credentials_id']).first()
        if v2_exsists:
            v2_exsists.profile_name = v2_data['profile_name']
            v2_exsists.description = v2_data['description']
            v2_exsists.snmp_port = v2_data['port']
            v2_exsists.snmp_read_community = v2_data['community']
            data ={
                "monitoring_credentials_id":v2_exsists.monitoring_credentials_id,
                "profile_name":v2_exsists.profile_name,
                "description":v2_exsists.description,
                "port":v2_exsists.snmp_port,
                "community":v2_exsists.snmp_read_community,
            }
            data_dict['message'] = f"{v2_exsists.profile_name} : Updated Successfully"
            data_dict['data'] = data
            return  data_dict
        else:
            return JSONResponse(content=f"{v2_data['monitoring_credentials_id']} : Not Found",status_code=400)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Updting the SNMP v1_v2 credentials",status_code=500)


@router.post('/edit_snmp_v3_credentials',responses={
    200:{"model":str},
    400:{"model":str},
    500:{"model":str}
},
description="API to edit the  snmp v1_v2 credentials",
summary="API to edit the  snmp v1_v2 credentials"
)
def edit_snmp_v3_credentials(v3_data:MonitoringSnmpV3CredentialsRequestSchema):
    try:
        data_dict = {}
        v3_data = dict(v3_data)
        v3_exsists = configs.db.query(Monitoring_Credentails_Table).filter_by(monitoring_credentials_id = v3_data['monitoring_credentials_id']).first()
        if v3_exsists:
            v3_exsists.username = v3_data['username']
            v3_exsists.authentication_password = v3_data['authorization_password']
            v3_exsists.encryption_password = v3_data['encryption_password']
            v3_exsists.authentication_protocol = v3_data['authorization_password']
            v3_exsists.encryption_protocol = v3_data['encryption_protocol']
            v3_exsists.description = v3_data['description']
            v3_exsists.profile_name = v3_data['profile_name']
            v3_exsists.snmp_port = v3_data['port']
            v3_exsists.username = v3_data['username']
            data ={
                "monitoring_credentials_id": v3_exsists.monitoring_credentials_id,
                    "profile_name": v3_exsists.profile_name,
                    "port": v3_exsists.snmp_port,
                    "username": v3_exsists.username,
                    "password": v3_exsists.password,
                    "encryption_password": v3_exsists.encryption_password,
                    "authorization_protocol": v3_exsists.authentication_method,
                    "encryption_protocol": v3_exsists.encryption_method,
                    "authorization_password":v3_exsists.password,
                    "description":v3_exsists.description
            }
            message = f"{v3_exsists.profile_name} : Updated Successfully"
            data_dict['data'] = data
            data_dict['messgae'] = message

            return data_dict
        else:
            return JSONResponse(content=f"{v3_exsists['credentials_id']} : Not Found",status_code=400)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Updting the SNMP v1_v2 credentials",status_code=500)




@router.post('/edit_WMI_credentials',
             responses={
                 200:{"model":Response200},
                 400:{"model":str},
                 500:{"model":str}
             },
             summary="use this api to add the WMI credentials",
             description="Use this api to add the WMI credentials"
             )
def edit_wmi_credentials(wmiObj:WMIMonitoringCredentialSchema):
    try:
        data_dict_wmi = {}
        wmiObj = dict(wmiObj)
        credentials = configs.db.query(Monitoring_Credentails_Table).filter_by(profile_name=wmiObj['profile_name']).first()
        if credentials:
            credentials.username = wmiObj['username']
            credentials.profile_name = wmiObj['profile_name']
            credentials.password = wmiObj['password']
            credentials.category = "wmi"
            UpdateDBData(credentials)
            data_dict = {
                "monitoring_credentials_id":credentials.monitoring_credentials_id,
                "username":credentials.username,
                "password":credentials.password,
                "profile_name":credentials.profile_name,
                "category":credentials.category
            }
            data_dict_wmi['data'] = data_dict
            data_dict_wmi['message'] = f"{credentials.profile_name} : Updated Successfully"
            return JSONResponse(content=data_dict_wmi,status_code=200)
        else:
            return JSONResponse(content=f"Credentials Not Found",status_code=400)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured while adding wmi credentials",status_code=500)
