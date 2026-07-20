from datetime import timedelta, datetime, timezone
from typing import Annotated

from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users

router = APIRouter(prefix="/auth", tags=["auth"])


# Configuration Objects
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = "0b264f40ccf2b5a6441396494707668cf191aa3819e9e9e29fb77e553458a662"
ALGORITHM = "HS256"


# Database Integration
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]

login_token_field_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]

oauth2_bearer_token_dependency = Annotated[str, Depends(oauth2_bearer)]


# Request Field Validation
class UserRequest(BaseModel):
    user_name: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Supporting Methods
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.user_name == username).first()
    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(
    user_name: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": user_name, "id": user_id, "role": role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: oauth2_bearer_token_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")

        if user_name is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return {"user_id": user_id, "user_name": user_name, "user_role": user_role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


# Create / Register User
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserRequest):
    user = Users(
        email=create_user_request.email,
        user_name=create_user_request.user_name,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.hashed_password),
        role=create_user_request.role,
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Create Token and Login
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: login_token_field_dependency, db: db_dependency
):
    user = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        user_name=user.user_name,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=30),
    )

    return {"access_token": token, "token_type": "bearer"}
