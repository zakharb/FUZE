from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from app.collection.routers import router as col_router
from app.normalization.routers import router as nor_router
from app.fusion.routers import router as fus_router

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['Content-Type', 'application/xml'],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(col_router, tags=["collection"], prefix="/collection")
app.include_router(nor_router, tags=["normalization"], prefix="/normalization")
app.include_router(fus_router, tags=["fusion"], prefix="/fusion")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=True,
        #settings.DEBUG_MODE,
        port=settings.PORT,
    )
