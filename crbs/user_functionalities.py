from datetime import timedelta

from crbs.constants import (
    ACTION_NOT_ALLOWED,
    ALLOWED_CANCELLATION_IN_ADVANCE_MINUTES,
    ALLOWED_CANCELLATION_IN_ADVANCE_SECONDS,
    SEPARATOR,
    VALUE_PROMPT,
    END_DATETIME_PROMPT,
    START_DATETIME_PROMPT,
)
from crbs.entities import equipments
from crbs.permissions import (
    check_if_user_allowed_to_book_room,
    check_if_user_allowed_to_see_all_bookings,
)
from crbs.utils import (
    check_booking_limit,
    create_booking,
    get_available_booking_limit_quota,
    get_available_conference_rooms,
    get_booking_details,
    get_bookings,
    get_current_datetime_ist,
    get_datetime_obj_from_str_ist,
    get_user_details,
    print_items_from_list,
    show_suitable_rooms,
)
from crbs.validations import validate_duration


def show_available_rooms():
    print(f"{SEPARATOR}\n\t\t\tSHOW AVAILABLE ROOMS\n")
    from_datetime = input(START_DATETIME_PROMPT)
    to_datetime = input(END_DATETIME_PROMPT)
    from_datetime_obj_ist = get_datetime_obj_from_str_ist(from_datetime)
    to_datetime_obj_ist = get_datetime_obj_from_str_ist(to_datetime)
    validate_duration(from_datetime_obj_ist, to_datetime_obj_ist, True)
    available_rooms = get_available_conference_rooms(
        from_datetime_obj_ist, to_datetime_obj_ist
    )
    print_items_from_list("Available Rooms", available_rooms)


def find_and_book_suitable_room(user_id):
    print(f"{SEPARATOR}\n\t\t\tFIND SUITABLE ROOMS\n")
    user_details = get_user_details(user_id)
    available_booking_limit = get_available_booking_limit_quota(
        user_details["organization_id"]
    )
    print(
        f"\n\t\t\tAvailable monthly conference room booking quota "
        f"for your organization is : {available_booking_limit} hours"
    )
    from_datetime = input(START_DATETIME_PROMPT)
    to_datetime = input(END_DATETIME_PROMPT)
    from_datetime_obj_ist = get_datetime_obj_from_str_ist(from_datetime)
    to_datetime_obj_ist = get_datetime_obj_from_str_ist(to_datetime) + timedelta(
        seconds=-1
    )
    validate_duration(from_datetime_obj_ist, to_datetime_obj_ist, True)
    capacity = int(input("\t\t\tEnter value for capacity : "))
    print(
        "\t\t\tEnter the required equipment ids from followings (comma separated, example : 1,3)"
    )
    for equipment in equipments:
        print("\t\t\t\tID : {}, Name : {}".format(equipment["id"], equipment["name"]))
    required_equipments = input("\t\t\tValue for equipments ids : ")
    required_equipments = ("".join(required_equipments.split())).split(",")
    required_equipments = list(map(int, required_equipments))
    available_rooms = get_available_conference_rooms(
        from_datetime_obj_ist, to_datetime_obj_ist, capacity, required_equipments
    )
    if not available_rooms:
        print(
            "\t\t\t\tNo rooms available for selected dates. Please try for some other dates/time\n"
        )
        return
    show_suitable_rooms(available_rooms)
    allowed_booking_by_user = check_if_user_allowed_to_book_room(user_id)
    if allowed_booking_by_user:
        booking_allowed, reason = check_booking_limit(
            user_details["organization_id"], from_datetime_obj_ist, to_datetime_obj_ist
        )
        if not booking_allowed:
            print(reason)
        else:
            print(
                f"\t\t\tKindly enter the serial number to book a conference room from above options"
            )
            print("\t\t\t\tEnter 0 to go to main menu\n")
            choice = int(input(VALUE_PROMPT))
            if choice == 0:
                return
            elif choice <= len(available_rooms):
                booking_details = {
                    "room_id": available_rooms[choice - 1]["id"],
                    "from_datetime": from_datetime_obj_ist,
                    "to_datetime": to_datetime_obj_ist,
                    "booked_by": user_id,
                    "organization_id": user_details["organization_id"],
                }
                booked, info = create_booking(
                    booking_details, capacity, required_equipments
                )
                if booked:
                    print(f"\n\t\t\tBooking successful, Booking id is : {info}")
                else:
                    print(
                        f"\n\t\t\tBooking failed, Reason : {info}\n\t\t\tPlease try to book some other room."
                    )


def cancel_a_booking(user_id):
    print(f"{SEPARATOR}\n\t\t\tCANCEL BOOKING\n")
    filters = {"user_id": user_id}
    user_bookings = get_bookings(**filters)
    print_items_from_list("Your booking details", user_bookings)
    booking_id = int(input(f"\n\t\t\tEnter the booking id to cancel a booking : "))
    booking_details = get_booking_details(booking_id)
    now_datetime = get_current_datetime_ist()
    if (
        int((booking_details["from_datetime"] - now_datetime).total_seconds())
        > ALLOWED_CANCELLATION_IN_ADVANCE_SECONDS
    ):
        booking_details.update({"cancelled": True})
        print(f"\n\t\t\tCancellation successful")
    else:
        print(
            f"\n\t\t\tSorry!\n\t\t\tCancellation is allowed before {ALLOWED_CANCELLATION_IN_ADVANCE_MINUTES}"
            f" minutes before the start time of the booking"
        )


def show_all_bookings(user_id):
    print(f"{SEPARATOR}\n\t\t\tLIST ALL BOOKINGS\n")
    from_datetime = input(START_DATETIME_PROMPT)
    to_datetime = input(END_DATETIME_PROMPT)
    from_datetime_obj_ist = get_datetime_obj_from_str_ist(from_datetime)
    to_datetime_obj_ist = get_datetime_obj_from_str_ist(to_datetime) + timedelta(
        seconds=-1
    )
    validate_duration(from_datetime_obj_ist, to_datetime_obj_ist, False)
    print(f"\n\t\t\tEnter 1 to see all bookings done by you")
    print("\t\t\tEnter 2 to see all bookings for your organization")
    print("\t\t\tEnter the user id to see all bookings done by that user")
    integer_value = int(input(VALUE_PROMPT))
    filters = {
        "from_datetime_obj_ist": from_datetime_obj_ist,
        "to_datetime_obj_ist": to_datetime_obj_ist,
    }
    if integer_value == 1:
        filters.update({"user_id": user_id})
        bookings = get_bookings(**filters)
    else:
        allowed = check_if_user_allowed_to_see_all_bookings(user_id)
        if not allowed:
            print(ACTION_NOT_ALLOWED)
            return
        user_org_id = get_user_details(user_id)["organization_id"]
        if integer_value == 2:
            filters.update({"organization_id": user_org_id})
            bookings = get_bookings(**filters)
        else:
            other_user_org_id = get_user_details(integer_value)["organization_id"]
            if (
                user_org_id == other_user_org_id
            ):  # check to see if user belong to same organization
                filters.update({"user_id": integer_value})
                bookings = get_bookings(**filters)
            else:
                print(ACTION_NOT_ALLOWED)
                return
    print_items_from_list("Booking details", bookings)
