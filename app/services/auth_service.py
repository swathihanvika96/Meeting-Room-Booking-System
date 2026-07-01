from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.logger import logger


class AuthService:

    @staticmethod
    def register(db: Session, user: UserCreate):

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:
            logger.error(f"Registration failed. Email already exists: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        new_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            role=user.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"New user registered: {new_user.email}")

        return new_user

    @staticmethod
    def login(db: Session, email: str, password: str):

        user = db.query(User).filter(
            User.email == email
        ).first()

        # Check whether user exists
        if not user:
            logger.error(f"Login failed. Email not found: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Email or Password"
            )

        # Verify password
        if not verify_password(password, user.password):
            logger.error(f"Wrong password for: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Email or Password"
            )

        # Generate JWT Token
        access_token = create_access_token(
            {
                "sub": user.email
            }
        )

        logger.info(f"User logged in successfully: {user.email}")

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }