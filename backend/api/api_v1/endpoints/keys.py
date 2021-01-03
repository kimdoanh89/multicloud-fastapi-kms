from fastapi import APIRouter, Query
from cryptography.fernet import Fernet

from backend import schemas

router = APIRouter()


@router.get("/")
async def read_keys():
    return [{"key_name": "KEK"}, {"key_name": "DEK"}]


@router.get("/{key_name}")
async def read_key(key_name: str):
    return {"key_name": key_name}


@router.post("/")
def create_key(key: schemas.Key):
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
