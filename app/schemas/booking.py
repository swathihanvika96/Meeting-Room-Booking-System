from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional


class BookingCreate(BaseModel):
    room_id: int
    meeting_title: str = Field(..., min_length=3)
    booking_date: date
    start_time: time
    end_time: time


class BookingUpdate(BaseModel):
    meeting_title: Optional[str] = None
    booking_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    room_id: int
    employee_id: int
    meeting_title: str
    booking_date: date
    start_time: time
    end_time: time
    status: str

    class Config:
        from_attributes = True