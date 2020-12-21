from fastapi import APIRouter, Query
from cryptography.fernet import Fernet
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


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


router = APIRouter()


@router.get("/")
async def read_keys():
    return [{"key_name": "KEK"}, {"key_name": "DEK"}]


@router.get("/{key_name}")
async def read_key(key_name: str):
    return {"key_name": key_name}


@router.post("/")
def create_key(key: Key):
    """
    Create a new key.
    Validation for keyname, group, and keyType (Enum: AES, RSA, EC)
    """
    value = Fernet.generate_key()
    result = {
        "key_name": key.key_name,
        "key_description": key.key_description,
        "type": key.key_type.value,
        "group": key.group,
        "value": value,
    }
    return result
