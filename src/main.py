from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import userControler
from api import chatbotController
from api import routineController
from db.session import connect_to_mongo, close_mongo_connection
from api import authController
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(userControler.router, prefix="/api/v1")
app.include_router(chatbotController.router, prefix="/api/v1")
app.include_router(authController.router, prefix="/api/v1")
app.include_router(routineController.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 