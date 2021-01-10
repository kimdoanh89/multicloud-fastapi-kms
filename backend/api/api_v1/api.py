from fastapi import APIRouter, Depends

from backend.api.api_v1.endpoints import users, keys, login
from backend.api.deps import reusable_oauth2

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    keys.router,
    prefix="/keys",
    tags=["keys"],
    dependencies=[Depends(reusable_oauth2)]
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(reusable_oauth2)]
)
