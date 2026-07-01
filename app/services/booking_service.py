from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.booking import Booking
from app.models.room import Room
from app.schemas.booking import BookingCreate, BookingUpdate
from app.logger import logger


class BookingService:

    @staticmethod
    def create_booking(
        db: Session,
        booking: BookingCreate,
        current_user
    ):

        # Check Room Exists
        room = db.query(Room).filter(
            Room.id == booking.room_id,
            Room.is_deleted == False
        ).first()

        if not room:
            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        # Room Availability
        if not room.is_available:
            raise HTTPException(
                status_code=400,
                detail="Room is not available"
            )

        # Booking Date Validation
        if booking.booking_date < date.today():
            raise HTTPException(
                status_code=400,
                detail="Cannot book for past date"
            )

        # Time Validation
        if booking.start_time >= booking.end_time:
            raise HTTPException(
                status_code=400,
                detail="End time must be greater than start time"
            )

        # Overlapping Booking Validation
        overlap = db.query(Booking).filter(
            Booking.room_id == booking.room_id,
            Booking.booking_date == booking.booking_date,
            Booking.status != "Cancelled",
            and_(
                Booking.start_time < booking.end_time,
                Booking.end_time > booking.start_time
            )
        ).first()

        if overlap:
            raise HTTPException(
                status_code=400,
                detail="Room already booked during this time"
            )

        new_booking = Booking(
            room_id=booking.room_id,
            employee_id=current_user.id,
            meeting_title=booking.meeting_title,
            booking_date=booking.booking_date,
            start_time=booking.start_time,
            end_time=booking.end_time,
            status="Scheduled"
        )

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        logger.info(
      f"Booking created. Room ID: {new_booking.room_id}, Employee ID: {new_booking.employee_id}"
)

        return new_booking

    @staticmethod
    def get_all_bookings(db: Session):

        return db.query(Booking).all()

    @staticmethod
    def get_booking(db: Session, booking_id: int):

        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return booking
    
    @staticmethod
    def update_booking(
        db: Session,
        booking_id: int,
        booking_data: BookingUpdate,
        current_user
    ):

        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        # Employee can update only their own booking
        if (
            current_user.role != "Admin"
            and booking.employee_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        update_data = booking_data.model_dump(exclude_unset=True)

        if (
            "start_time" in update_data
            and "end_time" in update_data
        ):
            if update_data["start_time"] >= update_data["end_time"]:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid booking time"
                )

        for key, value in update_data.items():
            setattr(booking, key, value)

        db.commit()
        db.refresh(booking)

        logger.info(f"Booking updated: {booking.id}")

        return booking
    
    @staticmethod
    def delete_booking(
        db: Session,
        booking_id: int,
        current_user
    ):

        booking = db.query(Booking).filter(
            Booking.id == booking_id
        ).first()

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        if (
            current_user.role != "Admin"
            and booking.employee_id != current_user.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access Denied"
            )

        booking.status = "Cancelled"

        db.commit()

        logger.info(f"Booking cancelled: {booking.id}")

        return {
         "message": "Booking Cancelled Successfully"
}
    
    @staticmethod
    def get_booking_history(db: Session, room_id: int):

        room = db.query(Room).filter(
            Room.id == room_id,
            Room.is_deleted == False
        ).first()

        if not room:
            raise HTTPException(
                status_code=404,
                detail="Room not found"
            )

        bookings = db.query(Booking).filter(
            Booking.room_id == room_id
        ).order_by(
            Booking.booking_date.desc(),
            Booking.start_time.desc()
        ).all()

        return bookings
    
    @staticmethod
    def filter_by_date(db: Session, booking_date):

        bookings = db.query(Booking).filter(
            Booking.booking_date == booking_date
        ).all()

        return bookings
    
    @staticmethod
    def filter_by_room(db: Session, room_id: int):

        bookings = db.query(Booking).filter(
            Booking.room_id == room_id
        ).all()

        return bookings
    
    @staticmethod
    def search_meeting(db: Session, keyword: str):

        bookings = db.query(Booking).filter(
            Booking.meeting_title.ilike(f"%{keyword}%")
        ).all()

        return bookings
    
    @staticmethod
    def get_paginated_bookings(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        offset = (page - 1) * limit

        bookings = db.query(Booking).offset(
            offset
        ).limit(
            limit
        ).all()

        return bookings
    
    @staticmethod
    def search_bookings(
        db: Session,
        room_id=None,
        booking_date=None,
        meeting_title=None
    ):

        query = db.query(Booking)

        if room_id:
            query = query.filter(
                Booking.room_id == room_id
            )

        if booking_date:
            query = query.filter(
                Booking.booking_date == booking_date
            )

        if meeting_title:
            query = query.filter(
                Booking.meeting_title.ilike(
                    f"%{meeting_title}%"
                )
            )

        return query.all()