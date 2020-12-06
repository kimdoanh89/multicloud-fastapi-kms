from fastapi import FastAPI
# import uvicorn

from api.api_v1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


# if __name__ == "__main__":
#     uvicorn.run("main:app")

