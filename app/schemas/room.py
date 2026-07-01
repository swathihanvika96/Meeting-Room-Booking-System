from pydantic import BaseModel, Field
from typing import Optional


class RoomCreate(BaseModel):
    room_name: str
    capacity: int = Field(..., gt=0)
    floor: int
    amenities: Optional[str] = None
    is_available: bool = True


class RoomUpdate(BaseModel):
    room_name: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0)
    floor: Optional[int] = None
    amenities: Optional[str] = None
    is_available: Optional[bool] = None


class RoomResponse(BaseModel):
    id: int
    room_name: str
    capacity: int
    floor: int
    amenities: Optional[str]
    is_available: bool

    class Config:
        from_attributes = True