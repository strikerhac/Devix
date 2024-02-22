from fastapi import FastAPI,APIRouter
from fastapi.responses import JSONResponse
import sys
import traceback
import asyncio
from starlette import status
import ast
from app.models.users_models import *
from app.schema.users_schema import *
from app.core.config import *
from app.utils.db_utils import *
from datetime import datetime
import hashlib
import base64
import json
import asyncio


router = APIRouter(
    prefix="/licenses",
    tags=["licenses"]
)


def Hashing(string):
    try:
        length = 20
        #conversion of string to bytes
        string_bytes = string.encode()
        #use sha256 to create a hash algorithm to create a hash object
        sha256 = hashlib.sha256()
        sha256.update(string_bytes)

        #Get the hexadecimal representiation of the hash
        hex_hash = sha256.hexdigest()
        print("hex hash is::::::::::::::::::::::::::::;",hex_hash,file=sys.stderr)
        #take the first 'length' character of hexadecimal
        short_hash = hex_hash[:length]
        print("short hash is::::::::::::::::;;;;",short_hash,file=sys.stderr)
        return short_hash
    except Exception as e:
        traceback.print_exc()
        print("Error Occurred While License Hashing",str(e),file=sys.stderr)


async def DecodeLicense(license_key):
    try:
        # Decode the base64 encoded data to bytes
        decode_data = base64.b64decode(license_key)
        print("Decoded data type is:", type(decode_data), file=sys.stderr)

        # Convert the decoded bytes to a string
        decoded_string = decode_data.decode()
        print("Decoded string is:", decoded_string, file=sys.stderr)

        # Attempt to parse the decoded string as JSON
        try:
            license_data = json.loads(decoded_string)
        except json.decoder.JSONDecodeError as json_err:
            print("JSON decoding error:", json_err, file=sys.stderr)
            return None

        # Extracting data from the JSON object
        company_name = license_data['company_name']
        start_date = datetime.strptime(license_data['start_date'], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(license_data['end_date'], "%Y-%m-%d %H:%M:%S")

        return {
            "company_name": company_name,
            "start_date": start_date,
            "end_date": end_date
        }

    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
        traceback.print_exc()
        return None


async def LicenseTenure(end_date):
    try:
        from dateutil.relativedelta import relativedelta
        print("end date is::::::::::",end_date,file=sys.stderr)
        str_end_date = str(end_date).split(' ')[0]
        print("str end date is::::::::::::::",str_end_date,file=sys.stderr)
        format_end_date = datetime.strptime(str_end_date, '%Y-%m-%d')
        print("formatted end date is:::::::::::",format_end_date,file=sys.stderr)
        months = float(str_end_date)
        print("months are:::::::::::::::::::",months,file=sys.stderr)
        today = datetime.now()
        date_after_months = today + relativedelta(months=months)
        print("License start date is:::::::::::::::::::::::::::",today,file=sys.stderr)
        print("license will expire on::::::::::::::::::::::::::",date_after_months,file=sys.stderr)
        return date_after_months
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Calculating license tenure",status_code=500)



async def LicenseDaysLeft(date_string):
    try:
        parsed_date = datetime.strptime(str(date_string),"%Y-%m-%d %H:%M:%S")
        print("parsed date is::::::::::::::::",parsed_date,file=sys.stderr)
        #conversion of the parssed date to the desired format is
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        print("formatted date is:::::::::::::::",formatted_date,file=sys.stderr)
        target_date = datetime.strptime(formatted_date,"%y-%m-%d")
        print("target date is:::::::::::::::::",target_date,file=sys.stderr)
        today = datetime.now()
        time_left = target_date - today
        time_left_in_days = time_left.days
        print("day left is:::::::::::::::::",time_left_in_days,file=sys.stderr)
        return time_left_in_days
    except Exception as e:
        traceback.print_exc()






# @router.post('/generate_license',responses={
#     200:{"model":str},
#     400:{"model":str},
#     500:{"model":str}
# },
# summary="API to Generate the license",
# description="API to generate the license"
# )
def generate_license(license_data):
    try:
        print("liscence data is being executed::::::",file=sys.stderr)
        objDict = {}
        license_data = dict(license_data)
        end_user_id = ""
        print("license data is:::::::::::::::::::::", license_data, file=sys.stderr)
        end_user_exsists = configs.db.query(EndUserTable).filter_by(company_name = license_data['company_name']).first()
        if end_user_exsists:
            end_user_id = license_data['end_user_id']
        # Verify required fields
        required_fields = ['company_name', 'start_date', 'end_date', 'device_onboard_limit']
        for field in required_fields:
            if field not in license_data:
                return JSONResponse(content=f"{field} Is Missing", status_code=400)
        start_date_obj = datetime.strptime(license_data['start_date'], '%a, %d %b %Y %H:%M:%S GMT')
        end_date_obj = datetime.strptime(license_data['end_date'], '%a, %d %b %Y %H:%M:%S GMT')
        print("start date obj is::::::::::::::::::::",start_date_obj,file=sys.stderr)
        print("end dateobj is::::::::::::::::::::::::",end_date_obj,file=sys.stderr)

        objDict['company_name'] = license_data['company_name']
        objDict['start_date'] = start_date_obj
        objDict['end_date'] = end_date_obj
        objDict['device_onboard_limit'] = license_data['device_onboard_limit']
        objDict['middleware'] = 'Monetx'
        print("setting attrbute to the object::::::::::::")
        strDict = str(objDict)
        res = bytes(strDict, 'utf-8')
        final = base64.b64encode(res)
        encoded_data = final.decode("utf-8")

        hashedString = Hashing(encoded_data) if asyncio.iscoroutinefunction(Hashing) else Hashing(encoded_data)
        hashDict = {
            "hashed_string": hashedString,
            "encoded_data": encoded_data
        }

        with open("/app/hashFile", "w") as outfile:
            json.dump(hashDict, outfile)
        print("encoded data is:::::::::::::::::::",encoded_data,file=sys.stderr)
        license_tab = LicenseVerfificationModel()
        license_tab.end_user_id = end_user_id
        license_tab.start_date = start_date_obj
        license_tab.end_date = end_date_obj
        license_tab.license_generate_key = encoded_data
        license_tab.license_verfification_key = encoded_data
        license_tab.device_onboard_limit = license_data['device_onboard_limit']
        license_tab.verification = 'Verified'
        configs.db.add(license_tab)
        configs.db.commit()
        print("Data Inserted to the DB for the license verification", file=sys.stderr)

        data_license = {'encoded': encoded_data}
        return {'encoded': encoded_data}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occurred While Generating License", status_code=500)



@router.post('/decode_license')
async def decoded_license(key:str):
    try:
        objectDict = DecodeLicense(key)
        print("objct dict is::::::",objectDict,file=sys.stderr)
        return objectDict

    except Exception as e:
        traceback.print_exc()


async def liscence_expiry():
    try:
        liscences = configs.db.query(LicenseVerfificationModel).all()
        print("liscences are::::::::::::::::::::::::::",liscences,file=sys.stderr)
        for liscence in liscences:
            liscnece_end_date = liscence.end_date
            current_date = datetime.now()
            if liscnece_end_date < current_date:
                liscence.verfication ='Expired'
                UpdateDBData(liscences)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content="Error Occured While Liscence Expiry",status_code=500)

def check_license_expiration(license_id):
    try:
        # Assuming 'license_id' is the identifier to find the specific license
        license = configs.db.query(LicenseVerfificationModel).filter_by(license_verfification_id=license_id).first()
        if license:
            current_date = datetime.now()
            if license.end_date < current_date:
                license.verfication = 'Expired'
                configs.db.merge(license)
                configs.db.commit()
                print("db updated for liscence vification:::::::::::::::",file=sys.stderr)
                return 'Expired'
            else:
                return "Verified"
        else:
            return 'License Not Found'
    except Exception as e:
        # Handle any exceptions that occur
        print(f"An error occurred: {e}")
        traceback.print_exc()
        return 'Error Checking License'