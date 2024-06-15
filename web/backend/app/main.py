from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.collectors_router import router as collectors_router
from app.api.sources_router import router as sources_router
from app.api.normalization_router import router as normalization_router
from app.api.correlation_router import router as correlation_router
from app.api.taxanomy_router import router as taxanomy_router
from app.api.dahboard_router import router as siem_router
from app.api.netmap_router import router as netmap_router
from app.api.settings_router import router as settings_router
from app.api.ai_router import router as ai_router

from starlette.middleware.cors import CORSMiddleware
from app.config import DATABASE_URI
from fastapi import Request, HTTPException

app = FastAPI(openapi_url="/api/v1/openapi.json", 
              docs_url="/api/v1/docs")

# startup
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DATABASE_URI)
    app.mongodb = app.mongodb_client['db']

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# routes
app.include_router(collectors_router, tags=["collectors"], prefix="/api/v1/collectors")
app.include_router(sources_router, tags=["sources"], prefix="/api/v1/sources")
app.include_router(normalization_router, tags=["normalization"], prefix="/api/v1/normalization")
app.include_router(correlation_router, tags=["correlation"], prefix="/api/v1/correlation")
app.include_router(taxanomy_router, tags=["taxanomy"], prefix="/api/v1/taxanomy")
app.include_router(siem_router, tags=["dashboard"], prefix="/api/v1/siem")
app.include_router(netmap_router, tags=["netmap"], prefix="/api/v1/netmap")
app.include_router(settings_router, tags=["settings"], prefix="/api/v1/settings")
app.include_router(ai_router, tags=["ai"], prefix="/api/v1/ai")

# set middleare to check token
async def verify_token(request: Request, call_next):
    token = request.headers.get("token")
    if token:
        alg = jwt.get_unverified_header(token)['alg']
        decoded_token = jwt.decode(token, algorithms=alg, options={"verify_signature": False})
        if "exp" in decoded_token and decoded_token["exp"] < int(time.time()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired authentication token",
            )
    response = await call_next(request)        
    return response

app.middleware("http")(verify_token)

# CORS middleware
origins = [
    'http://localhost:3000',
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['Content-Type', 'application/xml'],
)
