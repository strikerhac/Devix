import sys
import traceback

from app.core.config import *


def InsertDBData(obj):
    try:
        configs.db.add(obj)
        configs.db.commit()
        return 200
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        print(
            f"Something else went wrong in Database Insertion: {e}", file=sys.stderr)
        return 500


def UpdateDBData(obj):
    try:
        configs.db.flush()

        configs.db.merge(obj)
        configs.db.commit()
        return 200
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        print(
            f"Something else went wrong during Database Update: {e}", file=sys.stderr)
        return 500


def DeleteDBData(obj):
    try:
        configs.db.delete(obj)
        configs.db.commit()
        return 200
    except Exception as e:
        configs.db.rollback()
        traceback.print_exc()
        print(
            f"Something else went wrong during Database Delete: {e}", file=sys.stderr)
        return 500
