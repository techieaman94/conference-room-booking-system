from colorama import Fore, Style

CHOICE_PROMPT = "\n\t\t\tPlease enter your choice from followings\n"
INVALID_CHOICE_MESSAGE = "\n\t\t\tPlease enter a valid choice!\n"
INVALID_LOGIN_DETAILS = "\n\t\t\tPlease enter valid email id and password\n"
VALUE_PROMPT = "\n\t\t\t--> "
HOME_SCREEN_PROMPT = "\n\t\t\t 9 to Logout and go to home screen"
EXIT_PROMPT = "\t\t\t 0 to Exit"
ACTION_NOT_ALLOWED = "\n\t\t\tUser action not allowed!"
ALLOWED_BOOKING_DURATION_QUOTA = 30 * 60 * 60
ALLOWED_CANCELLATION_IN_ADVANCE_MINUTES = 15
ALLOWED_CANCELLATION_IN_ADVANCE_SECONDS = ALLOWED_CANCELLATION_IN_ADVANCE_MINUTES * 60
SEPARATOR = (
    Fore.BLUE
    + "\t\t\t-----------------------------------------------------------------"
    + Style.RESET_ALL
)
HOME_SCREEN_SEPARATOR = (
    Fore.LIGHTGREEN_EX
    + "\t\t\t================================================================="
    + Style.RESET_ALL
)
