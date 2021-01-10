from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from backend import schemas
from backend.db import crud_user
from sqlalchemy.orm import Session
from backend.api.deps import get_db
from backend.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.User], summary="List all users")
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db=db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User, summary="Get current user")
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    summary="Get user by username"
)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error!"},
        )
    return db_user


@router.post(
    "/",
    response_model=schemas.UserBase,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    response_description="The created user",
    deprecated=False,
    # description="Create a user with all information, username, full name, password, user role, active time range",
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
    db_user = crud_user.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud_user.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud_user.create_user(db=db, user=user)

    return user


@router.delete(
    "/{user_id}",
    response_model=schemas.User,
    summary="Delete user by user id", )
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    if user_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete this superuser!"
        )
    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Item not found!")
    user = crud_user.remove_by_id(db=db, user_id=user_id)
    return user
