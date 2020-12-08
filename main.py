from fastapi import FastAPI
import uvicorn

from api.api_v1.api import api_router
from api.api_v2.api import api_router as api_v2_router

app = FastAPI()
app.include_router(api_router)
app.include_router(api_v2_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("main:app")

