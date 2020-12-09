from fastapi import APIRouter
from cryptography.fernet import Fernet
from typing import Optional

router = APIRouter()


@router.get("/")
async def read_keys():
    return [{"keyname": "KEK"}, {"keyname": "DEK"}]


@router.get("/{keyname}")
async def read_key(keyname: str):
    return {"keyname": keyname}


@router.post("/")
def create_key(keyname: str,  group: str, key_type: str, key_description: Optional[str] = None):
    """
    Create a new key
    :return:
    """
    key = Fernet.generate_key()
    result = {
        "keyname": keyname,
        "key_description": key_description,
        "type": key_type,
        "group": group,
        "value": key
    }
    return result

