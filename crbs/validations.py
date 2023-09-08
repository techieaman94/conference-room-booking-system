from crbs.utils import get_current_datetime_ist


def validate_duration(from_datetime_obj, to_datetime_obj, check_future_duration=False):
    if from_datetime_obj >= to_datetime_obj:
        raise ValueError(
            "Invalid duration, start datetime should be less than end of duration!"
        )
    if check_future_duration and from_datetime_obj <= get_current_datetime_ist():
        raise ValueError("Invalid duration, start datetime should be in future!")
