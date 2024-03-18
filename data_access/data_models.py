from datetime import date

from typing import List
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    '''
    Basis Klasse für unser Model. Daraus kann SQLAlchemy herleiten welche Klassen zu unserem Modell gehören.
    '''
    pass

class Address(Base):
    '''
    Adress Entitätstyp.
    '''
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column()
    zip: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, street={self.street!r}, city={self.city!r}, zip={self.zip!r})"

class Guest(Base):
    '''
    Gast Entitätstyp.
    '''
    __tablename__ = "guest"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))
    address: Mapped["Address"] = relationship()
    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "guest",
        "polymorphic_on": "type",
    }

    def __repr__(self) -> str:
        return f"Guest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, address={self.address!r})"
    
class RegisteredGuest(Guest):
    '''
    Registrier Gast Entitätstyp.
    '''
    __tablename__ = "registred_guest"
    id: Mapped[int] = mapped_column(ForeignKey("guest.id"), primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    bookings: Mapped[List["Booking"]] = relationship(back_populates="guest")

    __mapper_args__ = {
        "polymorphic_identity": "registered"
    }

    def __repr__(self) -> str:
        return f"RegisteredGuest(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r}, address={self.address!r}, email={self.email!r}, password={self.password!r})"

class Hotel(Base):
    '''
    Hotel Entitätstyp.
    '''
    __tablename__ = "hotel"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    stars: Mapped[int] = mapped_column()
    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))
    address: Mapped["Address"] = relationship()
    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel")

    def __repr__(self) -> str:
        return f"Hotel(id={self.id!r}, name={self.name!r}, stars={self.stars}, address={self.address})"

class RoomType(Base):
    '''
    Raumtyp Entitätstyp.
    '''
    __tablename__ = "room_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"RoomType(id={self.id!r}, description={self.description!r})"

class Amenity(Base):
    '''
    Einrichtung Entitätstyp.
    '''
    __tablename__ = "amenity"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Amenity(id={self.id!r}, description={self.description!r})"
    
class RoomAmenity(Base):
    __tablename__ = "room_amenity"
    room_hotel_id: Mapped[int] = mapped_column(primary_key=True)
    room_number: Mapped[str] = mapped_column(primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenity.id"), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_hotel_id', 'room_number'],
            ['room.hotel_id', 'room.number'],
        ),
    )

class Room(Base):
    '''
    Raum Entitätstyp.
    '''
    __tablename__ = "room"
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotel.id"), primary_key=True)
    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    number: Mapped[str] = mapped_column(primary_key=True)
    type_id: Mapped[str] = mapped_column(ForeignKey("room_type.id"))
    type: Mapped["RoomType"] = relationship()
    max_guests: Mapped[int] = mapped_column()
    #beds: Mapped[List["Bed"]] = relationship()
    description: Mapped[str] = mapped_column()
    amenities: Mapped[List["Amenity"]] = relationship(secondary='room_amenity')
    price: Mapped[float] = mapped_column()

    def __repr__(self) -> str:
        return f"Room(hotel={self.hotel!r}, room_number={self.number!r}, type={self.type!r}, description={self.description!r}, price={self.price!r})"

class Booking(Base):
    __tablename__ = "booking"

    id:Mapped[int] = mapped_column(primary_key=True)
    room_hotel_id: Mapped[int] = mapped_column()
    room_number: Mapped[str] = mapped_column()
    room: Mapped["Room"] = relationship()
    guest_id: Mapped[int] = mapped_column(ForeignKey("guest.id"))
    guest: Mapped["Guest"] = relationship()
    number_of_guests: Mapped[int] = mapped_column()
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    comment: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['room_hotel_id', 'room_number'],
            ['room.hotel_id', 'room.number'],
        ),
    )

    def __repr__(self) -> str:
        return f"Booking(room={self.room!r}, guest={self.guest!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, comment={self.comment!r})"