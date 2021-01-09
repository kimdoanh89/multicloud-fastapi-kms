from sqlalchemy.orm import Session

from . import models
from backend import schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username,
        email=user.email,
        role=user.user_role,
        active_from=user.active_from,
        active_to=user.active_to,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_by_email(db: Session, email: str):
    obj = db.query(models.User).filter(models.User.email == email).first()
    db.delete(obj)
    db.commit()
    return obj


def remove_by_username(db: Session, username: str):
    obj = db.query(models.User).filter(models.User.username == username).first()
    db.delete(obj)
    db.commit()
    return obj
