from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json 
router = APIRouter()

templates = Jinja2Templates(directory="app/pages")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Dashboards
@router.get("/dash/siem", response_class=HTMLResponse)
async def dash_siem(request: Request):

    return templates.TemplateResponse("dash_siem.html", {"request": request})

@router.get("/dash/ids", response_class=HTMLResponse)
async def dash_ids(request: Request):
    return templates.TemplateResponse("dash_ids.html", {"request": request})

# Monitoring
@router.get("/mon/net", response_class=HTMLResponse)
async def mon_net(request: Request):
    return templates.TemplateResponse("mon_net.html", {"request": request})

@router.get("/mon/risk", response_class=HTMLResponse)
async def mon_risk(request: Request):
    return templates.TemplateResponse("mon_risk.html", {"request": request})

@router.get("/mon/unk", response_class=HTMLResponse)
async def mon_unk(request: Request):
    return templates.TemplateResponse("mon_unk.html", {"request": request})

# Configuration
@router.get("/conf/coll", response_class=HTMLResponse)
async def conf_coll(request: Request):
    return templates.TemplateResponse("conf_coll.html", {"request": request})

@router.get("/conf/norm", response_class=HTMLResponse)
async def conf_norm(request: Request):
    return templates.TemplateResponse("conf_norm.html", {"request": request})

@router.get("/conf/corr", response_class=HTMLResponse)
async def conf_corr(request: Request):
    return templates.TemplateResponse("conf_corr.html", {"request": request})

# Data
@router.get("/data/pkt", response_class=HTMLResponse)
async def data_pkt(request: Request):
    return templates.TemplateResponse("data_pkt.html", {"request": request})

@router.get("/data/msg", response_class=HTMLResponse)
async def data_msg(request: Request):
    return templates.TemplateResponse("data_msg.html", {"request": request})

@router.get("/data/evt", response_class=HTMLResponse)
async def data_evt(request: Request):
    return templates.TemplateResponse("data_evt.html", {"request": request})

@router.get("/data/inc", response_class=HTMLResponse)
async def data_inc(request: Request):
    return templates.TemplateResponse("data_inc.html", {"request": request})

