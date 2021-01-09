from fastapi import FastAPI, Depends
import uvicorn

from backend.api.api_v1.api import api_router
# from fastapi.security import OAuth2PasswordBearer

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
app.include_router(
    api_router,
    prefix="/v1",
    # dependencies=[Depends(oauth2_scheme)]
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications new3!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)

