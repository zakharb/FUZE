from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import datetime

import random

router = APIRouter()

@router.get("/polar", response_description="Polar chart")
async def polar(request: Request, timeframe: str = None):
  labels = ['High', 'Medium', 'Low']
  now = datetime.datetime.utcnow()
  if timeframe == '1h':
    previous_minute = now - datetime.timedelta(minutes=60)
  elif timeframe == '8h':
    previous_minute = now - datetime.timedelta(minutes=480)
  else:
    previous_minute = now - datetime.timedelta(minutes=1440)
  query = {'time': {'$gte': previous_minute}, 'severity': 'low', 'positive':True}
  low = 5
  query = {'time': {'$gte': previous_minute}, 'severity': 'med', 'positive':True}
  med = 4
  query = {'time': {'$gte': previous_minute}, 'severity': 'high', 'positive':True}
  high = await request.app.mongodb["meta_events"].count_documents(query)
  data = [high, med, low]
  response_data = {
    'labels': labels,
    'data': data,
  }
  return response_data

@router.get("/radar", response_description="Radar chart")
async def radar(request: Request, timeframe: str = None):
  dataset1_label = 'Critical'
  dataset3_label = 'Total'
  now = datetime.datetime.utcnow()
  if timeframe == '1h':
    previous_minute = now - datetime.timedelta(minutes=60)
  elif timeframe == '8h':
    previous_minute = now - datetime.timedelta(minutes=480)
  else:
    previous_minute = now - datetime.timedelta(minutes=1440)
  query = {'time': {'$gte': previous_minute}}
  data = await request.app.mongodb["meta_events"].find(query).to_list(length=1000)
  positive_events = {
    'Class 1': 2,
    'Class 2': 3,
    'Class 3': 4,
    'Class 4': 8,
    'Class 5': 0,
    'Class 6': 0
  }
  total_events = positive_events.copy()
  for d in data:
    if d['tactic'] not in total_events:
      total_events[d['tactic']] = 1
      if d['positive']:
        positive_events[d['tactic']] = 1
      else:
        positive_events[d['tactic']] = 0
    else:
      total_events[d['tactic']] += 1
      if d['positive']:
        positive_events[d['tactic']] += 1
  total_events = {key: value 
          for key, value 
          in sorted(total_events.items(), key=lambda item: item[1])[::-1]}
  labels = [x for x in total_events]
  dataset3_data = [x for x in total_events.values()]
  dataset1_data = []
  for label in labels:
    dataset1_data.append(positive_events[label])
  response_data = {
    'labels': labels,
    'dataset1_label': dataset1_label,
    'dataset1_data': dataset1_data,
    'dataset3_label': dataset3_label,
    'dataset3_data': dataset3_data,
  }
  return response_data
 
@router.get("/bar", response_description="Bar chart")
async def bar(request: Request, timeframe: str = None):
  data = []
  queries = []
  now = datetime.datetime.utcnow()
  if timeframe == '1d':
    previous_minute = now - datetime.timedelta(minutes=60)
  elif timeframe == '1m':
    previous_minute = now - datetime.timedelta(minutes=480)
  else:
    for interval in range(6,-1,-1):
      start_date = now - datetime.timedelta(days=interval)
      end_date = now - datetime.timedelta(days=interval - 1)
      query = {"$and": [
        {'time': {'$gte': start_date }},
        {'time': {'$lt': end_date }}, 
        {'positive':True} 
      ]}
      d = await request.app.mongodb["meta_events"].find(query).to_list(length=1000)
      data.append(d)
  i = 0
  dataset1_data = [0,0,2,0,0,0,0]
  dataset2_data = [0,0,0,0,3,0,0]
  dataset3_data = [0,1,0,0,0,0,0]
  dataset4_data = [0,0,2,0,0,0,0]
  dataset5_data = [0,0,0,0,3,0,0]
  dataset6_data = [0,0,1,0,0,0,0]
  dataset7_data = [0,0,4,0,0,0,0]
  dataset8_data = [0,1,0,0,0,0,0]
  leng = 0
  for d in data:
    leng += len(d)
    for event in d:
      if event['tactic'] == 'Discovery':
        dataset1_data[i] += 1
      elif event['tactic'] == 'Execution':
        dataset2_data[i] += 1
      elif event['tactic'] == 'Command and Control':
        dataset3_data[i] += 1
      elif event['tactic'] == 'Impact':
        dataset4_data[i] += 1
      elif event['tactic'] == 'Evasion':
        dataset5_data[i] += 1
      elif event['tactic'] == 'Lateral Movement':
        dataset6_data[i] += 1
      elif event['tactic'] == 'Persistence':
        dataset7_data[i] += 1
      elif event['tactic'] == 'Execution':
        dataset8_data[i] += 1
    i += 1
  today = datetime.date.today()
  labels = [str((today - datetime.timedelta(days=i)).strftime('%d.%m')) for i in range(6,-1,-1)]
  dataset1_label = 'SSH'
  dataset3_label = 'FTP'
  dataset2_label = 'SMB'
  dataset4_label = 'Modbus'
  dataset5_label = 'HTTP'
  dataset6_label = 'Lateral Movement'
  dataset7_label = 'Persistence'
  dataset8_label = 'Execution'
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
    'dataset6_label': dataset6_label,
    'dataset6_data': dataset6_data,
    'dataset7_label': dataset7_label,
    'dataset7_data': dataset7_data,
    'dataset8_label': dataset8_label,
    'dataset8_data': dataset8_data,
  }
  return response_data
 
@router.get("/sum_chart", response_description="Summary chart")
async def sum_chart(request: Request):
  now = datetime.datetime.now()
  label = 0
  labels = []
  data = []
  for i in range(59,0,-1):
    start_date = now - datetime.timedelta(minutes=i*24)
    end_date = now - datetime.timedelta(minutes=i*24 - 24)
    query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }}, {'positive':True} ]}
    events = await request.app.mongodb["meta_events"].count_documents(query)
    data.append(events)
    label += events
    minute = (now - datetime.timedelta(minutes=i*24)).minute
    hour = (now - datetime.timedelta(minutes=i*24)).hour
    dt = f"{hour:02d}:{minute:02d}"
    labels.append(dt)  
  response_data = {
    'labels': labels,
    'label': label,
    'data': data,
  }
  return response_data
 
@router.get("/timeline", response_description="Timeline chart full")
async def timeline_chart(request: Request, timeframe: str = None):
  dataset1_label = 'Sources'
  dataset2_label = 'Destinations'
  dataset3_label = 'Services'
  now = datetime.datetime.utcnow()
  labels = []
  dataset1_data = []
  dataset2_data = []
  dataset3_data = []
  if timeframe == '0h':
    start_date = now - datetime.timedelta(minutes=1)
    end_date = now
    query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }} ]}
    messages = await request.app.mongodb["messages"].count_documents(query)
    events = await request.app.mongodb["events"].count_documents(query)
    query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }}, {'positive': True} ]}
    meta_events = await request.app.mongodb["meta_events"].count_documents(query)
    dataset1_data = messages
    dataset2_data = events
    dataset3_data = meta_events
    labels = now.strftime("%H:%M")
  elif timeframe == '8h':
    for i in range(59,0,-1):
      start_date = now - datetime.timedelta(minutes=i*8)
      end_date = now - datetime.timedelta(minutes=i*8 - 8)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }} ]}
      messages = await request.app.mongodb["messages"].count_documents(query)
      events = await request.app.mongodb["events"].count_documents(query)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }}, {'positive': True} ]}
      meta_events = await request.app.mongodb["meta_events"].count_documents(query)
      dataset1_data.append(messages)
      dataset2_data.append(events)
      dataset3_data.append(meta_events)
      minute = (now - datetime.timedelta(minutes=i*8)).minute
      hour = (now - datetime.timedelta(minutes=i*8)).hour
      dt = f"{hour:02d}:{minute:02d}"
      labels.append(dt)
  elif timeframe == '24h':
    for i in range(59,0,-1):
      start_date = now - datetime.timedelta(minutes=i*24)
      end_date = now - datetime.timedelta(minutes=i*24 - 24)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }} ]}
      messages = await request.app.mongodb["messages"].count_documents(query)
      events = await request.app.mongodb["events"].count_documents(query)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }}, {'positive': True} ]}
      meta_events = await request.app.mongodb["meta_events"].count_documents(query)
      dataset1_data.append(messages)
      dataset2_data.append(events)
      dataset3_data.append(meta_events)
      minute = (now - datetime.timedelta(minutes=i*24)).minute
      hour = (now - datetime.timedelta(minutes=i*24)).hour
      dt = f"{hour:02d}:{minute:02d}"
      labels.append(dt)
  elif timeframe == '1h':
    for i in range(59,0,-1):
      start_date = now - datetime.timedelta(minutes=i)
      end_date = now - datetime.timedelta(minutes=i - 1)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }} ]}
      messages = await request.app.mongodb["messages"].count_documents(query)
      events = await request.app.mongodb["events"].count_documents(query)
      query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }}, {'positive': True} ]}
      meta_events = await request.app.mongodb["meta_events"].count_documents(query)
      dataset1_data.append(messages)
      dataset2_data.append(events)
      dataset3_data.append(meta_events)
      minute = (now - datetime.timedelta(minutes=i)).minute
      hour = (now - datetime.timedelta(minutes=i)).hour
      dt = f"{hour:02d}:{minute:02d}"
      labels.append(dt)
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

@router.get("/total_messages", response_description="Total Meassages")
async def total_messages(request: Request):
    rules = await request.app.mongodb["sources"].find().to_list(length=10000)
    data = {
        'total': len(rules),
        'change': 0,
    }
    return data

 
@router.get("/total_events", response_description="Total Events")
async def total_events(request: Request):
    rules = await request.app.mongodb["destinations"].find().to_list(length=10000)
    data = {
        'total': len(rules),
        'change': 0,
    }
    return data

@router.get("/total_incidents", response_description="Total Incidents")
async def total_incidents(request: Request):
    rules = await request.app.mongodb["services"].find().to_list(length=1000)
    data = {
        'total': len(rules),
        'change': 0,
    }
    return data
  
@router.get("/top_categories", response_description="Total categories")
async def top_categories(request: Request):
    now = datetime.datetime.utcnow()
    start_date = now - datetime.timedelta(days=1)
    end_date = now
    query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }},{'positive': True } ]}
    last_month = await request.app.mongodb["meta_events"].find(query).to_list(length=1000)
    start_date = now - datetime.timedelta(minutes=60)
    query = {"$and": [{'time': {'$gte': start_date }},{'time': {'$lt': end_date }},{'positive': True } ]}
    last_day = await request.app.mongodb["meta_events"].find(query).to_list(length=1000)
    data_month = {
      'Initial Access': 2,
      'Execution': 3,
      'Persistence': 4,
      'Privilege Escalation': 0,
      'Evasion': 0,
      'Discovery': 0,
      'Lateral Movement': 0,
      'Collection': 0,
      'Command and Control': 0,
      'Inhibit Response Function': 0,
      'Impair Process Control': 0,
      'Impact': 0
    }
    data_day = {
      'Initial Access': 0,
      'Execution': 0,
      'Persistence': 0,
      'Privilege Escalation': 0,
      'Evasion': 0,
      'Discovery': 0,
      'Lateral Movement': 0,
      'Collection': 0,
      'Command and Control': 0,
      'Inhibit Response Function': 0,
      'Impair Process Control': 0,
      'Impact': 0
    }
    for d in last_month:
      if d['tactic'] in data_month:
        data_month[d['tactic']] += 1
    for d in last_day:
      if d['tactic'] in data_day:
        data_day[d['tactic']] += 1
    data = [
    {
      'id': 1,
      'title': 'Zero hits Rules',
      'count': data_month['Initial Access'],
      'subtitle': 'rules without data',
      'delta': data_day['Initial Access'],
      'href': '',
    },
    {
      'id': 2,
      'title': 'All ports Services',
      'count': data_month['Execution'],
      'subtitle': 'all range of ports used',
      'delta': data_day['Execution'],
      'href': '',
    },
    {
      'id': 3,
      'title': '3 Rule Detection',
      'count': data_month['Persistence'],
      'subtitle': 'description',
      'delta': data_day['Persistence'],
      'href': 'https://attack.mitre.org/tactics/TA0110/',
    },
    {
      'id': 4,
      'title': '4 Rule Detection',
      'count': data_month['Privilege Escalation'],
      'subtitle': 'description',
      'delta': data_day['Privilege Escalation'],
      'href': 'https://attack.mitre.org/tactics/TA0111/',
    },
    {
      'id': 5,
      'title': '5 Rule Detection',
      'count': data_month['Evasion'],
      'subtitle': 'description',
      'delta': data_day['Evasion'],
      'href': 'https://attack.mitre.org/tactics/TA0103/',
    },
    {
      'id': 6,
      'title': '6 Rule Detection',
      'count': data_month['Discovery'],
      'subtitle': 'description',
      'delta': data_day['Discovery'],
      'href': 'https://attack.mitre.org/tactics/TA0102/',
    },
    {
      'id': 7,
      'title': '7 Rule Detection',
      'count': data_month['Lateral Movement'],
      'subtitle': 'move through your environment',
      'delta': data_day['Lateral Movement'],
      'href': 'https://attack.mitre.org/tactics/TA0109/',
    },
    {
      'id': 8,
      'title': '8 Rule Detection',
      'count': data_month['Collection'],
      'subtitle': 'description',
      'delta': data_day['Collection'],
      'href': 'https://attack.mitre.org/tactics/TA0100/',
    },
    {
      'id': 9,
      'title': '9 Rule Detection',
      'count': data_month['Command and Control'],
      'subtitle': 'description',
      'delta': data_day['Command and Control'],
      'href': 'https://attack.mitre.org/tactics/TA0101/',
    },
    {
      'id': 10,
      'title': '10 Rule Detection',
      'count': data_month['Inhibit Response Function'],
      'subtitle': 'description',
      'delta': data_day['Inhibit Response Function'],
      'href': 'https://attack.mitre.org/tactics/TA0107/',
    },
    {
      'id': 11,
      'title': '11 Rule Detection',
      'count': data_month['Impair Process Control'],
      'subtitle': 'description',
      'delta': data_day['Impair Process Control'],
      'href': 'https://attack.mitre.org/tactics/TA0106/',
    },
    {
      'id': 12,
      'title': '12 Rule Detection',
      'count': data_month['Impact'],
      'subtitle': 'description',
      'delta': data_day['Impact'],
      'href': 'https://attack.mitre.org/tactics/TA0105/',
    },
    ]
    return data

