from getpass import getpass

from colorama import Fore, Style

from crbs.admin_functionalities import (
    add_new_floor,
    add_rooms_to_existing_floor,
    register_new_organization,
    register_new_user,
)
from crbs.constants import (
    CHOICE_PROMPT,
    HOME_SCREEN_SEPARATOR,
    INVALID_CHOICE_MESSAGE,
    INVALID_LOGIN_DETAILS,
    SEPARATOR,
    VALUE_PROMPT,
)
from crbs.user_functionalities import (
    cancel_a_booking,
    find_and_book_suitable_room,
    show_all_bookings,
    show_available_rooms,
)
from crbs.utils import login_and_get_user_id, prompt_other_choices


def admin_home_screen(admin_id):
    print(f"\n{SEPARATOR}")
    print(
        Fore.GREEN + "\t\t\tCONFERENCE ROOM BOOKING SYSTEM [ ADMIN PORTAL ]",
        Style.RESET_ALL,
    )
    print(f"{SEPARATOR}")
    print(CHOICE_PROMPT)
    print("\t\t\t 1 Add new floor")
    print("\t\t\t 2 Add room to existing floor")
    print("\t\t\t 3 Register new organization")
    print("\t\t\t 4 Register new user for an organization")
    prompt_other_choices()
    try:
        choice = int(input(VALUE_PROMPT))
        if choice == 1:
            add_new_floor(admin_id)
        elif choice == 2:
            add_rooms_to_existing_floor(admin_id)
        elif choice == 3:
            register_new_organization(admin_id)
        elif choice == 4:
            register_new_user(admin_id)
        elif choice == 9:
            home_screen()
        elif choice == 0:
            exit()
        else:
            print(INVALID_CHOICE_MESSAGE)
    except Exception as e:
        print(Fore.RED + f"\n\t\t\tException occurred:", Style.RESET_ALL, e)
    admin_home_screen(admin_id)


def normal_user_home_screen(user_id):
    print(f"\n{SEPARATOR}")
    print(
        Fore.GREEN + "\t\t\tCONFERENCE ROOM BOOKING SYSTEM [ USER PORTAL ]",
        Style.RESET_ALL,
    )
    print(SEPARATOR)
    print(CHOICE_PROMPT)
    print("\t\t\t 1 List available conference room")
    print("\t\t\t 2 Find and book a suitable room")
    print("\t\t\t 3 Cancel an existing booking")
    print("\t\t\t 4 See all booking for your organization")
    prompt_other_choices()
    try:
        choice = int(input(VALUE_PROMPT))

        if choice == 1:
            show_available_rooms()
        elif choice == 2:
            find_and_book_suitable_room(user_id)
        elif choice == 3:
            cancel_a_booking(user_id)
        elif choice == 4:
            show_all_bookings(user_id)
        elif choice == 9:
            home_screen()
        elif choice == 0:
            exit()
        else:
            print(INVALID_CHOICE_MESSAGE)
    except Exception as e:
        print(Fore.RED + f"\n\t\t\tException occurred:", Style.RESET_ALL, e)
    normal_user_home_screen(user_id)


def login_screen(admin=False):
    title, format_value = "\t\t\t\t\t{} LOGIN PORTAL", "USER"
    format_value = "ADMIN" if admin else "USER"
    print(f"\n{SEPARATOR}")
    print(title.format(format_value))
    print(f"{SEPARATOR}")
    email_id = input("\t\t\tEnter your email id : ")
    password = getpass(prompt="\t\t\tEnter your password : ")
    user_id = login_and_get_user_id(email_id, password, admin)
    if user_id == -1:
        print(Fore.RED + INVALID_LOGIN_DETAILS, Style.RESET_ALL)
        login_screen(admin)
    else:
        print(
            Fore.GREEN + "\n\t\t\tYou have successfully logged in (^_^)",
            Style.RESET_ALL,
        )
        if admin:
            admin_home_screen(user_id)
        else:
            normal_user_home_screen(user_id)


def home_screen():
    print(f"\n{HOME_SCREEN_SEPARATOR}")
    print("\t\t\t\t\tCONFERENCE ROOM BOOKING SYSTEM")
    print(f"{HOME_SCREEN_SEPARATOR}")
    print(CHOICE_PROMPT)
    print("\t\t\t 1 Admin login")
    print("\t\t\t 2 User login")
    print("\t\t\t 0 to Exit")
    try:
        choice = int(input(VALUE_PROMPT))

        if choice == 1:
            login_screen(True)
        elif choice == 2:
            login_screen()
        elif choice == 0:
            exit()
        else:
            print(INVALID_CHOICE_MESSAGE)
            home_screen()
    except Exception as e:
        print(Fore.RED + f"\n\t\t\tException occurred:", Style.RESET_ALL, e)
    home_screen()
