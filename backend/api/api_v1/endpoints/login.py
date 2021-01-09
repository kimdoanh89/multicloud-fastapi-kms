from fastapi import APIRouter
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login/access-token")
def login_access_token():
    pass
