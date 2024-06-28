from fastapi import APIRouter, Request, HTTPException
import datetime
from bson.objectid import ObjectId
from fastapi import Query
import json 
from app.db import db

router = APIRouter()


@router.get("/packets", response_description="List all packets")
async def list_packets(
    request: Request,
    tap: str = Query(None, description="Tap name"),
    proto: str = Query(None, description="Protocol"),
    src_addr: str = Query(None, description="Source IP"),
    tgt_addr: str = Query(None, description="Target IP"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_packets = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if tap:
        query["tap"] = tap
    if proto:
        query["proto"] = proto
    if src_addr:
        query["src_addr"] = src_addr
    if tgt_addr:
        query["tgt_addr"] = tgt_addr
    for doc in await db["packets"].find(query).sort("_id", -1).to_list(length=1000):
        packet = {
            '_id': str(doc['_id']),
            'proto': doc['proto'],
            'tap': doc['tap'],
            'src_addr': doc['src_addr'],
            'tgt_addr': doc['tgt_addr'],
            'raw_data': doc['raw_data'] ,
            'time': doc['time'],
        }
        list_packets.append(packet)
    return list_packets


@router.get("/packets/{id}", response_description="Get a single packet")
async def get_packet(id: str, request: Request):
    if (packet := await db["packets"].find_one({"_id": ObjectId(id)})) is not None:
        packet['_id'] = str(packet['_id'])
        return packet
    raise HTTPException(status_code=404, detail=f"Packet {id} not found")


@router.get("/messages", response_description="List all messages")
async def list_messages(
    request: Request,
    tap: str = Query(None, description="Tap name"),
    src: str = Query(None, description="Source"),
    code: str = Query(None, description="Code"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_messages = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if tap:
        query["tap"] = tap
    if code:
        query["code"] = code
    if src:
        query["source"] = src
    for doc in await db["messages"].find(query).sort("_id", -1).to_list(length=1000):
        message = {
            '_id': str(doc['_id']),
            'tap': doc['tap'],
            'source': doc['source'],
            'code': doc['code'],
            'message': doc['message'],
            'time': doc['time'],
        }
        list_messages.append(message)
    return list_messages


@router.get("/messages/{id}", response_description="Get a single message")
async def get_message(id: str, request: Request):
    if (doc := await db["messages"].find_one({"_id": ObjectId(id)})) is not None:
        doc['_id'] = str(doc['_id'])
        message = {
            '_id': str(doc['_id']),
            'message': doc['message'],
            'tap': doc['tap'],
            'source': doc['source'],
            'tgt_addr': doc['tgt_addr'],
            'proto': doc['proto'],
            'raw_data': doc['raw_data'],
            'time': doc['time'],
        }
        return message        
    raise HTTPException(status_code=404, detail=f"Message {id} not found")


@router.get("/events", response_description="List all events")
async def list_events(
    request: Request,
    event_name: str = Query(None, description="Rule name"),
    tap: str = Query(None, description="Tap name"),
    source: str = Query(None, description="Node name"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_events = []
    query = {}
    if startDate and endDate:
        start_datetime = datetime.datetime.fromisoformat(startDate)
        end_datetime = datetime.datetime.fromisoformat(endDate)
        query['time'] = {"$gte": start_datetime, "$lte": end_datetime}
    if event_name:
        query["name"] = event_name
    if tap:
        query["tap"] = tap
    if source:
        query["source"] = source
    for doc in await db["events"].find(query).sort("_id", -1).to_list(length=10000):
        event = {
            '_id': str(doc['_id']),
            'tap': doc['tap'],
            'source': doc['source'],
            'tgt_addr': doc['tgt_addr'],
            'name': doc['name'],
            'time': doc['time'],
        }
        list_events.append(event)
    return list_events


@router.get("/events/{id}", response_description="Get a single event")
async def get_event(id: str, request: Request):
    if (doc := await db["events"].find_one({"_id": ObjectId(id)})) is not None:
        data = {
            '_id': str(doc['_id']),
            'tap': doc['tap'],
            'source': doc['source'],
            'name': doc['name'],
            'time': doc['time'],
            'tgt_addr': doc['tgt_addr'],
            'proto': doc['proto'],
            'fields': [{k:v for k,v in doc['fields'].items()}]
        }
        return data
    raise HTTPException(status_code=404, detail=f"Rule {id} not found")


@router.get("/incidents", response_description="List all incidents")
async def list_incidents(
    request: Request,
    tactic: str = Query(None, description="Filter by tactic"),
    severity: str = Query(None, description="Filter by severity"),
    startDate: str = Query(None, description="Start date"),
    endDate: str = Query(None, description="End date")
):
    list_incidents = []
    filter_query = {}
    if tactic:
        filter_query['tactic'] = tactic
    if severity:
        filter_query['severity'] = severity
    color = {
      'high':'error',
      'med':'warning',
      'low':'secondary' 
    }
    for doc in await db["incidents"].find(filter_query).sort("_id", -1).to_list(length=1000):
        sev = doc.get('severity')
        incident = {
            '_id': str(doc['_id']),
            'name': doc['name'],
            'description': doc['desc'],
            'time': doc.get('time'),
            'severity': sev,
            'tactic': doc.get('tactic'),
            'positive': doc.get('positive'),
            'color': color.get(sev)
        }
        incident['taps'] = [x['tap'] for x in doc['events'].values()]
        incident['nodes'] = [x['source'] for x in doc['events'].values()]
        list_incidents.append(incident)
    return list_incidents


@router.get("/incidents/{id}", response_description="Get a single incident")
async def get_incident(id: str, request: Request):
    color = {
      'high':'error',
      'med':'warning',
      'low':'secondary' 
    }
    if (doc := await db["incidents"].find_one({"_id": ObjectId(id)})) is not None:
        data = {
            '_id': str(doc['_id']),
            'name': doc['name'],
            'desc': doc['desc'],
            'tactic': doc['tactic'],
            'severity': doc['severity'],
            'time': doc['time'],
            'color': color[doc['severity']],
            'status': 'Positive' if doc['positive'] else 'FalsePositive',
            'events': [],
        }
        for event in doc['events'].values():
            d = {
                'Name': event['name'],
                'Tap': event['tap'],
                'Source': event['source'],
                'Target': event['tgt_addr'],
                'Time': event['time'],
            }
            for key, value in event['fields'].items():
                d[key] = value
            data['events'].append(d)
        return data
    raise HTTPException(status_code=404, detail=f"Meta event {id} not found")


@router.get("/incidents/filter", response_description="Get a filter incident")
async def filter_incident(id: str, request: Request):
    list_incidents = []
    return list_incidents


@router.get("/playbook/{id}", response_description="Get a playbook for meta event")
async def get_playbook(id: str, request: Request):
    incident = await db["incidents"].find_one({"_id": ObjectId(id)})
    if incident:
        playbook = []
        return playbook
    raise HTTPException(status_code=404, detail=f"Meta event {id} not found")
