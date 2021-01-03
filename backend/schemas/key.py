from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
from fastapi import Query


class KeyType(str, Enum):
    aes = "AES"
    rsa = "RSA"
    ec = "EC"


class Key(BaseModel):
    key_name: str = Query(..., min_length=3, max_length=50)
    group: str = Query(..., min_length=3, max_length=50)
    key_type: KeyType
    key_description: Optional[str] = Field(
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
