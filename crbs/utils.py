import threading
from datetime import datetime

import pytz

from crbs.constants import (
    ALLOWED_BOOKING_DURATION_QUOTA,
    EXIT_PROMPT,
    HOME_SCREEN_PROMPT,
)
from crbs.entities import admins, bookings, equipments, rooms, users


def login_and_get_user_id(email_id, password, admin):
    users_list = users
    if admin:
        users_list = admins
    for user in users_list:
        if user["email_id"] == email_id and user["password"] == password:
            return user["id"]
    return -1


def prompt_other_choices():
    print(HOME_SCREEN_PROMPT)
    print(EXIT_PROMPT)


def get_current_datetime_ist():
    return datetime.now(pytz.timezone("Asia/Kolkata"))


def get_datetime_obj_from_str_ist(date_string):
    date_string = f"{date_string} +0530"
    datetime_obj = datetime.strptime(date_string, "%d-%m-%Y %H:%M %z")
    return datetime_obj


def print_items_from_list(entity_type, item_list):
    print(f"\n\t\t\t-------------------{entity_type}------------------------")
    for item in item_list:
        print("\n")
        sorted_dict = sorted(item.items())
        for key, value in sorted_dict:
            print(f"\t\t\t{key} : {value}")


def get_user_details(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None


def add_rooms_to_floor(no_of_rooms, floor_number, admin_id):
    for i in range(no_of_rooms):
        room_name = input(f"\n\t\t\tEnter name for room {i + 1}: ")
        room_capacity = int(input(f"\t\t\tEnter capacity for room {i + 1} : "))
        print(
            "\t\t\tEnter the equipment ids available in the room from followings (comma separated, example : 1,3)"
        )
        for equipment in equipments:
            print(
                "\t\t\t\tID : {}, Name : {}".format(equipment["id"], equipment["name"])
            )
        room_equipments = input("\t\t\tEquipments ids : ")
        room_equipments = ("".join(room_equipments.split())).split(",")
        room_equipments = list(map(int, room_equipments))
        room_id = int(get_current_datetime_ist().timestamp())
        rooms.append(
            dict(
                id=room_id,
                floor_number=floor_number,
                name=room_name,
                capacity=room_capacity,
                equipments=room_equipments,
                added_by=admin_id,
            )
        )
        print(f"\n\t\t\tRoom added, room id : {room_id}")


def show_suitable_rooms(suitable_rooms):
    print(
        f"\n\t\t\t---------------Available conference rooms based on your search-----------------\n"
    )
    for i in range(len(suitable_rooms)):
        room = suitable_rooms[i]
        print(f"\t\t\tserial number : {i + 1}")
        for key, value in room.items():
            print(f"\t\t\t{key} : {value}")
        print("\n")


def get_available_conference_rooms(
    from_datetime_obj_ist, to_datetime_obj_ist, capacity=0, required_equipments=None
):
    if required_equipments is None:
        required_equipments = []
    already_booked_room_ids_set = set()
    for booking in bookings:
        if (
            not (
                from_datetime_obj_ist > booking["to_datetime"]
                or to_datetime_obj_ist < booking["from_datetime"]
            )
            and not booking["cancelled"]
        ):
            already_booked_room_ids_set.add(booking["room_id"])
    available_rooms = [
        room
        for room in rooms
        if room["id"] not in already_booked_room_ids_set
        and capacity <= room["capacity"]
        and set(required_equipments).issubset(set(room["equipments"]))
    ]
    return available_rooms


def get_consumed_booking_durations(organization_id, month):
    current_month_booking_durations_in_seconds = []
    for booking in bookings:
        if (
            booking["organization_id"] == organization_id
            and booking["from_datetime"].month == month
            and not booking["cancelled"]
        ):
            duration_in_seconds = int(
                (booking["to_datetime"] - booking["from_datetime"]).total_seconds()
            )
            current_month_booking_durations_in_seconds.append(duration_in_seconds)
    return sum(current_month_booking_durations_in_seconds)


def get_available_booking_limit_quota(organization_id):
    month = get_current_datetime_ist().month
    consumed_booking_durations_in_seconds = get_consumed_booking_durations(
        organization_id, month
    )
    total_remaining_durations_in_hours = (
        ALLOWED_BOOKING_DURATION_QUOTA - consumed_booking_durations_in_seconds
    ) // 3600
    if total_remaining_durations_in_hours < 0:
        total_remaining_durations_in_hours = 0
    return total_remaining_durations_in_hours


def check_booking_limit(organization_id, from_datetime_obj_ist, to_datetime_obj_ist):
    asked_duration_in_seconds = int(
        (to_datetime_obj_ist - from_datetime_obj_ist).total_seconds()
    )
    month = from_datetime_obj_ist.month
    consumed_booking_durations = get_consumed_booking_durations(organization_id, month)
    if (
        consumed_booking_durations + asked_duration_in_seconds
        > ALLOWED_BOOKING_DURATION_QUOTA
    ):
        total_remaining_durations_in_hours = (
            ALLOWED_BOOKING_DURATION_QUOTA - consumed_booking_durations
        ) // 3600
        if total_remaining_durations_in_hours < 0:
            total_remaining_durations_in_hours = 0
        reason = f"\t\t\tMonthly quota for booking conference room is not enough for your organization!\n\t\t\tAvailable {total_remaining_durations_in_hours} hours!!"
        return False, reason
    else:
        return True, None


def create_booking(booking_details, capacity, required_equipments):
    lock = threading.Lock()
    from_datetime_obj_ist = booking_details["from_datetime"]
    to_datetime_obj_ist = booking_details["to_datetime"]
    with lock:
        available_conference_rooms = get_available_conference_rooms(
            from_datetime_obj_ist, to_datetime_obj_ist, capacity, required_equipments
        )
        available_conference_room_ids = [
            room["id"] for room in available_conference_rooms
        ]
        if booking_details["room_id"] in available_conference_room_ids:
            booking_id = int(get_current_datetime_ist().timestamp())
            booking_details.update({"id": booking_id, "cancelled": False})
            bookings.append(booking_details)
            return True, booking_id
        error_message = "\n\t\t\tSelected conference room is not available!!"
        return False, error_message


def get_booking_details(booking_id):
    booking_details = None
    for booking in bookings:
        if booking["id"] == booking_id:
            booking_details = booking
            break
    return booking_details


def get_bookings(**kwargs):
    from_date = kwargs.get("from_datetime_obj_ist")
    to_date = kwargs.get("to_datetime_obj_ist")
    user_id = kwargs.get("user_id")
    organization_id = kwargs.get("organization_id")
    filtered_bookings = bookings
    if from_date:
        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if booking["from_datetime"] >= from_date
        ]
    if to_date:
        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if booking["to_datetime"] <= to_date
        ]
    if user_id:
        filtered_bookings = [
            booking for booking in filtered_bookings if booking["booked_by"] == user_id
        ]
    if organization_id:
        filtered_bookings = [
            booking
            for booking in filtered_bookings
            if booking["organization_id"] == organization_id
        ]
    return filtered_bookings
