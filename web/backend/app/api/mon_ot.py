from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime
import random

router = APIRouter()

@router.get("/polar", response_description="Polar chart")
async def polar(request: Request, timeframe: str = None):
  labels = []
  if timeframe == '1h':
    data = []
  elif timeframe == '8h':
    data = []
  else:
    data = []
  response_data = {
    'labels': labels,
    'data': data,
  }
  return response_data

@router.get("/radar", response_description="Radar chart")
async def radar(request: Request, timeframe: str = None):
  labels = ['Vector', 'Complexity', 'Privilege', 'User Interaction', 'Scope', 'Confidentiality', 'Integrity', 'Availability' ]
  dataset1_label = 'High'
  dataset2_label = 'Medium'
  dataset3_label = 'Low'
  if timeframe == '1h':
    dataset1_data = [0.1, 0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0, 0]
  elif timeframe == '8h':
    dataset1_data = [0.1, 0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0, 0]
  else:
    dataset1_data = [0.1, 0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0, 0]
  response_data = {
    'labels': labels,
    'dataset1_label': dataset1_label,
    'dataset1_data': dataset1_data,
    'dataset2_label': dataset2_label,
    'dataset2_data': dataset2_data,
    'dataset3_label': dataset3_label,
    'dataset3_data': dataset3_data,
  }
  return response_data

@router.get("/bar", response_description="Bar chart")
async def bar(request: Request, timeframe: str = None):
  today = datetime.date.today()
  labels = [str((today - datetime.timedelta(days=i)).strftime('%d.%m')) for i in range(6,-1,-1)]
  dataset1_label = 'Modbus'
  dataset2_label = 'OPC'
  dataset3_label = 'DNP'
  dataset4_label = 'Ethernet/IP'
  dataset5_label = 'Other'
  if timeframe == '1d':
    dataset1_data = [0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0]
    dataset4_data = [0, 0, 0, 0, 0, 0, 0]
    dataset5_data = [0, 0, 0, 0, 0, 0, 0]
  elif timeframe == '1w':
    dataset1_data = [0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0]
    dataset4_data = [0, 0, 0, 0, 0, 0, 0]
    dataset5_data = [0, 0, 0, 0, 0, 0, 0]
  else:
    dataset1_data = [0, 0, 0, 0, 0, 0, 0]
    dataset2_data = [0, 0, 0, 0, 0, 0, 0]
    dataset3_data = [0, 0, 0, 0, 0, 0, 0]
    dataset4_data = [0, 0, 0, 0, 0, 0, 0]
    dataset5_data = [0, 0, 0, 0, 0, 0, 0]
  response_data = {
    'labels': labels,
    'dataset1_label': dataset1_label,
    'dataset1_data': dataset1_data,
    'dataset2_label': dataset2_label,
    'dataset2_data': dataset2_data,
    'dataset3_label': dataset3_label,
    'dataset3_data': dataset3_data,
    'dataset4_label': dataset4_label,
    'dataset4_data': dataset4_data,
    'dataset5_label': dataset5_label,
    'dataset5_data': dataset5_data,
  }
  return response_data

@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
  name = 'Incidents'
  labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
  label = '+0'
  data = [0, 0, 0, 0, 0, 0, 0]
  response_data = {
    'name': name,
    'labels': labels,
    'label': label,
    'data': data,
  }
  return response_data


@router.get("/timeline", response_description="Timeline chart full")
async def timeline_chart(request: Request, timeframe: str = None):
  dataset1_label = 'Traffic'
  dataset2_label = 'Packets'
  dataset3_label = 'Errors'
  now = datetime.datetime.utcnow()
  labels = []
  if timeframe == '0':
    labels = datetime.datetime.utcnow().strftime("%H:%M")
    dataset1_data = random.randint(20, 30)
    dataset2_data = random.randint(10, 20)
    dataset3_data = random.randint(0, 10)
  else:
    if timeframe == '1h':
      for i in reversed(range(60)):
          minute = (now - datetime.timedelta(minutes=i)).minute
          hour = (now - datetime.timedelta(minutes=i)).hour
          dt = f"{hour:02d}:{minute:02d}"
          labels.append(dt)
    elif timeframe == '8h':
      for i in reversed(range(60)):
          minute = (now - datetime.timedelta(minutes=i)).minute
          hour = (now - datetime.timedelta(minutes=i)).hour
          dt = f"{hour:02d}:{minute:02d}"
          labels.append(dt)
    elif timeframe == '24h':
      for i in reversed(range(60)):
          minute = (now - datetime.timedelta(minutes=i)).minute
          hour = (now - datetime.timedelta(minutes=i)).hour
          dt = f"{hour:02d}:{minute:02d}"
          labels.append(dt)
    dataset1_data  = [0 for _ in range(60)]
    dataset2_data = [0 for _ in range(60)]
    dataset3_data = [0 for _ in range(60)]
  response_data = {
    'labels': labels,
    'dataset1_label': dataset1_label,
    'dataset2_label': dataset2_label,
    'dataset3_label': dataset3_label,
    'dataset1_data': dataset1_data,
    'dataset2_data': dataset2_data,
    'dataset3_data': dataset3_data,
  }
  return response_data

@router.get("/total_devices", response_description="Total Devices")
async def total_messages(request: Request):
    total = 0
    taps = await request.app.mongodb["collections"].find().to_list(length=100)
    for tap in taps:
      total += len(tap['nodes'])
    data = {
        'total': total,
        'change': '100',
    }
    return data
 
@router.get("/total_active", response_description="Total active Devices")
async def total_threats(request: Request):
    total = 0
    taps = await request.app.mongodb["collections"].find().to_list(length=100)
    for tap in taps:
      total += len(tap['nodes'])
    data = {
        'total': total,
        'change': '0',
    }
    return data
  
@router.get("/total_disconnected", response_description="Total disconnected Devices")
async def total_positives(request: Request):
    data = {
        'total': 0,
        'change': '100',
    }
    return data
 
@router.get("/top_categories", response_description="Total categories")
async def top_categories(request: Request):
    data = [
      {
        "id": 1,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 2,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 3,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 4,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 5,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 6,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      },
      {
        "id": 7,
        "title": "",
        "count": "",
        "subtitle": "",
        "delta": "",
        "href": ""
      }
    ]
    return data
