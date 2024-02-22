from app.api.v1.atom.utils.atom_utils import *
from app.schema.atom_schema import *
from app.schema.atom_schema import AddPasswordGroupRequestSchema
router = APIRouter(
    prefix="/password_group",
    tags=["password_group"],
)


@router.post("/add_password_group", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def add_passwords_group(pass_obj: AddPasswordGroupRequestSchema):
    try:
        print("pass obj is::::::::::::::::::::::::::::::::::::::",pass_obj,file=sys.stderr)
        pass_obj = pass_obj.dict()

        response, status = add_password_group_util(pass_obj, False)
        print("response is:::::::::::::::::::::::::::::::::::::::::::::::::",file=sys.stderr)
        print("status is:::::::::::::::::::::::::::::::::::::::::::",status,file=sys.stderr)
        if status == 200:
            print("reponse if status is 200 is::::::::::::::::::::::::::::::::::::::::::::::::",response,file=sys.stderr)
            return JSONResponse(content=response, status_code=200)
        elif status == 400:
            print("if status is 400 ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::",response,file=sys.stderr)
            return JSONResponse(content=response, status_code=400)

        
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Password Group", status_code=500)


@router.post("/add_password_groups", responses={
    200: {"model": SummeryResponseSchema},
    500: {"model": str}
})
async def add_password_groups(pass_list: list[AddPasswordGroupRequestSchema]):
    try:
        print("passwprd list is::::::::::::::::::::::::::::::::::::::::::::",pass_list,file=sys.stderr)
        success_list = []
        error_list = []
        data_lst = []
        for pass_obj in pass_list:
            pass_obj = pass_obj.dict()

            msg, status = add_password_group_util(pass_obj, True)
            # print("message in fields ossssssssssss:::::::::::::::::::::::",msg,file=sys.stderr)
            # print("status is::::::::::::::::::::::",status,file=sys.stderr)
            if status == 200:
                for key,value in msg.items():
                                # print("key for msg ares::::::::::::::::::::",key,file=sys.stderr)
                                # print("values are:::::::::::::::::::::::::::::",value,file=sys.stderr)

                                if key =='data':
                                    data_lst.append(value)
                                if key == 'message':
                                    if value not in success_list:
                                        # print("values for the message is::::::::::::::::::::::",value,file=sys.stderr)
                                        success_list.append(value)
                    
                # success_list.append(msg)
            else:
                error_list.append(msg)

        response = SummeryResponseSchema(
            data = data_lst,
            success=len(success_list),
            error=len(error_list),
            success_list=success_list,
            error_list=error_list
        )

        return response
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Adding Password Groups", status_code=500)


@router.post("/edit_password_group", responses={
    200: {"model": Response200},
    400: {"model": str},
    500: {"model": str}
})
async def edit_password_group(pass_obj: EditPasswordGroupRequestSchema):
    try:
        pass_obj = pass_obj.dict()

        response, status = edit_password_group_util(pass_obj)
        print("status ===============================================",status,file=sys.stderr)
        if status == 200:
            return JSONResponse(response,status_code=200)
        elif status == 400:
            return JSONResponse(response,status_code=400)

        # return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Updating Password Group", status_code=500)


@router.post("/delete_password_group", responses={
    200: {"model": ListtDeleteResponseSchema},
    400:{"model":str},
    500: {"model": str}
})
async def delete_password_groups(pass_list: list[int]):
    try:

        success_list = []
        error_list = []
        deleted_password_group = []
        default_password = configs.db.query(PasswordGroupTable).filter(PasswordGroupTable.password_group == "default_password").first()
        print("password list is:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::",pass_list,file=sys.stderr)
        for pass_obj in pass_list:
            pass_obj = pass_obj
            print("password obj is::::::::::::::::::::::::::::",pass_obj,file=sys.stderr)
            passworg_grp_id = pass_obj
            print("password group id for deletion::::::::::::::::::::::::::::::::::::::::::::::::",passworg_grp_id,file=sys.stderr)
            deleted_passw_group = {}
            password = configs.db.query(PasswordGroupTable).filter(
                    PasswordGroupTable.password_group_id == pass_obj).first()
            print("password is:::::::::::::::::::::::::::::::::::::",password,file=sys.stderr)
            if password.password_group_id == default_password.password_group_id:
                error_list.append(f"{password.password_id} : defualt password cannot be deleted ")
            print("is passsowrd is true::::::::::",file=sys.stderr)
            password_id = password.password_group_id
            print("password id is:::::::::::::::",password_id,file=sys.stderr)
            password_asssociated_with_atom = configs.db.query(AtomTable).filter_by(password_group_id = password_id).first()
            print("password group associated with the atom::::::::::::::::::::::::",password_asssociated_with_atom,file=sys.stderr)
            if password_asssociated_with_atom:
                error_list.append(f"{password.password_group} : Cannot be deleted it is associated with device {password_asssociated_with_atom.ip_address}")
            else:           
                if password:
                    deleted_password_group_id = password.password_group_id
                    print("delted password id is:::::::::::::::::::::::::::::::::::::::",deleted_password_group_id,file=sys.stderr)

                    if DeleteDBData(password) == 200:
                        deleted_password_group.append(deleted_password_group_id)
                    
                        # deleted_password_group.append(deleted_passw_group)
                        success_list.append(
                            f"{password.password_group} : Password Group Deleted Successfully")
                        
                    else:
                        error_list.append(
                            f"{password.password_group} : Error While Deleting Password Group")
                else:
                    error_list.append(f"{passworg_grp_id} : Password Group ID Not Found")

        response = {
            "data":deleted_password_group,
            "success": len(success_list),
            "error": len(error_list),
            "success_list": success_list,
            "error_list": error_list
        }

        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Deleting Password Groups",
                            status_code=500)


@router.get("/get_password_groups", responses={
    200: {"model": list[GetPasswordGroupResponseSchema]},
    500: {"model": str}
})
async def get_password_groups():
    try:
        response = list()
        results = configs.db.query(PasswordGroupTable).all()
        for result in results:
            response.append(result.as_dict())

        # Sort non-default passwords, handling None in creation_date
        non_default_sorted = sorted(
            (x for x in response if x['password_group'] != 'default_password'),
            key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%d %H:%M:%S') if x['creation_date'] else datetime.min,
            reverse=True
        )

        # Sort 'default_password' groups and place them at the beginning
        default_passwords = [x for x in response if x['password_group'] == 'default_password']
        sorted_list = default_passwords + non_default_sorted
        print("sorted list is::::::::::::::::::::::",sorted_list,file=sys.stderr)
        return JSONResponse(content=sorted_list, status_code=200)
    except Exception:
        configs.db.rollback()
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Password Groups",
                            status_code=500)

@router.get("/get_password_group_dropdown", responses={
    200: {"model": list[str]},
    500: {"model": str}
})
async def get_password_group_dropdown():
    try:
        response = list()
        results = configs.db.query(PasswordGroupTable).all()
        for result in results:
            response.append(result.password_group)

        return JSONResponse(content=response, status_code=200)
    except Exception:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Fetching Password Groups Dropdown",
                            status_code=500)
