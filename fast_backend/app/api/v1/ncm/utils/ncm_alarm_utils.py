from app.models.ncm_models import *
from app.utils.db_utils import *


def insert_login_alarm(atom, ncm):
    alarm_description = (
            "1. The credentials (username or password) on the device have been changed\n"
            + "2. Credentials have not been added or updated in MonetX\n"
            + "3. Number of connections to the device have been exceeded and monetX is "
              "unable to connect"
    )

    alarm = NCM_Alarm_Table()
    alarm.ncm_device_id = ncm.ncm_device_id
    alarm.alarm_category = "Login"
    alarm.alarm_title = "Login Failed"
    alarm.alarm_description = alarm_description

    if InsertDBData(alarm):
        print(
            f"NCM Login Alarm: {atom.ip_address} : Login Alarm Added",
            file=sys.stderr,
        )
    else:
        print(
            f"NCM Login Alarm: {atom.ip_address} : Error : While Adding Login Alarm",
            file=sys.stderr,
        )


def update_login_alarm(atom, ncm, login, alarm):
    current_time = datetime.now()
    if login is False:

        difference = current_time - alarm.modification_date
        difference = int(difference.total_seconds())

        if difference >= 86400:  # seconds in a day

            alarm.mail_status = 'no'
            alarm.modification_date = current_time

            if UpdateDBData(alarm) == 200:
                print(
                    f"NCM Login Alarm: {atom.ip_address} : Login Alarm Updated",
                    file=sys.stderr,
                )
            else:
                print(
                    f"NCM Login Alarm: {atom.ip_address} : Error : While Updating Login Alarm",
                    file=sys.stderr,
                )
        else:
            print(
                f"NCM Login Alarm: {atom.ip_address} : Time Difference {difference} < 1 day",
                file=sys.stderr,
            )

    else:
        alarm.resolve_remarks = 'Successfully Logged Into The Device'
        alarm.alarm_status = 'Close'
        if UpdateDBData(alarm) == 200:
            print(
                f"NCM Login Alarm: {atom.ip_address} : Login Alarm Closed",
                file=sys.stderr,
            )
        else:
            print(
                f"NCM Login Alarm: {atom.ip_address} : Error : While Closing Login Alarm",
                file=sys.stderr,
            )


def login_alarm(atom, ncm, login):
    print(
        f"NCM Login Alarm: {atom.ip_address} : Checking Login Alarm...",
        file=sys.stderr,
    )
    try:
        result = configs.db.query(NCM_Alarm_Table).filter(
            NCM_Alarm_Table.ncm_device_id == ncm.ncm_device_id,
            NCM_Alarm_Table.alarm_category == "Login",
            NCM_Alarm_Table.alarm_status == "Open",
        ).first()

        if result is None:
            print(
                f"NCM Login Alarm: {atom.ip_address} : No Open Login Alarm Found",
                file=sys.stderr,
            )

            if login is False:
                insert_login_alarm(atom, ncm)
                print("LOGIN ALARAM inserted login is false:::::::::::::::::::::::",file=sys.stderr)

        else:
            print(
                f"NCM Login Alarm: {atom.ip_address} : Open Login Alarm Found",
                file=sys.stderr,
            )
            update_login_alarm(atom, ncm, login, result)

    except Exception:
        print(
            f"NCM Login Alarm: {atom.ip_address} : Error : While Checking Login Alarm",
            file=sys.stderr,
        )


def insert_config_change_alarm(atom, ncm):
    alarm = NCM_Alarm_Table()
    alarm.ncm_device_id = ncm.ncm_device_id
    alarm.alarm_category = "Configuration"
    alarm.alarm_title = "Configuration Change Detected"
    alarm.alarm_description = (
        f"Change in device configuration has been detected at {ncm.config_change_date}"
    )

    if InsertDBData(alarm) == 200:
        print(
            f"NCM Config Alarm: {atom.ip_address} : Config Alarm Added", file=sys.stderr
        )
    else:
        print(
            f"NCM Config Alarm: {atom.ip_address} : Error while Adding Config Alarm",
            file=sys.stderr,
        )


def backup_failed_alarm(host, backup):
    try:
        pass
    except Exception:
        pass


def config_change_alarm(atom, ncm):
    print(
        f"NCM Config Alarm: {atom.ip_address} : Checking Config Alarm...",
        file=sys.stderr,
    )
    try:
        insert_config_change_alarm(atom, ncm)

    except Exception:
        print(
            f"NCM Config Alarm: {atom.ip_address} : Error : While Checking Config Alarm",
            file=sys.stderr,
        )
