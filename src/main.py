from fastapi import FastAPI
from api import userControler
from db.session import connect_to_mongo


app = FastAPI(
    title="HyperFit API",
    description="Backend service for HyperFit - AI-powered fitness application",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routers
app.include_router(userControler.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 