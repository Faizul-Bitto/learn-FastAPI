from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from routers.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

# Configuration Objects
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Database Integration
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# Request Field Validation
class UserRequest(BaseModel):
    hashed_password: str
    new_hashed_password: str = Field(min_length=6)


# Get user information
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    return user


# Update Password
@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user: user_dependency, db: db_dependency, user_verification_request: UserRequest
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(
        user_verification_request.hashed_password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password",
        )

    user.hashed_password = bcrypt_context.hash(
        user_verification_request.new_hashed_password
    )

    db.add(user)
    db.commit()


# Update Phone Number
@router.put("/update_phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: user_dependency, db: db_dependency, phone_number: str
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user = db.query(Users).filter(Users.id == user.get("user_id")).first()

    user.phone_number = phone_number

    db.add(user)
    db.commit()