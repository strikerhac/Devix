import sys
import traceback
from app.models.common_models import *
from app.utils.db_utils import *


def addFailedDevice(ip, date, device_type, failure_reason, module):
    failed = FailedDevicesTable()
    failed.ip_address = ip
    failed.date = date
    failed.device_type = device_type
    failed.failure_reason = failure_reason
    failed.module = module
    if configs.db.query().with_entities(FailedDevicesTable.ip_address).filter_by(ip_address=ip) is not None:

        print("Updated "+ip, file=sys.stderr)
        InsertDBData(failed)
    else:
        print("Inserted ", ip, file=sys.stderr)
        UpdateDBData(failed)