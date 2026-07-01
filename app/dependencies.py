from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.oauth2 import get_current_user


def get_database():
    return Depends(get_db)


def admin_required(
    current_user=Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can access."
        )
    return current_user


def employee_required(
    current_user=Depends(get_current_user)
):
    if current_user.role not in ["Admin", "Employee"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )
    return current_user