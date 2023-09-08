from datetime import datetime, timedelta

import pytz

# Global variables to store data

floors = [1]

permissions = [
    {"id": 7, "name": "Can book a room"},
    {"id": 8, "name": "See all booking for the organization"},
]

equipments = [
    {"id": 1, "name": "Projector"},
    {"id": 2, "name": "White board"},
    {"id": 3, "name": "Mic"},
]

rooms = [
    {
        "id": 1693599332,
        "floor_number": 1,
        "name": "demo room 1",
        "capacity": 10,
        "equipments": [2, 3],
        "added_by": 1000,
    },
    {
        "id": 1693512123,
        "floor_number": 1,
        "name": "demo room 2",
        "capacity": 5,
        "equipments": [2],
        "added_by": 1000,
    },
]

organizations = [
    {
        "id": 1693599435,
        "name": "dummy organization",
        "contact_number": "+918888899999",
        "address": "201/126, xyz, abc, Bangalore, 560048",
        "added_by": 1000,
    }
]

admins = [
    {"id": 1000, "name": "Admin", "email_id": "admin@crbs.com", "password": "admin"}
]

users = [
    {
        "id": 2000,
        "name": "Rahul",
        "email_id": "user@crbs.com",
        "password": "user",
        "role": "SDE",
        "organization_id": 1693599435,
        "permissions": [7, 8],
        "added_by": 1000,
    }
]

now_datetime = datetime.now(pytz.timezone("Asia/Kolkata"))
bookings = [
    {
        "id": 1693599399,
        "room_id": 1693599332,
        "from_datetime": now_datetime + timedelta(hours=3),
        "to_datetime": now_datetime + timedelta(hours=4),
        "booked_by": 2000,
        "organization_id": 1693599435,
        "cancelled": False,
    },
    {
        "id": 1694158090,
        "room_id": 1693599332,
        "from_datetime": now_datetime + timedelta(hours=6),
        "to_datetime": now_datetime + timedelta(hours=7),
        "booked_by": 2000,
        "organization_id": 1693599435,
        "cancelled": False,
    },
]
