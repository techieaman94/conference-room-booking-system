from crbs.constants import SEPARATOR
from crbs.entities import floors, organizations, permissions, rooms, users
from crbs.user_functionalities import get_current_datetime_ist
from crbs.utils import add_rooms_to_floor, print_items_from_list
from getpass import getpass

from crbs.validations import validate_email


def add_new_floor(admin_id):
    print(f"{SEPARATOR}\n\t\t\tADD NEW FLOOR\n")
    floor_number = int(input("\t\t\tEnter floor number : "))
    if floor_number in floors:
        print(f"\t\t\tFloor number : {floor_number} already exists!")
    else:
        floors.append(floor_number)
        no_of_rooms = int(input("\t\t\tEnter number of rooms you want to add : "))
        add_rooms_to_floor(no_of_rooms, floor_number, admin_id)
        print(f"\n\t\t\tFloor details added successfully")
        print_items_from_list("All Rooms", rooms)


def add_rooms_to_existing_floor(admin_id):
    print(f"{SEPARATOR}\n\t\t\tADD NEW ROOMS TO A FLOOR\n")
    floor_number = int(input("\t\t\tEnter the existing floor number to add rooms : "))
    if floor_number not in floors:
        print(f"\t\t\tFloor number : {floor_number} doesn't exists!")
        add_rooms_to_existing_floor(admin_id)
    else:
        no_of_rooms = int(input("\t\t\tEnter number of rooms you want to add : "))
        add_rooms_to_floor(no_of_rooms, floor_number, admin_id)
        print(f"\n\t\t\tRoom details added successfully")
        print_items_from_list("Rooms", rooms)


def register_new_organization(admin_id):
    print(f"{SEPARATOR}\n\t\t\tADD NEW ORGANIZATION\n")
    org_name = input("\t\t\tEnter the name of the organization : ")
    contact_number = input("\t\t\tEnter contact number : ")
    address = input("\t\t\tEnter address : ")
    org_id = int(get_current_datetime_ist().timestamp())
    organizations.append(
        dict(
            id=org_id,
            name=org_name,
            contact_number=contact_number,
            address=address,
            added_by=admin_id,
        )
    )
    print(f"\n\t\t\tOrganization added, id : {org_id}")
    print_items_from_list("Organizations", organizations)


def register_new_user(admin_id):
    print(f"{SEPARATOR}\n\t\t\tREGISTER NEW USER\n")
    user_name = input("\t\t\tEnter the name of the user : ")
    email_id = input("\t\t\tEnter email id, example - 'abc@xyz.com' : ")
    validate_email(email_id)
    password = getpass(prompt="\t\t\tEnter password for user : ")
    role = input("\t\t\tEnter user role : ")
    valid_org_ids_list = [org["id"] for org in organizations]
    valid_org_ids_str = ", ".join(map(str, valid_org_ids_list))
    print(f"\t\t\tValid organization ids (already registered) : {valid_org_ids_str}")
    org_id = int(input("\t\t\tEnter organization id for the user : "))
    if org_id not in valid_org_ids_list:
        raise ValueError(f"\t\t\tOrganization id : {org_id} doesn't exists!")
    print(
        "\t\t\tEnter the permission ids for the user from followings (comma separated, example : 7,8)"
    )
    for permission in permissions:
        print("\t\t\t\tID : {}, Name : {}".format(permission["id"], permission["name"]))
    permission_ids = input("\t\t\tPermissions ids : ")
    permission_ids = ("".join(permission_ids.split())).split(",")
    permission_ids = list(map(int, permission_ids))
    valid_permission_ids = [permission["id"] for permission in permissions]
    if not set(permission_ids).issubset(set(valid_permission_ids)):
        print(f"\t\t\tInvalid input for permission!")
        return

    user_id = int(get_current_datetime_ist().timestamp())
    users.append(
        dict(
            id=user_id,
            name=user_name,
            email_id=email_id,
            password=password,
            role=role,
            organization_id=org_id,
            permissions=permission_ids,
            added_by=admin_id,
        )
    )
    print(f"\n\t\t\tUser added, id : {user_id}")
    print_items_from_list("Users", users)
