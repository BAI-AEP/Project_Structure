import datetime
import sys
from datetime import date
from random import seed, choices

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from data_models.models import *


def generate_hotels(engine: Engine):
    with Session(engine) as session:
        single_room = RoomType(description="Einzelzimmer")
        double_room = RoomType(description="Doppelzimmer")
        family_room = RoomType(description="Familienzimmer")
        suite = RoomType(description="Suite")
        session.add_all([single_room, double_room, family_room])

        tv43 = Amenity(description='TV - 43"')
        tv50 = Amenity(description='TV - 50"')
        tee_cooker = Amenity(description="Teekocher")
        nespresso = Amenity(description="Nespresso Machine")
        iron = Amenity(description="Bügeleisen")
        session.add_all([tv43, tv50, tee_cooker, nespresso, iron])

        hotels_to_insert = [
            Hotel(
                name="Hotel Amaris",
                stars=3,
                address=Address(
                    street="Tannwaldstrasse 34",
                    zip="4600",
                    city="Olten"
                ),
                rooms=[
                    Room(number="01", type=single_room, max_guests=1, description="One single bed", price=124.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="02", type=double_room, max_guests=2, description="One double bed", price=138.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="03", type=single_room, max_guests=1, description="One single bed", price=124.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="04", type=double_room, max_guests=2, description="Two single beds", price=138.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="05", type=family_room, max_guests=4,
                         description="One queensized bed and two single beds", price=219.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="06", type=double_room, max_guests=2, description="One double bed", price=138.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="07", type=double_room, max_guests=2, description="One double bed", price=138.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="11", type=double_room, max_guests=2, description="One queensized bed", price=165.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="12", type=double_room, max_guests=2, description="One queensized bed", price=165.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="13", type=double_room, max_guests=2, description="One queensized bed", price=165.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="14", type=double_room, max_guests=2, description="One kingsized bed", price=183.0,
                         amenities=[tv50, tee_cooker, nespresso, iron]),
                    Room(number="15", type=double_room, max_guests=2, description="One kingsized bed", price=183.0,
                         amenities=[tv50, tee_cooker, nespresso, iron]),
                ]
            ),

            Hotel(
                name="Leonardo Boutique Hotel Rigihof Zurich",
                stars=3,
                address=Address(
                    street=" Universitätstrasse 101",
                    zip="8006",
                    city="Zürich"
                ),
                rooms=[
                    Room(number="01", type=double_room, max_guests=2, description="Komfort Zimmer", price=139.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="02", type=double_room, max_guests=2, description="Komfort Zimmer", price=139.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="03", type=double_room, max_guests=2, description="Komfort Zimmer", price=139.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="04", type=double_room, max_guests=2, description="Komfort Zimmer", price=139.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="05", type=double_room, max_guests=3, description="Komfort Zimmer", price=139.0,
                         amenities=[tv43, tee_cooker]),
                    Room(number="06", type=double_room, max_guests=2, description="Superior Zimmer", price=141.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="07", type=double_room, max_guests=2, description="Superior Zimmer", price=141.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="11", type=double_room, max_guests=2, description="Superior Zimmer", price=141.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="12", type=suite, max_guests=4, description="Suite", price=153.0,
                         amenities=[tv50, tee_cooker, iron]),
                    Room(number="13", type=suite, max_guests=4, description="Suite", price=153.0,
                         amenities=[tv50, tee_cooker, iron]),
                ]
            )
        ]

        session.add_all(hotels_to_insert)
        session.commit()


def generate_guests(engine: Engine):
    with Session(engine) as session:
        guests_to_add = [
            Guest(
                firstname="Hans",
                lastname="Müller",
                address=Address(
                    street="Bachstrasse 12",
                    zip="5000",
                    city="Aarau"
                ),
                email="hans.müller@gmail.com"
            ),
            Guest(
                firstname="Anna",
                lastname="Becker",
                address=Address(
                    street="Munzingerstrasse 17C",
                    zip="3007",
                    city="Bern"
                ),
                email="anna.becker@gmail.com"
            ),
            Guest(
                firstname="Bettina",
                lastname="Braun",
                address=Address(
                    street="Im Egeli 23",
                    zip="8700",
                    city="Küsnacht"
                ),
                email="bettina.braun@gmail.com"
            )
        ]

        session.add_all(guests_to_add)
        session.commit()

def generate_system_data(engine: Engine):
    with Session(engine) as session:
        administrator = Role(name="administrator", access_level=sys.maxsize)
        registered_user = Role(name="registered_user", access_level=1)
        session.add_all([administrator, registered_user])
        session.commit()


def generate_registered_guests(engine: Engine):
    with Session(engine) as session:
        registered_guests_to_add = [
            RegisteredGuest(
                firstname="Sabrina",
                lastname="Schmidt",
                email="sabrina.schmidt@bluemail.ch",
                address=Address(
                    street="Goethestrasse 26",
                    zip="9008",
                    city="St. Gallen"
                ),
                login=Login(
                    username="sabrina.schmidt@bluemail.ch",
                    password="SuperSecret",
                    role=session.query(Role).filter(Role.name == "registered_user").one()
                )
            ),
            RegisteredGuest(
                firstname="Laura",
                lastname="Jackson",
                email="laura.jackson@bluemail.ch",
                address=Address(
                    street="Tödistrasse 49",
                    zip="8002",
                    city="Zürich"
                ),
                login=Login(
                    username="laura.jackson@bluemail.ch",
                    password="SuperSecret",
                    role=session.query(Role).filter(Role.name == "registered_user").one()
                )
            )
        ]
        session.add_all(registered_guests_to_add)
        session.commit()


def generate_booking_dates(k: int = 20, s: int = 1):
    seed(s)
    start_of_year = date(date.today().year, 1, 1)
    end_of_year = date(date.today().year, 12, 31)
    possible_days = [start_of_year + datetime.timedelta(days=x) for x in range((end_of_year - start_of_year).days + 1)]
    start_day_choices = choices(possible_days, k=k)

    possible_durations = [1, 2, 3, 4, 5]
    duration_choices = choices(possible_durations, k=k)
    end_day_choices = [start_day_choices[i] + datetime.timedelta(days=duration) for i, duration in
                       enumerate(duration_choices)]

    return start_day_choices, end_day_choices


def generate_random_bookings(engine: Engine, k: int = 20, s: int = 1):
    seed(s)
    start_days, end_days = generate_booking_dates(k, s)

    with Session(engine) as session:
        possible_guests = session.query(Guest).all()
        if not len(possible_guests) > 0:
            generate_guests(engine)
            possible_guests = session.query(Guest).all()
        guest_choices = choices(possible_guests, k=k)

        possible_rooms = session.query(Room).all()
        if not len(possible_rooms) > 0:
            generate_hotels(engine)
            possible_rooms = session.query(Room).all()
        room_choices = choices(possible_rooms, k=k)

        bookings_to_add = []
        for i in range(k):
            bookings_to_add.append(
                Booking(
                    room=room_choices[i],
                    guest=guest_choices[i],
                    number_of_guests=1,
                    start_date=start_days[i],
                    end_date=end_days[i]
                )
            )
        session.add_all(bookings_to_add)
        session.commit()


def generate_random_registered_bookings(engine: Engine, k: int = 5, s: int = 1):
    seed(s)
    start_days, end_days = generate_booking_dates(k, s)
    with Session(engine) as session:
        possible_registered_guests = session.query(RegisteredGuest).all()
        if not len(possible_registered_guests) > 0:
            generate_guests(engine)
            possible_registered_guests = session.query(RegisteredGuest).all()
        registered_guest_choices = choices(possible_registered_guests, k=k)

        possible_rooms = session.query(Room).all()
        if not len(possible_rooms) > 0:
            generate_hotels(engine)
            possible_rooms = session.query(Room).all()
        room_choices = choices(possible_rooms, k=k)
        registered_bookings_to_add = []
        for i in range(k):
            registered_bookings_to_add.append(
                Booking(
                    room=room_choices[i],
                    guest=registered_guest_choices[i],
                    number_of_guests=1,
                    start_date=start_days[i],
                    end_date=end_days[i]
                )
            )
        session.add_all(registered_bookings_to_add)
        session.commit()
