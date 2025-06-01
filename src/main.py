from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import userControler
from api import deepseek
from db.session import connect_to_mongo, close_mongo_connection
from api import googleAuthController

@asynccontextmanager
async def lifespan(app: FastAPI):
   await connect_to_mongo()
   yield
   await close_mongo_connection()

app = FastAPI(
    title="HyperFit API",
    description="Backend service for HyperFit - AI-powered fitness application",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(userControler.router, prefix="/api/v1")
app.include_router(googleAuthController.router, prefix="/api/v1")
app.include_router(deepseek.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 