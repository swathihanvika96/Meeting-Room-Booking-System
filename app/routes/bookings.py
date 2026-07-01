from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.oauth2 import get_current_user
from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse
)
from app.schemas.responses import MessageResponse
from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post(
    "",
    response_model=BookingResponse
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.create_booking(
        db,
        booking,
        current_user
    )


@router.get(
    "",
    response_model=List[BookingResponse]
)
def get_bookings(
    db: Session = Depends(get_db)
):
    return BookingService.get_all_bookings(db)


@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    return BookingService.get_booking(
        db,
        booking_id
    )


@router.put(
    "/{booking_id}",
    response_model=BookingResponse
)
def update_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.update_booking(
        db,
        booking_id,
        booking,
        current_user
    )


@router.delete(
    "/{booking_id}",
    response_model=MessageResponse
)
def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BookingService.delete_booking(
        db,
        booking_id,
        current_user
    )

@router.get("/history/{room_id}")
def booking_history(
    room_id: int,
    db: Session = Depends(get_db)
):
    return BookingService.get_booking_history(
        db,
        room_id
    )


@router.get("/search/")
def search_bookings(
    room_id: Optional[int] = None,
    booking_date: Optional[date] = None,
    meeting_title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return BookingService.search_bookings(
        db,
        room_id,
        booking_date,
        meeting_title
    )


@router.get("/page/")
def paginated_bookings(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return BookingService.get_paginated_bookings(
        db,
        page,
        limit
    )