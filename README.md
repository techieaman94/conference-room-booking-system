# Conference Room Booking System 

## This is a terminal based application which can be used to create, book and manage conference rooms



### In this application

* An admin can do followings.
  * Add floors, rooms for a building.
  * Register organizations and their users.
* A registered user can do followings.
  * Can see available rooms for a selected duration.
  * Find rooms based on their requirements and book the same.
  * Cancel a booking.
  * See all bookings for their organization/done by the user/done by another user of the same company.
  
## Project structure
```
.
├── crbs
|   ├── __init__.py
|   ├── admin_functionalities.py
|   ├── command_line_interface.py
|   ├── constants.py
|   ├── entities.py
|   ├── permissions.py
|   ├── user_functionalities.py
|   ├── utils.py
|   └── validations.py
├── media
|   └── screenshots
|          └── ..
|          └── ..
|          └── ..
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

Here is a screenshot of the terminal for application.

![Screenshot_CRBS](https://github.com/techieaman94/conference-room-booking-system/assets/32607259/b25d2a66-4558-478f-b8dc-cf1acc8aff23)

Please check [media/screenshots](https://github.com/techieaman94/conference-room-booking-system/tree/master/media/screenshots) for more details.

### Installation and running the application

* Install [Python](https://wiki.python.org/moin/BeginnersGuide/Download).
* Install [pip](https://pip.pypa.io/en/stable/installation/)
* Download or clone this repo in local system.
* Open terminal.
* Get required packages for the application. 
 ```
 pip install -r requirements.txt
 ```
* Navigate inside the project folder where 'main.py' file is present.
* Run this application by command `python main.py`.

### Packages used

* [pytz](https://pypi.org/project/pytz/)
* [colorama](https://pypi.org/project/colorama/)
