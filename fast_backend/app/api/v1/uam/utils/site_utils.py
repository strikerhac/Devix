from app.models.atom_models import *
from app.models.site_rack_models import *
from app.utils.db_utils import *
from sqlalchemy import and_
from geopy.geocoders import Nominatim

def FormatDate(date):
    result = datetime(2000, 1, 1)
    try:
        result = date.strftime("%d-%m-%Y")
    except Exception:
        traceback.print_exc()

    return result




def check_site_name(site_obj):
    site_obj["site_name"] = site_obj["site_name"].strip()

    if site_obj["site_name"] == "":
        return "Site Name Can Not Be Empty", 400

    if site_obj["site_name"].lower() == "default_site":
        return "Site Name (default_site) Is Not Allowed", 400

    site_exist = configs.db.query(SiteTable).filter(
        SiteTable.site_name == site_obj["site_name"]).first()

    return site_exist, 200


def check_site_status(site_obj):
    site_obj["status"] = str(site_obj["status"]).strip().title()

    if site_obj["status"] == "":
        return "Status Must Be Defined (Production / Not Production)", 400

    if site_obj["status"] != "Production" and site_obj["status"] != "Not Production":
        return "Status Must Be Defined (Production / Not Production)", 400

    return site_obj["status"], 200


def check_site_optional_data(site_obj, site_exist):
    site_obj = dict(site_obj)
    print("site obj is:::::::::::::::::::::::::",site_obj,file=sys.stderr)
    if "region" in site_obj.keys():
        if site_obj["region"] is not None:
            site_exist.region_name = site_obj["region"]

    if "city" in site_obj.keys():
        if site_obj["city"] is not None:
            site_exist.city = site_obj["city"]

    if "longitude" in site_obj.keys():
        if site_obj["longitude"] is not None:
            site_exist.longitude = site_obj["longitude"]

    if "latitude" in site_obj.keys():
        if site_obj["latitude"] is not None:
            site_exist.latitude = site_obj["latitude"]

    return site_exist


def add_site_util(site_obj):
    try:
        print("site obj is:::::::::::::::::",site_obj,file=sys.stderr)
        site_group_data = {}
        site_exist, status = check_site_name(site_obj)

        if status == 400:
            return site_exist, status

        if site_exist is not None:
            return "Site Name Is Already Assigned", 400



        site_exist = SiteTable()
        site_exist.site_name = site_obj["site_name"]

        site_status, status = check_site_status(site_obj)
        if status != 200:
            return site_status, status

        site_exist.status = site_status

        site_exist = check_site_optional_data(site_obj, site_exist)

        status = InsertDBData(site_exist)
        if status == 200:
            msg = "Site Inserted Successfully"
            site_data = dict(site_obj)
            site_data['site_id'] = site_exist.site_id
            site_group_data = {
                    "data":site_data,
                    "message":msg
            }
        else:
            msg = "Error While Inserting Site"

        return site_group_data,status

    except Exception:
        traceback.print_exc()
        return "Server Error", 500


def edit_site_util(site_obj):
    try:
        site_exist = configs.db.query(SiteTable).filter(
            SiteTable.site_id == site_obj["site_id"]).first()
        default_rack = configs.db.query(RackTable).filter(
            RackTable.rack_name == "default_rack").first()

        if site_exist is None:
            return "Site Does Not Exist", 400

        if site_exist.site_id == default_rack.site_id:
            return "Default Site Is Not Editable", 400

        response, status = check_site_name(site_obj)

        if status != 200:
            return response, status

        if response is not None:
            if response.site_id != site_exist.site_id:
                return "Site Name Is Already Assigned", 400

        site_exist.site_name = site_obj["site_name"]

        site_status, status = check_site_status(site_obj)
        if status != 200:
            return site_status, status

        site_exist.status = site_status
        site_exist = check_site_optional_data(site_obj, site_exist)
        site_id = site_exist.site_id
        site_name = site_exist.site_name
        status = UpdateDBData(site_exist)
        if status == 200:
            site_data = dict(site_obj)
            site_data['site_id'] = site_id
            msg = f"{site_name} : Site Updated Successfully"
            site_data_dict = {
                "data": site_data,
                "message":msg
            }
            return site_data_dict,200
        else:
            msg = f"Error While Updating Site"
            return msg,400

    except Exception:
        traceback.print_exc()
        return "Server Error", 500


def GetAllSites():
    try:
        siteObjList = []
        siteObjs = configs.db.query(SiteTable).all()
        for siteObj in siteObjs:
            siteDataDict = {
                "site_id": siteObj.site_id,
                "site_name": siteObj.site_name,
                "region": siteObj.region_name,
                "longitude": siteObj.longitude,
                "latitude": siteObj.latitude,
                "city": siteObj.city,
                "creation_date": FormatDate(siteObj.creation_date),
                "modification_date": FormatDate(siteObj.modification_date),
                "status": siteObj.status,
            }

            siteObjList.append(siteDataDict)

        return siteObjList, 200
    except Exception:
        traceback.print_exc()
        return "Server Error", 500


def delete_site_util(site_id):
    try:
        site = configs.db.query(SiteTable).filter(SiteTable.site_id == site_id).first()
        default_rack = configs.db.query(RackTable).filter(
            RackTable.rack_name == 'default_rack').first()
        print("site id is:::::::::::::::::::::::::::::::::",site_id,file=sys.stderr)

        site_exsist = configs.db.query(SiteTable).filter_by(site_id = site_id).first()
        if site_exsist:
            print("site exsist is::::::::::::::::::::::::",site_exsist,file=sys.stderr)
            rack_associated_with_site  = configs.db.query(RackTable).filter_by(site_id = site_id).first()
            if rack_associated_with_site:
                return f"{site_exsist.site_name} : Is associate with the rack and cannot be deleted",400
                rack_id_associated_with_site_id = rack_associated_with_site.rack_id
                print("rack associated with the site is true:::",rack_associated_with_site,file=sys.stderr)
                device_associated_with_rack = configs.db.query(AtomTable).filter_by(rack_id = rack_id_associated_with_site_id).first()
                print("device associated with the rack is :::::::::::::::::",device_associated_with_rack,file=sys.stderr)
                if device_associated_with_rack:
                    return f"{site_exsist.site_name} : Is associate with the rack and device and cannot be deleted",400

        if site is None:
            return f"{site_id} : Site Not Found", 400

        if site.site_id == default_rack.site_id:
            return f"{site_id} : Default Site Can Not Be Deleted", 400
        
        # result = configs.db.query(AtomTable).filter(AtomTable.site_id == site_id).first()
        # if result:
        #     return f"{site_id} : Is Associated with device cannot be deleted",400
        site_name = site.site_name



        racks = configs.db.query(RackTable).filter(RackTable.site_id == site_id).all()
        for rack in racks:
            # print("rack is::::::::::::::::::::::::::::::",rack,file=sys.stderr)
            atoms = configs.db.query(AtomTable).filter(AtomTable.rack_id == rack.rack_id).all()
            for atom in atoms:
                atom.rack_id = default_rack.rack_id
                UpdateDBData(atom)

            # DeleteDBData(rack)

        if DeleteDBData(site) == 200:
            deleted_sites = {
                "data":site_id,
                "message" : f"{site_name} : Site Is Deleted Successfully"
            }
            
            return deleted_sites,200
        else:
            return f"{site_name} : Error While Deleting Site", 500

    except Exception:
        traceback.print_exc()
        return f"{site_id} : Exception Occurred While Deleting Site", 500
