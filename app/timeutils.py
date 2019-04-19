from dateutil.parser import parse as datetime_parse
from datetime import datetime, timedelta

def parse_date_or_get_default(to_parse: str, default: datetime = datetime.now()) -> datetime:
    try:
        return datetime_parse(to_parse)
    except (ValueError, TypeError):
        return default


def one_month_ago() -> datetime:
    return datetime.now() - timedelta(days=30)


def to_minutes(runtime: timedelta) -> float:
    return runtime / timedelta(minutes=1)


def to_hours(runtime: timedelta) -> float:
    return runtime / timedelta(hours=1)


