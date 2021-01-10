from fastapi import APIRouter
from cryptography.fernet import Fernet

from backend import schemas

router = APIRouter()


@router.get("/")
async def read_keys():
    return [{"key_name": "KEK"}, {"key_name": "DEK"}]


@router.get("/{key_name}")
async def read_key(key_name: str):
    return {"key_name": key_name}


@router.post("/", response_model=schemas.KeyCreate)
def create_key(key: schemas.KeyCreate):
    """
    Create a new key.

    Validation for key name, group, and keyType (Enum: AES, RSA, EC)
    """
    value = Fernet.generate_key()
    result = {
        "key_name": key.name,
        "key_description": key.description,
        "type": key.type.value,
        "group": key.group,
        "value": value,
    }
    return key
