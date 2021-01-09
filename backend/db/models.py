from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    active_from = Column(DateTime)
    active_to = Column(DateTime)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

    keys = relationship("Key", back_populates="owner")


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    group = Column(String, index=True)
    type = Column(String)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="keys")
