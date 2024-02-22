import datetime
import sys
import traceback


def FormatStringDate(date):
    print(date, file=sys.stderr)

    try:
        if date is not None:
            if '-' in date:
                result = datetime.strptime(date, '%d-%m-%Y')
            elif '/' in date:
                result = datetime.strptime(date, '%d/%m/%Y')
            else:
                print("incorrect date format", file=sys.stderr)
                result = datetime(2000, 1, 1)
        else:
            # result = datetime(2000, 1, 1)
            result = datetime(2000, 1, 1)
    except:
        result = datetime(2000, 1, 1)
        traceback.print_exc()
        print("date format exception", file=sys.stderr)

    return result
#API for date format for GET methods
def FormatDate(date):
    try:
        # print(date, addIosTrackerfile=sys.stderr)
        if date is not None:
            result = date.strftime('%d-%m-%Y')
        else:
            # result = datetime(2000, 1, 1)
            result = datetime(1, 1, 2000)

        return result
    except Exception as e:
        traceback.print_exc()