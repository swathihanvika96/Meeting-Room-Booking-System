from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    role = Column(String(20), default="Employee")

    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship(
        "Booking",
        back_populates="employee",
        cascade="all, delete"
    )