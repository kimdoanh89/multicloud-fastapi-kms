from sqlalchemy.orm import Session
from typing import Any, Optional

from . import models
from backend import schemas
from backend.api.deps import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: Any):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pwd = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        role=user.user_role,
        active_from=user.active_from,
        active_to=user.active_to,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_by_id(db: Session, user_id: int):
    obj = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(obj)
    db.commit()
    return obj


def authenticate(db: Session, username: str, password: str) -> Optional[schemas.User]:
    user = get_user_by_username(db=db, username=username)
    # breakpoint()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
