from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from fastapi import Body


class KeyType(str, Enum):
    aes = "AES"
    rsa = "RSA"
    ec = "EC"


class KeyBase(BaseModel):
    name: str = Body(..., min_length=3, max_length=50)
    group: str = Body(..., min_length=3, max_length=50)
    type: KeyType
    description: Optional[str] = Field(
        None, title="The description of the key", max_length=300
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "key_name": "Foo",
    #             "group": "Bar",
    #             "key_type": "AES",
    #             "key_description": "This is symmetric key"
    #         }
    #     }


class KeyCreate(KeyBase):
    pass


class KeyInDB(KeyBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
