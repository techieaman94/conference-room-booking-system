from crbs.utils import get_user_details


def check_if_user_allowed_to_book_room(user_id):
    user_permissions = get_user_details(user_id)["permissions"]
    if 7 in user_permissions:
        return True
    return False


def check_if_user_allowed_to_see_all_bookings(user_id):
    user_permissions = get_user_details(user_id)["permissions"]
    if 8 in user_permissions:
        return True
    return False
