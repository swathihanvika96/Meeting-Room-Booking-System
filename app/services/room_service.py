from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate
from app.logger import logger


class RoomService:

    @staticmethod
    def create_room(db: Session, room: RoomCreate):

        existing_room = db.query(Room).filter(
            Room.room_name == room.room_name,
            Room.is_deleted == False
        ).first()

        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room already exists"
            )

        new_room = Room(
            room_name=room.room_name,
            capacity=room.capacity,
            floor=room.floor,
            amenities=room.amenities,
            is_available=room.is_available
        )

        db.add(new_room)
        db.commit()
        db.refresh(new_room)

        logger.info(f"Room created: {new_room.room_name}")

        return new_room

    @staticmethod
    def get_all_rooms(db: Session):

        return db.query(Room).filter(
            Room.is_deleted == False
        ).all()

    @staticmethod
    def get_room_by_id(db: Session, room_id: int):

        room = db.query(Room).filter(
            Room.id == room_id,
            Room.is_deleted == False
        ).first()

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        return room

    @staticmethod
    def update_room(db: Session, room_id: int, room_data: RoomUpdate):

        room = db.query(Room).filter(
            Room.id == room_id,
            Room.is_deleted == False
        ).first()

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        update_data = room_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(room, key, value)

        db.commit()
        db.refresh(room)

        logger.info(f"Room updated: {room.room_name}")
        return room

    @staticmethod
    def delete_room(db: Session, room_id: int):

        room = db.query(Room).filter(
            Room.id == room_id,
            Room.is_deleted == False
        ).first()

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        room.is_deleted = True

        db.commit()

        logger.info(f"Room deleted: {room.room_name}")

        return {
        "message": "Room deleted successfully"
}