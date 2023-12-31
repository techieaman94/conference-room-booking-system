from crbs.utils import get_current_datetime_ist
import re


def validate_duration(from_datetime_obj, to_datetime_obj, check_future_duration=False):
    if from_datetime_obj >= to_datetime_obj:
        raise ValueError(
            "Invalid duration, start datetime should be less than end of duration!"
        )
    if check_future_duration and from_datetime_obj <= get_current_datetime_ist():
        raise ValueError("Invalid duration, start datetime should be in future!")


def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        raise ValueError("Invalid email id!")
