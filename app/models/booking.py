from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import Time
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    room_id = Column(
        Integer,
        ForeignKey("rooms.id"),
        nullable=False
    )

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    meeting_title = Column(String(200), nullable=False)

    booking_date = Column(Date, nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    status = Column(String(30), default="Scheduled")

    created_at = Column(DateTime, default=datetime.utcnow)

    room = relationship(
        "Room",
        back_populates="bookings"
    )

    employee = relationship(
        "User",
        back_populates="bookings"
    )