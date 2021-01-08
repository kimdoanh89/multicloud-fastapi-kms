from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    default = "Default/Standard ISM User"
    admin = "ISM Administrator"
    technical = "ISM Technical User Administrator"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    user_role: UserRole = UserRole.default
    active_from: datetime
    active_to: datetime
    first_name: str
    last_name: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str
