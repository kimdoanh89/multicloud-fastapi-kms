from fastapi import FastAPI
import uvicorn

from backend.api.api_v1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications new3!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)

