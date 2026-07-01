from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import admin_required
from app.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomResponse
)
from app.schemas.responses import MessageResponse
from app.services.room_service import RoomService

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post(
    "",
    response_model=RoomResponse
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return RoomService.create_room(db, room)


@router.get(
    "",
    response_model=List[RoomResponse]
)
def get_rooms(
    db: Session = Depends(get_db)
):
    return RoomService.get_all_rooms(db)


@router.get(
    "/{room_id}",
    response_model=RoomResponse
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    return RoomService.get_room_by_id(
        db,
        room_id
    )


@router.put(
    "/{room_id}",
    response_model=RoomResponse
)
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return RoomService.update_room(
        db,
        room_id,
        room
    )


@router.delete(
    "/{room_id}",
    response_model=MessageResponse
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    return RoomService.delete_room(
        db,
        room_id
    )