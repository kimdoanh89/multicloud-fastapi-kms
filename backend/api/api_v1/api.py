from fastapi import APIRouter

from api.api_v1.endpoints import users, keys

api_router = APIRouter()
api_router.include_router(keys.router, prefix="/keys", tags=["keys"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
