from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from backend import schemas
from backend.db import models, crud
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/")
async def read_users(token: str = Depends(oauth2_scheme)):
    return [{"token": token, "username": "Rick2"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get(
    "/{username}",
    # response_model=schemas.UserOut,
    summary="Get User by Username"
)
async def read_user(username, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(username=username, db=db)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error!"},
        )
    return db_user


@router.post(
    "/",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    response_description="The created user",
    deprecated=False,
    # description="Create a user with all information, username, full name, password, user role, active time range",
)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
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
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, user=user)

    return user


@router.put("/{username}", response_model=schemas.UserOut)
async def update_user(user: schemas.UserIn):
    update_user_encoded = jsonable_encoder(user)
    return update_user_encoded


@router.delete("{email}")
async def delete_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Item not found!")
    user = crud.remove_by_email(db=db, email=email)
    return user
