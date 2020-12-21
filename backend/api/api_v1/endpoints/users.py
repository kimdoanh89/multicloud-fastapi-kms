from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr


class UserName(BaseModel):
    first_name: str
    last_name: str


class UserRole(str, Enum):
    default = "Default/Standard ISM User"
    admin = "ISM Administrator"
    technical = "ISM Technical User Administrator"


class ActiveTimeRange(BaseModel):
    active_from: datetime
    active_to: datetime


class UserIn(BaseModel):
    username: UserName
    password: str
    email: EmailStr
    user_role: UserRole = UserRole.default
    active_time: ActiveTimeRange


class UserOut(BaseModel):
    username: UserName
    email: EmailStr
    user_role: UserRole
    active_time: ActiveTimeRange


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def read_users(token: str = Depends(oauth2_scheme)):
    return [{"token": token, "username": "Rick2"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}


@router.post("/", response_model=UserOut)
async def create_user(user: UserIn):
    return user
