from fastapi import FastAPI

from app.database import Base, engine

from app.routes import auth
from app.routes import rooms
from app.routes import bookings

# Import logger
from app.logger import logger

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Meeting Room Booking System",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(bookings.router)


@app.on_event("startup")
def startup_event():
    logger.info("Meeting Room Booking System started successfully.")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("Meeting Room Booking System stopped.")


@app.get("/")
def home():
    logger.info("Home endpoint accessed.")
    return {
        "message": "Welcome to Meeting Room Booking System API"
    }