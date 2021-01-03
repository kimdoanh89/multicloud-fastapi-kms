from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr


class FullName(BaseModel):
    first_name: str
    last_name: str


class UserRole(str, Enum):
    default = "Default/Standard ISM User"
    admin = "ISM Administrator"
    technical = "ISM Technical User Administrator"


class ActiveTimeRange(BaseModel):
    active_from: datetime
    active_to: datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    user_role: UserRole = UserRole.default
    active_time: ActiveTimeRange
    full_name: FullName


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
