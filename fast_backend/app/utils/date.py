from datetime import datetime, timedelta, tzinfo
from threading import Lock
from pytz import timezone


def get_now():
    return datetime.now(tz=timezone("UTC"))







class DateHelper:
    timezone: tzinfo
    def __init__(self, timezone: tzinfo = ...) -> None: ...
    # This returns None in the implementation, but a datetime-compatible
    # object is monkey-patched in at runtime.
    def parse_date(self, date_string: str) -> datetime: ...
    def to_nanoseconds(self, delta: timedelta) -> int: ...
    def to_utc(self, value: datetime) -> datetime: ...
date_helper: DateHelper | None
lock_: Lock
def get_date_helper() -> DateHelper: ...