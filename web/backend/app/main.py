from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import conf_coll
from app.api import conf_norm
from app.api import conf_corr
from app.api import dash_siem
from app.api import dash_ids
from app.api import mon_net
from app.api import mon_risk
from app.api import mon_unk
from app.api import data
from app.api import opt_set
from app import page_routes

app = FastAPI(openapi_url="/api/v1/openapi.json", 
              docs_url="/api/v1/docs")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/js", StaticFiles(directory="app/js"), name="js")
app.mount("/styles", StaticFiles(directory="app/styles"), name="styles")
app.mount("/components", StaticFiles(directory="app/components"), name="components")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# page routes
app.include_router(page_routes.router)

# api routes
app.include_router(conf_coll.router, tags=["conf_collection"], prefix="/api/collection")
app.include_router(conf_norm.router, tags=["conf_normalization"], prefix="/api/normalization")
app.include_router(conf_corr.router, tags=["conf_correlation"], prefix="/api/correlation")
app.include_router(data.router, tags=["data"], prefix="/api/data")
app.include_router(dash_siem.router, tags=["dashboard_siem"], prefix="/api/siem")
app.include_router(dash_ids.router, tags=["dashboard_ids"], prefix="/api/ids")
app.include_router(mon_net.router, tags=["monitor_netmap"], prefix="/api/netmap")
app.include_router(mon_risk.router, tags=["monitor_risk_assesment"], prefix="/api/risk")
app.include_router(mon_unk.router, tags=["monitor_unknown_sources"], prefix="/api/unk")
app.include_router(opt_set.router, tags=["settings"], prefix="/api/settings")