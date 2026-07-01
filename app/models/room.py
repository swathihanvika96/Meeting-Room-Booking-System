from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)

    room_name = Column(String(100), unique=True, nullable=False)

    capacity = Column(Integer, nullable=False)

    floor = Column(Integer, nullable=False)

    amenities = Column(String(300))

    is_available = Column(Boolean, default=True)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship(
        "Booking",
        back_populates="room",
        cascade="all, delete"
    )