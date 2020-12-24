from datetime import datetime
from enum import Enum

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
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


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users = {
    "admin": {
        "username": "Admin",
        "email": "user@example.com",
        "user_role": "Default/Standard ISM User",
        "active_time": {
          "active_from": "2020-12-22T17:16:57.545Z",
          "active_to": "2020-12-22T17:16:57.545Z"
        },
        "full_name": {
            "first_name": "string",
            "last_name": "string"
        },
        "password": "string"
    }

}


@router.get("/")
async def read_users(token: str = Depends(oauth2_scheme)):
    return [{"token": token, "username": "Rick2"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user(username: str):
    if username not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error!"},
        )
    return {"username": username}


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    response_description="The created user",
    deprecated=False,
    # description="Create a user with all information, username, full name, password, user role, active time range",
)
async def create_user(user: UserIn):
    """
    Create a user with all information:

    - **username**: each user must have a name
    - **email**: Email of the user
    - **user_role**: ISM user roles
      - Default / standard ISM user - Users automatically receive this user role, unless they are explicitly assigned an
       ISM Administrator or ISM Technical User Administrator role. Users can access the Data Custodian application.
      - ISM Administrator – Can add, edit, and remove all users and administrators in Data Custodian's ISM.
      - ISM Technical User Administrator – Can add, edit, and remove all technical users and technical user
      administrators in Data Custodian's ISM.
    - **Active Time Range**: The Active From field allows you to activate the user at a specific time.
    The Active To field allows you to deactivate the user at a specific time.
    - **full_name**: first name and last name
    """
    return user


@router.put("/{username}", response_model=UserOut)
async def update_user(username: str, user: UserIn):
    update_user_encoded = jsonable_encoder(user)
    return update_user_encoded


@router.patch("/{username}", response_model=UserOut)
async def update_user(username: str, user: UserIn):
    stored_user_data = users[username]
    stored_user_model = UserIn(**stored_user_data)
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_user_model.copy(update=update_data)
    users[username] = jsonable_encoder(updated_user)
    return updated_user
