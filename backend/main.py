from config import CFG

from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

from apps.basic.routers import router as basic_router

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    app.client = AsyncIOMotorClient(CFG["MONGODB_URL"])
    app.db = app.client[CFG["DB_NAME"]]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.client.close()

app.include_router(basic_router, tags=["basic"], prefix="/basic")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=CFG["HOST"],
        reload=CFG["DEBUG"],
        port=CFG["PORT"],
    )