from fastapi import APIRouter

from api.api_v2.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users", "v2"])
